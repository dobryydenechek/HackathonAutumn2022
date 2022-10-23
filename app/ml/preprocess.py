import csv
from scapy.all import *
import pandas as pd
from sklearn import preprocessing
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.model_selection import cross_val_score
from sklearn.metrics import accuracy_score
from sklearn.metrics import f1_score
from sklearn.metrics import precision_recall_curve, classification_report
from tqdm import tqdm

le_class = preprocessing.LabelEncoder()
le_class2 = preprocessing.LabelEncoder()

def get_key(value, class_names):
    for key in class_names:
        if value in class_names[key]:
            return key

def read_pcap(folder: str):
    print('Read pcaps...')
    b1 = []
    b7 = []
    b8 = []
    c1 = []
    c2 = []
    c3 = []
    c4 = []
    c5 = []
    c6 = []
    c7 = []
    c8 = []
    c9 = []
    c10 = []
    c16 = []
    class_name = []
    class_name2 = []
    count = 0

    class_names = {
        'chats': ['vpn_facebook_chat1a', 'vpn_icq_chat1a', 'vpn_skype_chat1a', 'vpn_hangouts_chat1a'],
        'voice_chats': ['vpn_facebook_audio2', 'vpn_skype_audio1', 'vpn_voipbuster1a', 'vpn_hangouts_audio1'], 
        'video': ['vpn_netflix_A', 'vpn_vimeo_A', 'vpn_youtube_A'],
        'audio': ['vpn_spotify_A'],
        'files': ['vpn_bittorrent', 'vpn_skype_files1a'],
        'email': ['vpn_email2a'],
        'sftp': ['vpn_sftp_A'],
        'ftps': ['vpn_ftps_A']
    }
    dict_apps = {x.split('.')[0]: y for y, x in enumerate(os.listdir(folder))}
    print(dict_apps)
    dict_classes = {x: y for y, x in enumerate(list(class_names.keys()))}
    print(dict_classes)
    for file in tqdm(os.listdir(folder)):
        path = os.path.join(folder, file)
        pkts = rdpcap(path)
        pkt = [i for i in pkts[0:500]]  
        
        for pkt0 in pkt:
            try:
                c16.append(pkt0['TCP'].options[2][1])
                c1.append(pkt0['TCP'].sport)
                c2.append(pkt0['TCP'].dport)
                c3.append(pkt0['TCP'].seq)
                c4.append(pkt0['TCP'].ack)
                c5.append(pkt0['TCP'].dataofs)
                c6.append(pkt0['TCP'].reserved)
                # c7.append(pkt0['TCP'].flags)
                c8.append(pkt0['TCP'].window)
                c9.append(pkt0['TCP'].chksum)
                c10.append(pkt0['TCP'].urgptr)
                b1.append(pkt0['IP'].version)
                b7.append(pkt0['IP'].src)
                b8.append(pkt0['IP'].dst)
                # class_name.append(dict_apps[file.split('.')[0]])
                class_name2.append(dict_classes[get_key(file.split('.')[0], class_names)])

            except:
                count+=1

        
    print(len(c1), len(class_name2))
    try:
        df = pd.DataFrame({'src': b7, 'dst': b8, 'version': b1, 'sport': c1, 'dport': c2, 'seq' :c3, 'ask': c4, 'dataofs': c5, 
        'reserved': c6, 'window': c8, 'chksum': c9, 'urgptr': c10, 'class2': class_name2, 'timestamp': c16})
        print(pd.unique(df['class2']))
    except:
        df = pd.DataFrame({'src': b7, 'dst': b8, 'version': b1, 'sport': c1, 'dport': c2, 'seq' :c3, 'ask': c4, 'dataofs': c5, 
        'reserved': c6, 'window': c8, 'chksum': c9, 'urgptr': c10, 'timestamp': c16})
    return df

    
def preprocess_df(data: pd.DataFrame):
    print('Preprocess datset...')
    done_df = pd.DataFrame()
    done_df['sport'] = data['sport']
    done_df['dport'] = data['dport']
    done_df['seq'] = data['seq']
    done_df['ask'] = data['ask']
    done_df['dataofs'] = data['dataofs']
    done_df['window'] = data['window']
    done_df['chksum'] = data['chksum']
    done_df['timestamp'] = data['timestamp']
    # done_df['class'] = data['class']
    try:
        done_df['class2'] = data['class2']
    except:
        done_df['class2'] = 0
    # print(done_df)
    return done_df

def train_apps_model(done_df: pd.DataFrame):
    print('Start training apps model...')
    done_df.reset_index(drop=True, inplace=True)
    X = done_df.loc[:, 'sport':'chksum']
    y = done_df['class']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    y_train.reset_index(drop=True, inplace=True)
    y_test.reset_index(drop=True, inplace=True)

    xgbc = XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
       colsample_bynode=1, colsample_bytree=1, gamma=0, learning_rate=0.1,
       max_delta_step=0, max_depth=3, min_child_weight=1, missing=1,
       n_estimators=100, n_jobs=1, nthread=None,
       objective='multi:softprob', random_state=0, reg_alpha=0,
       reg_lambda=1, scale_pos_weight=1, seed=None, silent=None,
       subsample=1, verbosity=1)

    xgbc.fit(X_train, y_train)
    print('Training completed!')
    y_pred = xgbc.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(pd.unique(y_train))
    print('Accuracy: ', accuracy)
    f1 = f1_score(y_test, y_pred, average='macro')
    print('F1-score: ', f1)

    return xgbc

def train_classes_model(done_df: pd.DataFrame):
    print('Start training classes model...')
    done_df.reset_index(drop=True, inplace=True)
    X = done_df.loc[:, 'sport':'chksum']
    y = done_df['class2']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    y_train.reset_index(drop=True, inplace=True)
    y_test.reset_index(drop=True, inplace=True)
    print(pd.unique(y_train))

    xgbc = XGBClassifier(base_score=0.5, booster='gbtree', colsample_bylevel=1,
       colsample_bynode=1, colsample_bytree=1, gamma=0, learning_rate=0.1,
       max_delta_step=0, max_depth=3, min_child_weight=1, missing=1,
       n_estimators=100, n_jobs=1, nthread=None, random_state=0, reg_alpha=0,
       reg_lambda=1, scale_pos_weight=1, seed=None, silent=None,
       subsample=1, verbosity=1, objective='multi:softprob')

    xgbc.fit(X_train, y_train)
    print('Training completed!')
    y_pred = xgbc.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print('Accuracy: ', accuracy)
    f1 = f1_score(y_test, y_pred, average='macro')
    print('F1-score:', f1)

    return xgbc

from .preprocess import read_pcap, preprocess_df
import xgboost as xgb

def preprocess_data(folder_path):
    df = read_pcap(folder_path)
    done_df = preprocess_df(df)
    # done_df = done_df.loc[:, 'sport':'chksum']
    return done_df

def predict_models(apps_model_path, classes_model_path, df):
    dict_apps = {'vpn_bittorrent': 0, 'vpn_email2a': 1, 'vpn_facebook_audio2': 2, 'vpn_facebook_chat1a': 3, 'vpn_ftps_A': 4, 'vpn_hangouts_audio1': 5, 'vpn_hangouts_chat1a': 6, 'vpn_icq_chat1a': 7, 'vpn_netflix_A': 8, 'vpn_sftp_A': 9, 'vpn_skype_audio1': 10, 'vpn_skype_chat1a': 11, 'vpn_skype_files1a': 12, 'vpn_spotify_A': 13, 'vpn_vimeo_A': 14, 'vpn_voipbuster1a': 15, 'vpn_youtube_A': 16}
    dict_classes = {'chats': 0, 'voice_chats': 1, 'video': 2, 'audio': 3, 'files': 4, 'email': 5, 'sftp': 6, 'ftps': 7}
    # apps_model = xgb.XGBClassifier()
    # apps_model.load_model(apps_model_path)
    done_df = df.copy()
    # done_df['apps_class'] = [dict_apps.keys()[dict_apps.values().index(i)] for i in apps_model.predict(df)]
    

    classes_model = xgb.XGBClassifier()
    classes_model.load_model(classes_model_path)
    done_df['class2'] = classes_model.predict(df.loc[:, 'sport':'chksum'])

    print(len(done_df['class2']), len(done_df.loc[done_df['class2']==0]))
    # done_df['classes_model'] = [dict_classes.keys()[dict_apps.values().index(i)] for i in classes_model.predict(df)]
    return done_df

def save_csv(path, pcap_dir):
    done_df  = predict_models('saved_models/apps_model.txt', '/app/ml/saved_models/classes_model.txt', preprocess_data(pcap_dir))
    done_df.to_csv(path)

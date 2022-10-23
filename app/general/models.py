from datetime import datetime

from secrets import choice
from django.db import models


bnt = {'blank': True, 'null': True}


class Interface(models.Model):
    title = models.CharField(max_length=30)

pcaps_1 = [
    'bittorrent',
    'email',
    'facebook_audio',
    'facebook_chat'
    'icq_chat',
    'netflix',
    'sftp',
    'skype_audio',
    'skype_chat',
    'skype_files',
    'spotify',
    'vimeo',
    'voipbuster1a',
    'youtube',
]

class_names = {
    'chats': ['vpn_facebook_chat1a', 'vpn_icq_chat1a', 'vpn_skype_chat1a'],
    'voice_chats': ['vpn_facebook_audio2', 'vpn_skype_audio1', 'vpn_voipbuster1a'], 
    'video': ['vpn_netflix_A', 'vpn_vimeo_A', 'vpn_youtube_A'],
    'audio': ['vpn_spotify_A'],
    'files': ['vpn_bittorrent', 'vpn_skype_files1a'],
    'email': ['vpn_email2a']
}


class Trafic(models.Model):
    CHOICES = [
        (0, 'chats'),
        (1, 'video'),
        (2, 'files'),
        (3, 'email'),
        (4, 'sftp'),
        (5, 'ftps')
    ]
    package   = models.ForeignKey('Package', on_delete=models.CASCADE, **bnt)
    type      = models.IntegerField(choices=CHOICES ,**bnt)
    sport     = models.CharField(max_length=50, **bnt)
    dport     = models.CharField(max_length=50, **bnt)
    seq       = models.CharField(max_length=50, **bnt)
    ask       = models.CharField(max_length=50, **bnt)
    dataofs   = models.CharField(max_length=50, **bnt)
    window    = models.CharField(max_length=50, **bnt)
    chksum    = models.CharField(max_length=50, **bnt)
    timestamp = models.CharField(max_length=50, **bnt)

    def get_type(self):
        for i, s in self.CHOICES:
            if i == self.type: return s


class Group(models.Model):
    title = models.CharField(max_length=30)

def get_pcap_upload_to(instance, filename):
    t = datetime.now()
    return f'upload/persone_pk_{instance.persone.pk}/{t.year}/{t.month}/{t.day}/{t.time().minute}/pcap/{filename}'

def get_csv_upload_to(instance, filename):
    return f'upload/'

class Package(models.Model):
    date_create = models.DateTimeField(auto_now_add=True, **bnt)
    start_date  = models.DateTimeField(**bnt)
    end_date    = models.DateTimeField(**bnt)
    title       = models.CharField(max_length=30, **bnt)
    pcaps       = models.ManyToManyField('PCAPFile')
    csv         = models.ForeignKey('CSVFile', on_delete=models.CASCADE, **bnt)
    persone     = models.ForeignKey('Persone', on_delete=models.CASCADE, **bnt)

    def get_types(self):
        ts = Trafic.objects.filter(package=self)
        r = {}
        for c, s in Trafic.CHOICES:
            count = ts.filter(type=c).count()
            if count: r[s] = count
        maxx = max([v for k, v in r])
        return r, maxx

class PCAPFile(models.Model):
    persone  = models.ForeignKey('Persone', on_delete=models.CASCADE, **bnt)
    filename = models.CharField(max_length=100, **bnt)
    file     = models.FileField(upload_to=get_pcap_upload_to, **bnt)

    def get_path_dir(self):
        s = str(self.file)
        return s[:s.rfind('/')+1]


class CSVFile(models.Model):
    persone = models.ForeignKey('Persone', on_delete=models.CASCADE, **bnt)
    filename = models.CharField(max_length=100, **bnt)
    file = models.FileField(upload_to=get_csv_upload_to, **bnt)

    def get_path_dir(self):
        s = str(self.file)
        return s[:s.rfind('/')]


class Persone(models.Model):
    CHOICES = [
        (1, 'Man'),
        (2, 'Woman')
    ]
    firstname  = models.CharField(max_length=255, **bnt)
    lastname   = models.CharField(max_length=255, **bnt)
    telephone  = models.CharField(max_length=20,  **bnt)
    old        = models.PositiveSmallIntegerField(**bnt)
    male       = models.PositiveSmallIntegerField(choices=CHOICES, **bnt)
    adres      = models.CharField(max_length=255, **bnt)
    email      = models.EmailField(**bnt)
    imei       = models.CharField(max_length=255, **bnt)
    interfaces = models.ManyToManyField(Interface)
    group      = models.ForeignKey('Group', on_delete=models.CASCADE, **bnt)

    def __str__(self):
        return '%s %s' % (self.firstname, self.lastname)

    def get_male(self):
        if self.male == 1: return 'Man'
        elif self.male == 2: return 'Weman'
        else: return 'no male'


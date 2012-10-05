#! /usr/bin/env python
import pickle

from libsams import Addressbook, Receiver
from os import environ
from rsa import PublicKey, PrivateKey
from datetime import datetime

dt = datetime(2012, 10, 05, 00, 00, 00)
home = environ.get('HOME')
user = environ.get('USER')
last_receive = '{home}/.sams/messages/last'.format(home=home)
try:
    with open(last_receive, 'rw') as last:
        dt = pickle.load(last)
except:
    dt = datetime(1990, 1, 1, 00, 00)

addressbookfile = '{home}/.sams/addressbook.csv'.format(home=home)
addressbook = Addressbook(addressbookfile)
my_address = addressbook.get_by_name(user)
n = int(my_address['n'])
e = int(my_address['e'])
pubkey = PublicKey(n, e)

privatefile = '{home}/.sams/private.pem'.format(home=home)
with open(privatefile, 'r') as privatefile:
    keydata = privatefile.read()
privkey = PrivateKey.load_pkcs1(keydata)

receiver = Receiver(privkey, pubkey)
messages = receiver(dt)

print 'You have {new} new Messages!'.format(new=len(messages))

for message in messages:
    sender = message['author']
    msg = message['msg']
    date = message['date']
    date = ('{day:02d}.{month:02d}.{year}'
            '{hour:02d}:{minute:02d}').format(day=date.day, month=date.month,
                                              year=date.year,
                                              hour=date.hour,
                                              minute=date.minute)

    uri = '{home}/.sams/messages/{sender}.txt'.format(home=home,
                                                      sender=sender)
    with open(uri, 'a') as file:
        file.write(date + '\n')
        file.write(msg)
        file.write('#' * 10 + '\n')

last_receive = '{home}/.sams/messages/last'.format(home=home)
with open(last_receive, 'w') as last:
    pickle.dump(now, last)

#! /usr/bin/env python

import os

from libsams import Addressbook, Receiver
from os import environ
from rsa import PublicKey, PrivateKey
from datetime import datetime

# prepare environment
home = environ.get('HOME')
user = environ.get('USER')
os.chdir('{home}/.sams/'.format(home=home))

# get pubkey
addressbook = Addressbook('addressbook.csv')
own_address = addressbook.get_by_name(user)
n = int(own_address['n'])
e = int(own_address['e'])
pubkey = PublicKey(n, e)

# get privkey
with open('private.pem', 'r') as privatefile:
    keydata = privatefile.read()
privkey = PrivateKey.load_pkcs1(keydata)

# receive messages
receiver = Receiver(privkey, pubkey)
mtime = 0
files = os.listdir('messages/')
for file in files:
    filestat = os.stat('messages/{file}'.format(file=file))
    if filestat.st_mtime > mtime:
        mtime = filestat.st_mtime
if mtime:
    dt = datetime.utcfromtimestamp(mtime)
    messages = receiver(dt)
else:
    messages = receiver()

# output result
print 'You have {new} new Messages!'.format(new=len(messages))

# save messages to conversation files
for message in messages:
    author = message['author']
    msg = message['msg']
    date = message['date']
    date_str = date.strftime("%A, %d. %B %Y %I:%M%p")
    file = 'messages/{author}.txt'.format(author=author)
    
    with open(file, 'a') as file:
        message = ("{date}\n"
                   "{message}\n"
                   "##########\n").format(date=date_str, message=msg)
        file.write(message)

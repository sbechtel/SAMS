#! /usr/bin/env python

from libsams import Addressbook, Receiver
from os import environ
from rsa import PublicKey, PrivateKey
from datetime import datetime

dt = datetime(2012, 10, 05, 00, 00, 00)
home = environ.get('HOME')
user = environ.get('USER')
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
print messages

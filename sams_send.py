#! /usr/bin/env python

import sys
import os

from libsams import Addressbook, Sender
from rsa import PublicKey

message = sys.stdin.read()
receiver_name = sys.argv[1]

home = os.environ.get('HOME')
uri = '{home}/.sams/addressbook.csv'.format(home=home)

addressbook = Addressbook(uri)
receiver = addressbook.get_by_name(receiver_name)

n = int(receiver['n'])
e = int(receiver['e'])
pubkey = PublicKey(n, e)

sender = Sender(pubkey)

sender(message)
print "Message successfully send!"

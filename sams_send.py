#! /usr/bin/env python

import sys
import os

from libsams import Addressbook, Sender
from rsa import PublicKey

message = sys.stdin.read()

try:
    receiver_name = sys.argv[1]
except IndexError:
    sys.exit('usage: {command} receiver\n'.format(command=sys.argv[0]))

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

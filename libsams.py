import csv
import rsa

from os import environ
from datetime import datetime
from Crypto import Random
from Crypto.Cipher import ARC4
from rsa import PublicKey, PrivateKey
from pymongo import Connection
from bson.binary import Binary

home = environ.get('HOME')
user = environ.get('USER')
host = environ.get('SAMS_HOST')
port = int(environ.get('SAMS_PORT'))


class Addressbook(object):
    """Represent Addressbook."""

    def __init__(self, uri):
        """Init addressbook with file."""
        self.uri = uri
        addresses = []
        with open(uri, 'r') as addressbook:
            reader = csv.DictReader(addressbook)
            for address in reader:
                addresses.append(address)
        self.addresses = addresses

    def get_all(self):
        """Return all addresses in addressbook."""
        return self.addresses

    def get_by_name(self, name):
        """Return address by name."""
        for address in self.addresses:
            if address['name'] == name:
                return address

    def put(self, address):
        """Put address in addressbook and write."""
        self.addresses.append(address)
        with open(self.uri, 'a') as addressbook:
            writer = csv.DictWriter(addressbook, ['name', 'n', 'e'])
            writer.writerow(address)


class Sender(object):
    """Represents Sender."""

    def __init__(self, pubkey):
        """Init Sender with pubkey."""
        self.pubkey = pubkey
        self.key = Random.get_random_bytes(16)
        self.connection = Connection(host, port, tz_aware=True)
        self.pubkey_ident = '{n}.{e}'.format(n=self.pubkey.n, e=self.pubkey.e)

    def __call__(self, msg):
        """Send message."""
        arc4 = ARC4.new(self.key)
        user_crypto = arc4.encrypt(user)
        msg_crypto = arc4.encrypt(msg)
        key_crypto = rsa.encrypt(self.key, self.pubkey)
        user_crypto_bin = Binary(user_crypto)
        msg_crypto_bin = Binary(msg_crypto)
        key_crypto_bin = Binary(key_crypto)
        doc = dict(author=user_crypto_bin, to=self.pubkey_ident,
                   date=datetime.now(), msg=msg_crypto_bin, key=key_crypto_bin)
        collection = self.connection.sams.messages
        collection.insert(doc)


class Receiver(object):
    """Represents Receiver."""

    def __init__(self, privkey, pubkey):
        """Init Receiver with privkey."""
        self.privkey = privkey
        self.pubkey = pubkey
        self.connection = Connection(host, port, tz_aware=True)

    def __call__(self, since=None):
        """Receive messages since datetime."""
        collection = self.connection.sams.messages
        pubkey_ident = '{n}.{e}'.format(n=self.pubkey.n, e=self.pubkey.e)
        query = {'to': pubkey_ident}
        # neccessary for the first receive
        if not since is None:
            query['date'] = {'$gte': since}
        cursor = collection.find(query).sort('date')
        messages = []
        for doc in cursor:
            key = rsa.decrypt(doc['key'], self.privkey)
            arc4 = ARC4.new(key)
            author = arc4.decrypt(doc['author'])
            date = doc['date']
            msg = arc4.decrypt(doc['msg'])
            message = dict(author=author, date=date, msg=msg)
            messages.append(message)
        return messages

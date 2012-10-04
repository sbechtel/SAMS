import csv
import rsa

from os import environ
from Crypto import Random
from Crypto.Cipher import ARC4
from rsa import PublicKey, PrivateKey
from pymongo import Connection
from bson.binary import Binary

home = environ.get('HOME')
host = environ.get('SAMS_HOST')
port = environ.get('SAMS_PORT')

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


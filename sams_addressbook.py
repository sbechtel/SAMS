#! /usr/bin/env python

import libsams
from sys import argv
from os import environ

argument = argv[1]
params = argv[2:]

uri = '{home}/.sams/addressbook.csv'.format(home=environ.get('HOME'))

addressbook = libsams.Addressbook(uri)

if argument == 'all':
    addresses = addressbook.get_all()
    for address in addresses:
        print 'Name: {name} \nN: {n} \nE: {e}'.format(name=address['name'],
                                                      n=address['n'],
                                                      e=address['e'])
        print '*' * 10

elif argument == 'add':
    name, n, e = tuple(params)
    address = dict(name=name, n=n, e=e)
    addressbook.put(address)

elif argument == 'show':
    address = addressbook.get_by_name(argument)
    print 'Name: {name} \nN: {n} \nE: {e}'.format(name=address['name'],
                                                  n=address['n'],
                                                  e=address['e'])

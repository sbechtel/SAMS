import rsa, os, csv

pub, priv = rsa.newkeys(512)

home = os.environ.get('HOME')
addressbook = '{home}/.sams/addressbook.csv'.format(home=home)
privatefile = '{home}/.sams/private.pem'.format(home=home)
user = os.environ.get('USER')

with open(addressbook, 'a') as addressbook:
    writer = csv.writer(addressbook)
    writer.writerow(['name', 'n', 'e'])
    writer.writerow([user, pub.n, pub.e])

with open(privatefile, 'w') as privatefile:
    keydata = priv.save_pkcs1()
    privatefile.write(keydata)

print 'Your public key is n={n} and e={e}!\n'.format(n=pub.n, e=pub.e)

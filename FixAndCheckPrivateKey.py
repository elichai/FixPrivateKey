__author__ = 'elichai2'

import bitcoin
import bitcoin.base58
import hashlib
import string
import argparse


def check(key):
    a = key
    keyH = bitcoin.base58.decode(key)
    check = keyH[-4:]
    keyH = keyH[:-4]
    sha = hashlib.sha256(hashlib.sha256(keyH).digest()).digest()
    if check == sha[:4]:
        print 'Yay!'
        return True
    return False


def change_letter(s):
    if len(s) != 51:
        return 'The address is too long\short'
    address = list(s)
    possible = string.lowercase + string.uppercase + '123456789'
    possible = possible.translate(None, 'OIl')
    for i in range(1, len(address)):
        for c in possible:
            addressN = list(address)
            addressN[i] = c
            addressE = "".join(addressN)
            if check(addressE):
                return addressE
    return 'None Find'

parser = argparse.ArgumentParser(description="Replace every letter in the private key and check if it's right"
                                            ". supports WIF private key only")
parser.add_argument('address', help='The WIF address', type=str)
args = parser.parse_args()
print change_letter(args.address)
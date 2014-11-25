__author__ = 'elichai2'

import bitcoin
import bitcoin.base58
import hashlib
import string
import argparse

possible = string.lowercase + string.uppercase + '123456789'
possible = possible.translate(None, 'OIl')
result = []


def check(key):
    key_decoded = bitcoin.base58.decode(key)
    check = key_decoded[-4:]
    key_decoded = key_decoded[:-4]
    sha = hashlib.sha256(hashlib.sha256(key_decoded).digest()).digest()
    if check == sha[:4]:
        return True
    return False


def change_letter(address, letters, start):
    if 52 < len(address) < 51:
        return 'The address is too long\short'
    if check(address):
        return address
    address_list = list(address)
    for i in range(start, len(address_list)):
        for c in possible:
            address_temp = list(address_list)
            address_temp[i] = c
            address_end = "".join(address_temp)
            # print address_end + " " + str(letters)
            if check(address_end):
                if args.results == 1:
                    return address_end
                result.append(address_end)
                print '\n' + address_end
                args.results -= 1
            if letters > 1:
                if len(change_letter(address_end, letters - 1, start + 1)) == 51:
                    return address_end
    if not result:
        return '\nCouldn\'t find any result'
    return result

parser = argparse.ArgumentParser(description="Replace every letter in the private key and check if it's right"
                                             ". supports WIF private key only")
parser.add_argument('address', type=str,
                    help='The WIF address')
parser.add_argument('-l', '--letters', action='store', type=int,
                    default=1,
                    dest='letters',
                    help='Specify the number of letters to replace')
parser.add_argument('--results', action='store', type=int,
                    default=1,
                    dest='results',
                    help="Specify number of results")
args = parser.parse_args()

print change_letter(args.address, args.letters, 1)

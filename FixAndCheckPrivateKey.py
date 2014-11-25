__author__ = 'elichai2'

import bitcoin
import bitcoin.base58
import hashlib
import string
import argparse
import logging

possible = string.lowercase + string.uppercase + '123456789'
possible = possible.translate(None, 'OIl')
result = []
chk = False


def query_yes_no(question, true='yes', false='no'):
    while True:
        print (question + ' [' + true[0] + '/' + false[0] + ']'),
        choice = raw_input().lower()
        if choice in (true, true[0]):
            return True
        if choice in (false, false[0]):
            return False
        else:
            print "Please respond with '" + true + "' or '" + false +\
                  "' (or '" + true[0] + "' or '" + false[0] + "').\n"


def check_duplicated_letters(address):
    count = 0
    retn = None
    address_list = list(address)
    for i in range(1, len(address_list)):
        if address_list[i] == address_list[i - 1]:
            count += 1
            if count > 1:
                return None
            retn = i

    return retn


def check(key):
    key_decoded = bitcoin.base58.decode(key)
    check = key_decoded[-4:]
    key_decoded = key_decoded[:-4]
    sha = hashlib.sha256(hashlib.sha256(key_decoded).digest()).digest()
    if check == sha[:4]:
        return True
    return False


def change_letter(address, letters=1, start=1):
    global chk
    address_list = list(address)
    if address[0] in ('L', 'K'):  # Compressed Key - supposed to be 52 bytes.
        if not chk:
            logging.info("detected Compressed private key")
            chk = True

        if len(address) == 53:
            indx = check_duplicated_letters(address)
            if indx is not None:
                if query_yes_no("Your privkey is 1 char too long, remove duplicated letters"
                                " or remove last letter?", "repeat", "last"):
                    address_list.pop(indx)
                    logging.info("".join(address_list))
                else:
                    return "Canceled by user"
            elif not query_yes_no("Your privkey is 1 char too long, do you want to remove the last one?"):
                return "Canceled by user"

        elif len(address) == 51:
            if not query_yes_no("Your privkey is 1 char short, do you want to try generate the last one?"):
                return "Canceled by user"

    elif not 50 >= len(address) >= 52:
        logging.info("the address is " + len(address) + " bytes long")
        return 'The address is too long\short'

    else:  # Not compressed key - supposed to be 51 bytes.
        if len(address) == 52:
            if not query_yes_no("Your privkey is 1 char too long, do you want to remove the last one?"):
                return "Canceled by user"
            else:
                address_list.pop()
                logging.info("removed last char, new privkey: " + address)
        if len(address) == 50:
            if not query_yes_no("Your privkey is 1 char short, do you want to try generate the last one?"):
                return "Canceled by user"
            address += '1'
            logging.info("added char to the end(it will try generating it), new privkey: " + address)

    if check(address):
        logging.info("The address was 100% right")
        return address

    for i in range(start, len(address_list)):
        for c in possible:
            address_temp = list(address_list)
            address_temp[i] = c
            address_end = "".join(address_temp)
            logging.debug("Checking this address: " + address_end)
            if check(address_end):
                if args.results == 1:
                    return address_end
                result.append(address_end)
                print '\n' + address_end
                args.results -= 1
            if letters > 1:
                if 53 > len(change_letter(address_end, letters - 1, start + 1)) > 50:
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
parser.add_argument('-v', action='count',
                    dest='verbose',
                    help='Verbose - use `-v` for level 1 and `-vv` for level 2')
args = parser.parse_args()

if args.verbose == 1:
    logging.basicConfig(level=logging.INFO)
elif args.verbose >= 2:
    logging.basicConfig(level=logging.DEBUG)

print change_letter(args.address, args.letters, 1)
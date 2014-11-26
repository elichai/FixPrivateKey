__author__ = 'elichai2'

import bitcoin
import bitcoin.base58
import hashlib
import string
import argparse
import logging
import sys

possible = string.lowercase + string.uppercase + '123456789'
possible = possible.translate(None, 'OIl')
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


def swap_letters(privkey):
    privkey_list = list(privkey)
    for i in range(1, len(privkey_list) - 1):
        privkey_tmp = list(privkey_list)
        tmp = privkey_tmp[i + 1]
        privkey_tmp[i + 1] = privkey_tmp[i]
        privkey_tmp[i] = tmp
        logging.debug("Swap test: " + "".join(privkey_tmp))
        if check("".join(privkey_tmp)):
            return "".join(privkey_tmp)
    return None


def check_duplicated_letters(privkey):
    count = 0
    retrn = None
    privkey_list = list(privkey)
    for i in range(1, len(privkey_list)):
        if privkey_list[i] == privkey_list[i - 1]:
            count += 1
            if count > 1:
                return None
            retrn = i
    return retrn


def check(key):
    key_decoded = bitcoin.base58.decode(key)
    check = key_decoded[-4:]
    key_decoded = key_decoded[:-4]
    sha = hashlib.sha256(hashlib.sha256(key_decoded).digest()).digest()
    if check == sha[:4]:
        return True
    return False


def change_letter(privkey, letters=1, start=1):
    global chk
    privkey_list = list(privkey)
    if privkey[0] in ('L', 'K'):  # Compressed Key - supposed to be 52 bytes.
        if not chk:
            logging.info("detected Compressed private key")
            chk = True

        if len(privkey) == 53:
            indx = check_duplicated_letters(privkey)
            if indx is not None:
                if query_yes_no("Your privkey is 1 char too long, remove duplicated letters"
                                " or remove last letter?", "repeat", "last"):
                    privkey_list.pop(indx)
                    logging.info("".join(privkey_list))
                else:
                    return "Canceled by user"
            elif not query_yes_no("Your privkey is 1 char too long,"
                                  " do you want to remove the last one?"):
                return "Canceled by user"

        elif len(privkey) == 51:
            if not query_yes_no("Your privkey is 1 char short,"
                                " do you want to try generate the last one?"):
                return "Canceled by user"

    elif len(privkey) >= 52 or len(privkey) <= 50:
        logging.info("the private key is " + str(len(privkey)) + " bytes long")
        return 'The private key is too long\short'

    else:  # Not compressed key - supposed to be 51 bytes.
        if len(privkey) == 52:
            if not query_yes_no("Your privkey is 1 char too long,"
                                " do you want to remove the last one?"):
                return "Canceled by user"
            else:
                privkey_list.pop()
                logging.info("removed last char, new privkey: " + privkey)
        if len(privkey) == 50:
            if not query_yes_no("Your privkey is 1 char short,"
                                " do you want to try generate the last one?"):
                return "Canceled by user"
            privkey += '1'
            logging.info("added char to the end(it will try generating it),"
                         " new privkey: " + privkey)

    if check(privkey):
        logging.info("The Private Key was 100% right")
        return privkey
    
    result = []
    for i in range(start, len(privkey_list)):
        for c in possible:
            privkey_temp = list(privkey_list)
            privkey_temp[i] = c
            privkey_end = "".join(privkey_temp)
            logging.debug("Checking this privkey: " + privkey_end)
            if check(privkey_end):
                if args.results == 1:
                    return privkey_end
                result.append(privkey_end)
                print '\n' + privkey_end
                args.results -= 1
            if letters > 1:
                if 53 > len(change_letter(privkey_end, letters - 1, start + 1)) > 50:
                    return privkey_end
    if not result:
        return '\nCouldn\'t find any result'
    return result

parser = argparse.ArgumentParser(description="Replace every letter in the private key and check if it's right"
                                             ". supports WIF private key only")
parser.add_argument('privkey', type=str,
                    help='The WIF privkey')
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
parser.add_argument('--swap', action='store_true',
                    dest='swap',
                    help='Check if two consecutive letters got misplaced.'
                         ' By swapping any pair of letters in the private key')
args = parser.parse_args()

if args.verbose == 1:
    logging.basicConfig(level=logging.INFO)
elif args.verbose >= 2:
    logging.basicConfig(level=logging.DEBUG)

if args.swap:
    result = swap_letters(args.privkey)
    if result is not None:
        print result
        sys.exit(0)
print change_letter(args.privkey, args.letters, 1)

__author__ = 'elichai2'

import bitcoin
import bitcoin.base58
import hashlib
import string
import argparse
import logging
import sys

b58_digits = string.lowercase + string.uppercase + '123456789'
b58_digits = b58_digits.translate(None, 'OIl')
comp = 0


def s2l(lisst):
    return "".join(lisst)


def query_yes_no(input_func, question, true='yes', false='no'):
    while True:
        print (question + ' [' + true[0] + '/' + false[0] + ']'),
        choice = input_func().lower()
        if choice in (true, true[0]):
            return True
        if choice in (false, false[0]):
            return False
        else:
            print "Please respond with '" + true + "' or '" + false +\
                  "' (or '" + true[0] + "' or '" + false[0] + "').\n"


def check_length(privkey_list, input_func=raw_input):
    if type(privkey_list) is not list:
        if type(privkey_list) is str:
            privkey_list = list(privkey_list)
        else:
            raise ValueError("This function accept list and string only. not: " + str(privkey_list).__name__)

    comp = 0  # Sign if privkey is compressed.
    if privkey_list[0] in ('L', 'K'):  # Compressed Key - suppose to be 52 bytes. Uncompressed Key - suppose to be 51 bytes.
        logging.info("detected Compressed private key")
        comp = 1
    if len(privkey_list) == (52 + comp):  # if it's compressed key(comp=1) so it'll be 53, 1 byte above normal.
        indx = check_duplicated_letters(privkey_list)
        if indx is not None:
            if query_yes_no(input_func, "Your privkey is 1 char too long, remove duplicated letters"
                            " or remove last letter?", "duplicated", "last"):
                privkey_list.pop(indx)
                logging.info("Removed last char, new privkey:" + "".join(privkey_list))
            else:
                privkey_list.pop()
                logging.info("Removed last char, new privkey:" + "".join(privkey_list))
        elif not query_yes_no(input_func, "Your privkey is 1 char too long,"
                              " do you want to remove the last one?"):
            print "Canceled by user"
            sys.exit(0)
        else:
            privkey_list.pop()
            logging.info("Removed last char, new privkey:" + "".join(privkey_list))

    elif len(privkey_list) == (50 + comp):  # if it's compressed key(comp=1) so it'll be 51, 1 byte above normal.
        if not query_yes_no(input_func, "Your privkey is 1 char short,"
                            " do you want to try generate the last one?"):
            print "Canceled by user"
            sys.exit(0)
        privkey_list.append('1')
        logging.info("added char to the end(it will try generating it),"
                     " new privkey: " + ("".join(privkey_list)))

    elif len(privkey_list) > (52 + comp) or len(privkey_list) < (50 + comp):
        logging.info("the private key is " + str(len(privkey_list)) + " bytes long")
        print 'The private key is too long\short'
        sys.exit(0)
    return privkey_list


def swap_letters(privkey):
    if check(privkey):
        return privkey
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


def check_duplicated_letters(privkey_list):
    count = 0
    retrn = None
    for i in range(1, len(privkey_list)):
        if privkey_list[i] == privkey_list[i - 1]:
            count += 1
            if count > 1:
                return None
            retrn = i
    return retrn


def check(key):
    try:
        key_decoded = bitcoin.base58.decode(key)
    except Exception, e:
        logging.info("Check privkey error:" + str(e))
        return False
    check = key_decoded[-4:]
    key_decoded = key_decoded[:-4]
    sha = hashlib.sha256(hashlib.sha256(key_decoded).digest()).digest()
    if check == sha[:4]:
        return True
    return False


def change_letter(privkey_list, letters=1, results=1, start=1):
    if type(privkey_list) is not list:
        if type(privkey_list) is str:
            privkey_list = list(privkey_list)
        else:
            raise ValueError("This function accept list and string only, not: " + type(privkey_list).__name__)

    if check("".join(privkey_list)):
        logging.info("The Private Key was 100% right")
        return "".join(privkey_list)

    result = []
    for i in range(start, len(privkey_list)):
        if privkey_list[i] not in b58_digits:
            privkey_list[i] = '1'
        for c in b58_digits:
            privkey_temp = list(privkey_list)
            privkey_temp[i] = c
            privkey_end = "".join(privkey_temp)
            logging.debug("Checking this privkey: " + privkey_end)
            if check(privkey_end):
                if results == 1:
                    return privkey_end
                result.append(privkey_end)
                print '\n' + privkey_end
                results -= 1
            if letters > 1:
                privkey_end = change_letter(privkey_end, letters - 1, results, start + 1)
                if 53 > len(privkey_end) > 50:
                    return privkey_end
    if not result:
        return '\nCouldn\'t find any result'
    return result


def main():
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
    print change_letter(check_length(list(args.privkey)), args.letters, args.results)

if __name__ == '__main__':
    main()
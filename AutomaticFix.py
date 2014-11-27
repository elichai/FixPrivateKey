__author__ = 'elichai2'
import FixPrivateKey
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="Tries a lot of automatic fix's, swapping letters,"
                                                 " checking length, changing up to 5 letters"
                                                 ". supports WIF private key only")
    parser.add_argument('privkey', type=str,
                        help='The WIF privkey')
    args = parser.parse_args()

    # check the length
    privkey = FixPrivateKey.check_length(privkey)

    # check if right
    privkey = args.privkey
    if FixPrivateKey.check(privkey):
        print privkey
        sys.exit(0)

    # check if letters swapped
    result = FixPrivateKey.swap_letters(privkey)
    if result is not None:
        print result
        sys.exit(0)

    # try changing 1 to 5 letters
    for i in range(1, 5):
        result = FixPrivateKey.check_length(privkey, i)
        if result != '\nCouldn\'t find any result':
            print result
            break

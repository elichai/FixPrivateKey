FixPrivateKey
=============

This tool is used to replace every single character in a WIF private key, and then check if the checksum is correct.
To use this tool you must install Peter Todd's `python-bitcoinlib` library.
Usage
----------------
```
$ python FixPrivateKey.py <address>
```
You can add `--letters LETTERS` option to try replacing more than 1 letter.
And you can add `--results RESULTS` option to stop trying after more than 1 letter.

If you don't succeed or you don't know how many letters you miswrote or if the letters may be swapped, you can try the automatic script:
```
$ python AutomaticFix.py <address>
```
This will try swapping and replacing up to 5 letters. but it will take a lot of time.
Install Peter Todd's library
----------------
```
sudo apt-get install libssl-dev
python setup.py build
python setup.py install
```

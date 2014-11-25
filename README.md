FixPrivateKey
=============

This tool is used to replace every single character in a WIF private key, and then check if the checksum is correct.
To use this tool you must install Petter Todd's `python-bitcoinlib` library.
Usage
----------------
```
$ python FixAndCheckPrivateKey.py <address>
```
You can add `--letters LETTERS` option to try replacing more than 1 letter.
And you can add `--results RESULTS` option to stop trying after more than 1 letter.
Install Peter Todd's library
----------------
```
sudo apt-get install libssl-dev
python setup.py build
python setup.py install
```

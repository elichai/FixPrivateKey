FixPrivateKey
=============

This tool is used to replace every single character in a WIF private key, and then check if the checksum is correct.<br>
To use this tool you must install Peter Todd's `python-bitcoinlib` library.
Usage
----------------
```
$ python FixPrivateKey.py <privkey>
```
You can add `--letters LETTERS` option to try replacing more than 1 letter.<br>
You can also add `--swap` to Check if two consecutive letters got misplaced.<br>
And you can add `--results RESULTS` option to stop trying after more than 1 result.


If you don't succeed or you don't know how many letters you miswrote or if the letters may be swapped, you can try the automatic script:
```
$ python AutomaticFix.py <privkey>
```
This will try swapping and replacing up to 5 letters. but it will take a lot of time.
Install Peter Todd's library
----------------
```
sudo apt-get install libssl-dev
sudo pip install python-bitcoinlib
```

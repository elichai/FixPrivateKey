FixPrivateKey
=============

This tool is used to replace every single character in a WIF private key, and then check if the checksum is correct.
To use this tool you must install Petter Todd's `python-bitcoinlib` library.
Usage
----------------
```
$ python FixAndCheckPrivateKey.py address
```

Install Petter Todd's library
----------------
```
sudo apt-get install libssl-dev
python setup.py build
python setup.py install
```

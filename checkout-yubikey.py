#!/usr/bin/python

###
#
# checkout-yubikey.py
#
# Troy Axthelm
# Advanced Research Computing Center
# University of Wyoming
# troy.axthelm@uwyo.edu
#
# Created: 13 June 2016
#
#
# Modified: <initials> <day> <month> <year> <change notes>
#
###

import sys
sys.path.insert(0, './lib/')
import logging
import subprocess
import idm_manage
import argparse

__version__='1.0'

# argparser and auto generate help

# checkout-yubikey usage
usage = "%(prog)s <username> <yubikeyid>"

parser = argparse.ArgumentParser(prog='checkout-yubikey.py', usage=usage,
                    description='Checkout a yubikey to an IDM user')

parser.set_defaults()

# version
parser.add_argument('--version', action='version', version="%(prog)s "+__version__)
parser.add_argument('username', nargs='+')
parser.add_argument('yubikeyid', nargs='+')

# create parser
args = parser.parse_args()

print args

#issue ipa command
idm_manage.addyubikey(args.username[0], args.yubikeyid[0])

#!/usr/bin/python
###
# get-ad-status.py
#
# To show attributes of AD users
#
# Troy Axthelm
# Advanced Research Computing Center
# University of Wyoming
# troy.axthelm@uwyo.edu
#
# Created: 4 May 2016
#
# Modified: <initials> <year>.<month>.<day> <change notes>
# KM  2017.09.05 Added usage comment. Edited text to apply to this program
#                (instead of update-idm-user) - could still remove irrelevant
#                options rather than just noting them.
###

# To show attributes of AD users, run:
#
#	./get-ad-status.py <usernames>
#
# where <usernames> is a list of one or more (space-separated) usernames.
# If a password file isn't set up, will prompt for username and password to 
# login to AD. Connecting as yourself (i.e. a regular user, not admin/special) 
# should work as read-only access to AD is needed. 

import sys
sys.path.insert(0, './lib/')
import argparse
import logging
import user_add
import ldap_tools
import idm_manage

__version__='1.0'

# argparser and auto generate help

# add-idm-user usage
usage = "%(prog)s [<username>] [options]"

parser = argparse.ArgumentParser(prog='get-ad-status.py', usage=usage,
                    description='Display user attributes from windows.uwyo.edu')

# version
parser.add_argument('--version', action='version', version="%(prog)s "+__version__)

# default arg values
parser.set_defaults(verbose=True,logfile="idm-actions.log", dry=False, confirm=True, uid=False)

# args
parser.add_argument(  "-v","--verbose", action="store_true", dest="verbose", 
                    help="print status messages to stdout")
parser.add_argument(  "-n", "--dry-run", action="store_true", dest="dry",
                    help="no effect as this program doesn't make any updates")
parser.add_argument(  "-l", "--logfile", dest="logfile", 
                    help="change logfile location")
parser.add_argument(  "-y", "--no-confirm", action="store_false", dest="confirm", 
                    help="no effect as this program doesn't make any updates")
parser.add_argument(  "--uid", action="store_true", dest="uid", 
                    help="update the users uid")
parser.add_argument(  'usernames', nargs='*')

# create parser
args = parser.parse_args()

logging.basicConfig(format='%(asctime)s :: %(message)s', level=logging.CRITICAL)
logging.info("START")
logging.debug(args)

dstring =""
if args.dry == True:
	dstring = "--dry-run selected, has no effect\n"

userattrs = []
notfound = []
# pull user attributes from AD with ldap query
for user in args.usernames:
	sres = ldap_tools.ldapsearch(user, 'bash')
	if sres != 'NOUSER':	
		userattrs.append(sres)
	else:
		notfound.append(user)

print userattrs

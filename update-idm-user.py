#!/usr/bin/python

###
#
# update-idm-user.py
#
# Troy Axthelm
# Advanced Research Computing Center
# University of Wyoming
# troy.axthelm@uwyo.edu
#
# Created: 16 February 2016
#
#
# Modified: <initials> <day> <month> <year> <change notes>
#
###

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

parser = argparse.ArgumentParser(prog='update-idm-user.py', usage=usage,
                    description='Update idm users with attributes from windows.uwyo.edu')

# version
parser.add_argument('--version', action='version', version="%(prog)s "+__version__)

# default arg values
parser.set_defaults(verbose=True,logfile="idm-actions.log", dry=False, confirm=True, uid=False)

# args
parser.add_argument(  "-v","--verbose", action="store_true", dest="verbose", 
                    help="print status messages to stdout")
parser.add_argument(  "-n", "--dry-run", action="store_true", dest="dry",
                    help="run but do not add users to idm")
parser.add_argument(  "-l", "--logfile", dest="logfile", 
                    help="change logfile location")
parser.add_argument(  "-y", "--no-confirm", action="store_false", dest="confirm", 
                    help="do not confirm user attributes after ldap search")
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
	dstring = "--dry-run selected, no changes will be made to idm regardless of confirmation!\n"

userattrs = []
# pull user attributes from AD with ldap query
for user in args.usernames:
	sres = ldap_tools.ldapsearch(user, 'bash')
	if sres != 'NOUSER':	
		userattrs.append(sres)
	else:
		print "error, user %s not found\n" %user

# The update list will be of tuples [<username>,"<attrs_to_update>"]
update_list = []

for user in userattrs:
	modstring = ""
	if args.uid == True:
		modstring = modstring + "--uid %s --gidnumber %s " % (user[5], user[6])
	
	update_list.append([user[0], modstring])

# if not a dry run, modify user attributes
if args.dry == False:
	idm_manage.updateidmusers(update_list)
# if it is a dry run, print the ipa command that would have run
if args.dry == True:
	idm_manage.printupdateidmusers(update_list)

	








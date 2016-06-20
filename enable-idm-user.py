#!/usr/bin/python

###
#
# enable-idm-user.py
#
# Troy Axthelm
# Advanced Research Computing Center
# University of Wyoming
# troy.axthelm@uwyo.edu
#
# Created: 16 June 2016
#
#
# Modified: <initials> <day> <month> <year> <change notes>
#
###

import sys
sys.path.insert(0, '/root/idm-management-tools/lib/')
import argparse
import logging
import user_add
import ldap_tools
import idm_manage

__version__='1.0'

# argparser and auto generate help

# enable-idm-user usage
usage = "%(prog)s [<username>]* [options]"

parser = argparse.ArgumentParser(prog='enable-idm-user.py', usage=usage,
                    description='disable idm users')

# version
parser.add_argument('--version', action='version', version="%(prog)s "+__version__)

# default arg values
parser.set_defaults(verbose=True,logfile="idm-actions.log", dry=False, defShell='bash', manual=False, confirm=True, uid=False, manid=False)

# args
parser.add_argument(  "-f", "--file", dest="filename", 
                    metavar="FILE", help="add users from FILE")
parser.add_argument(  "-s", "--shell", dest="defShell", 
                    metavar="SHELL", help="override default shell for added users \
                    valid shell options: bash, dash, tcsh")
parser.add_argument(  "-v","--verbose", action="store_true", dest="verbose", 
                    help="print status messages to stdout")
parser.add_argument(  "-q", "--quiet", action="store_false", dest="verbose", 
                    help="don't print status messages to stdout")
parser.add_argument(  "-n", "--dry-run", action="store_true", dest="dry",
                    help="run but do not add users to idm")
parser.add_argument(  "-l", "--logfile", dest="logfile", 
                    help="change logfile location")
parser.add_argument(  "-i", "--uid", action="store_true", dest="uid", 
                    help="only get user numeric id from active directory")
parser.add_argument(  "--manual-id", action="store_true", dest="manid", 
                    help="manually add the uid, must have username field in form <username>%<uid>")
parser.add_argument(  "-y", "--no-confirm", action="store_false", dest="confirm", 
                    help="do not confirm user attributes after ldap search")
parser.add_argument(  "--manual-add", action="store_true", dest="manual", 
                    help="manually add user not in AD (be careful)")
parser.add_argument(  'usernames', nargs='*')

# create parser
args = parser.parse_args()

logging.basicConfig(format='%(asctime)s :: %(message)s', level=logging.CRITICAL)
logging.info("START")
logging.debug(args)

dstring =""
if args.dry == True:
	dstring = "--dry-run selected, no changes will be made to idm regardless of confirmation!\n"



# import users from file if set
if args.filename != None: 
    args.usernames = args.usernames + user_add.readusers(args.filename)

users = []
# cleanup the usernames
for user in args.usernames:
	users.append(user.strip('\n'))
# if not a dry run, disable users in idm
if args.dry == False:
	idm_manage.enableidmusers(users)	
	print ("all users enabled in idm")

# otherwise, just print what the output would be
else:
	idm_manage.printenableidmusers(users)
	print ("no users enabled in idm, above is what would have be executed\n\n")
	

#!/usr/bin/python

###
#
# add-idm-user.py
#
# Troy Axthelm
# Advanced Research Computing Center
# University of Wyoming
# troy.axthelm@uwyo.edu
#
# Created: 14 October 2015
#
#
# Modified: <initials> <day> <month> <year> <change notes>
#
###

import argparse
import logging
import user_add
import ldap_tools
import idm_manage

__version__='1.0'

# argparser and auto generate help

# add-idm-user usage
usage = "%(prog)s [<username>[:<shell>] ]* [options]"

parser = argparse.ArgumentParser(prog='add-idm-user.py', usage=usage,
                    description='Add users to idm with attributes from windows.uwyo.edu')

# version
parser.add_argument('--version', action='version', version="%(prog)s "+__version__)

# default arg values
parser.set_defaults(verbose=True,logfile="idm-actions.log", dry=False, defShell='bash', manual=False, confirm=True)

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
parser.add_argument(  "-n", "--dry-run", action="store_true", dest="dryRun",
                    help="run but do not add users to idm")
parser.add_argument(  "-l", "--logfile", dest="logfile", 
                    help="change logfile location")
parser.add_argument(  "-y", "--no-confirm", action="store_false", dest="confirm", 
                    help="do not confirm user attributes after ldap search")
parser.add_argument(  "--manual-add", action="store_true", dest="manual", 
                    help="manually add user not in AD (be careful)")
parser.add_argument(  'usernames', nargs='*')

# create parser
args = parser.parse_args()

logging.basicConfig(format='%(asctime)s :: %(message)s', level=logging.DEBUG)
logging.info("START")
logging.debug(args)

# if --manual-add, begin interactive process to add IDM user
if args.manual==True:
    user_add.manualadd()

# verify default shell
args.defShell = args.defShell.lower()
logging.debug("validating default shell option")
if args.defShell=='bash' or args.defShell=='dash' or args.defShell=='tcsh':
    logging.debug("default shell (" + args.defShell + ") valid")
else:
    logging.warning("invalid default shell (" + args.defShell + ") default shell set to bash")
    args.defShell='bash'

# import users from file if set
if args.filename != None: 
    args.usernames = args.usernames + user_add.readusers(args.filename)
    
# verify user args and shell option
logging.info("validating shell options...")
logging.debug(args.usernames)

# if not entering users manually...
if args.manual == False:
	# validate and correct user shell options if manual not selected
    	args.usernames = user_add.validateshell(args.usernames, args.defShell)
	logging.debug(args.usernames)
	print args.usernames

	attrs=[]
	
	# find user ldap entries
	for uname in args.usernames:
		uname = uname.split(':')
		attrs.append(ldap_tools.ldapsearch(uname[0],uname[1]))
	print attrs

# if the user would like to confim user attributes
if args.confirm==True:
	# print out user attributes
	print("\nif confirmed, the following user(s) will be added to idm:")

	for users in attrs:
		userattrs=("\nusername:\t%s\nfirstname:\t%s\nlastname:\t%s\ndisplayname:\t%s\nemailAddr:\t%s\nuidnumber:\t%s\ngidnumber:\t%s\nphone:\t\t%s\norgunit:\t%s\n\
title:\t\t%s\nshell:\t\t%s" % (users[0],users[1],users[2],users[3],users[4],users[5],users[6],users[7],users[8],users[9],users[10]))

		print userattrs	

	confirm = raw_input("\nAre you sure you wish to add the above user(s) to idm (y/n)? [n]: ")
	
	# verify the user information is confirmed
	if confirm.lower() != 'y':
		logging.debug("user information not confirmed: %s, abort!" % confirm)
		print "user information not confirmed, no changes have been made to idm"
		exit()

# if not a dry run, add user to idm
if args.dry == False:
	idm_manage.addidmusers(attrs)	

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

# if --manual-add, begin interactive process to add IDM user
if args.manual==True:
    	attrs = []
	attrs.append( user_add.manualadd(dstring) )

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

man_uids = []
# split usernames and uids if manual is set
if args.manid == True:
   for n,uname in enumerate(args.usernames):
	ushell = uname.split(':')
        uname = ushell[0].split('%')
	
	if len(uname) == 2:
		man_uids.append(uname[1])
	else:
		logging.error("error, uid or username not found")
		exit()
	
	if len(ushell) == 2:
		args.usernames[n] =  uname[0] +":"+ ushell[1]
		print args.usernames[n]
	else:
		args.usernames[n] =  uname[0]
		print args.usernames[n]
	
	print uname
 
# if uid option set, get uids and return
if args.uid == True:
	print "[uid]"
	# find user ldap entries and uids
	for uname in args.usernames:
		uname = uname.strip("\n")
		uname = uname.split(':')
		sres = (ldap_tools.ldapgetuid(uname[1]))
		if sres != "NOUSER":
			print uname[0]+"="+sres
		else:
			print uname[0]+"=-1"
	exit()

# verify user args and shell option
logging.info("validating shell options...")
logging.debug(args.usernames)

# if not entering users manually...
if args.manual == False:
	# validate and correct user shell options if manual not selected
    	args.usernames = user_add.validateshell(args.usernames, args.defShell)
	logging.debug(args.usernames)

	attrs=[]
	
	# find user ldap entries
	for uname in args.usernames:
		uname = uname.split(':')
		sres = (ldap_tools.ldapsearch(uname[0],uname[1]))
		
		if sres != "NOUSER":
			attrs.append(sres)
		else:
			if args.manid == True:
				logging.critical("error, user not found and manid enabled...abort")
     				exit()
# if manual ids is on, set input ids
if args.manid == True:
	for n,user in enumerate(attrs):
		attrs[n][5] = man_uids[n]	
		attrs[n][6] = man_uids[n]	
	
	
# if the user would like to confim user attributes
if args.confirm==True and args.manual == False:
	# print out user attributes
	print("\n"+dstring+"if confirmed, the following user(s) will be added to idm (unless --dry-run option specified):")

	for users in attrs:
		userattrs=("\nusername:\t%s\nfirstname:\t%s\nlastname:\t%s\ndisplayname:\t%s\nemailAddr:\t%s\nuidnumber:\t%s\ngidnumber:\t%s\nphone:\t\t%s\norgunit:\t%s\n\
title:\t\t%s\nshell:\t\t%s" % (users[0],users[1],users[2],users[3],users[4],users[5],users[6],users[7],users[8],users[9],users[10]))
		
		print userattrs

	confirm = raw_input("\n"+dstring+"Are you sure you wish to add the above user(s) to idm (y/n)? [n]: ")
	
	# verify the user information is confirmed
	if confirm.lower() != 'y':
		logging.debug("user information not confirmed: %s, abort!" % confirm)
		print "user information not confirmed, no changes have been made to idm"
		exit()


# if not a dry run, add users to idm
if args.dry == False:
	idm_manage.addidmusers(attrs)	
	print ("all users added to idm")

# otherwise, just print what the output would be
else:
	idm_manage.printaddidmusers(attrs)
	print ("no users added to idm, above is what would have be executed\n\n")
	
	

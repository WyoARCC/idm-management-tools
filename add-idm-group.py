#!/usr/bin/python

###
#
# add-idm-group.py
#
# Troy Axthelm
# Advanced Research Computing Center
# University of Wyoming
# troy.axthelm@uwyo.edu
#
# Created: 21 October 2016
#
#
# Modified: <initials> <day> <month> <year> <change notes>
#
###

import argparse
import logging
import idm_manage

__version__='1.0'

# argparser and auto generate help

# add-idm-user usage
usage = "%(prog)s [<groupname>:<gid>[:<Description>] ]* [options]"

parser = argparse.ArgumentParser(prog='add-idm-group.py', usage=usage,
                    description='Add groups (projects) to idm')

# version
parser.add_argument('--version', action='version', version="%(prog)s "+__version__)

# default arg values
parser.set_defaults(verbose=True,logfile="idm-actions.log", dry=False, manual=False, confirm=True)

# args
parser.add_argument(  "-f", "--file", dest="filename", 
                    metavar="FILE", help="add users from FILE")
parser.add_argument(  "-v","--verbose", action="store_true", dest="verbose", 
                    help="print status messages to stdout")
parser.add_argument(  "-q", "--quiet", action="store_false", dest="verbose", 
                    help="don't print status messages to stdout")
parser.add_argument(  "-n", "--dry-run", action="store_true", dest="dry",
                    help="run but do not add users to idm")
parser.add_argument(  "-l", "--logfile", dest="logfile", 
                    help="change logfile location")
parser.add_argument(  "-y", "--no-confirm", action="store_false", dest="confirm", 
                    help="do not confirm user attributes after ldap search")
parser.add_argument(  "--manual-add", action="store_true", dest="manual", 
                    help="manually add user not in AD (be careful)")
parser.add_argument(  'groupnames', nargs='*')

# create parser
args = parser.parse_args()

logging.basicConfig(format='%(asctime)s :: %(message)s', level=logging.CRITICAL)
logging.info("START")
logging.debug(args)

dstring =""
if args.dry == True:
	dstring = "--dry-run selected, no changes will be made to idm regardless of confirmation!\n"

# if --manual-add, begin interactive process to add IDM group

# import groups from file if set
if args.filename != None: 
    args.groupnames = args.groupnames

# add groups in groupnames list
if args.groupnames:
	
	for group in args.groupnames:
		group = group.split(':')
		
		group.append("")
		
		if len(group) != 3:
			print "error not missing group attribute"
	
		print group[0] +" " + group[1] + " " + group[2]
		 
else:
	print "No groups set to be added"



























 

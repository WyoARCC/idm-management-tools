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
# TA 6 May 2016 modified usage to add-idm-group <groupname> <pi_username> [options]
#
###

import argparse
import logging
import idm_manage
import get_group_info as grpinfo

__version__='1.0'

# argparser and auto generate help

# add-idm-group usage
usage = "%(prog)s <groupname> <pi_username> <proj_description>"

parser = argparse.ArgumentParser(prog='add-idm-group.py', usage=usage,
                    description='Add groups (projects) to idm')

# version
parser.add_argument('--version', action='version', version="%(prog)s "+__version__)

# default arg values
parser.set_defaults(verbose=False,logfile="idm-actions.log", dry=False, manual=False, confirm=True)

# args
parser.add_argument(  "-v","--verbose", action="store_true", dest="verbose", 
                    help="print additional status messages to stdout")
parser.add_argument(  "-q", "--quiet", action="store_false", dest="verbose", 
                    help="don't print status messages to stdout")
parser.add_argument(  "-n", "--dry-run", action="store_true", dest="dry",
                    help="run but do not add users to idm")
parser.add_argument(  "-l", "--logfile", dest="logfile", 
                    help="change logfile location")
parser.add_argument(  "-y", "--no-confirm", action="store_false", dest="confirm", 
                    help="do not confirm group attributes")
parser.add_argument(  'groupname', nargs='+')
parser.add_argument(  'piname', nargs='+')
parser.add_argument(  'projdesc', nargs='+')

# create parser
args = parser.parse_args()

loglevel="CRITICAL"
if args.verbose == True:
	loglevel="INFO"

logging.basicConfig(format='%(asctime)s :: %(message)s', level=loglevel)
logging.info("START")
logging.debug(args)

dstring =""
if args.dry == True:
	dstring = "--dry-run selected, no changes will be made to idm regardless of confirmation!\n"

# add the group entries in idm
idm_manage.addidmgroup(args.groupname[0], grpinfo.getNextProj(), args.piname[0], args.projdesc[0])
























 

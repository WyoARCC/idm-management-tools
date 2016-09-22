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
# JDB 2016.09.19 Adding cluster flag, and additional output flags to terminal
#                including VERBOSE, DRYRUN, DEBUG so output on screen is better
#
###

# System Libraries
import sys
import argparse
import logging

# Package Libraries
sys.path.insert(0, './lib/')
import idm_manage
import get_group_info as grpinfo

# Version
__version__='1.0'

# Globals
VERBOSE = False
DRYRUN  = False
DEBUG   = 0

gid_select = 'legacy'


# Usage Statement
#usage = "%(prog)s <groupname> <pi_username> <proj_description>"

# Argument Parser
parser = argparse.ArgumentParser(prog='add-idm-group.py', #usage=usage,
                    description='Add groups (projects) to idm')

# version
parser.add_argument(  "-V","--version", action="version", version="%(prog)s "+__version__)

# Default Argument Values
parser.set_defaults( verbose=False,
                     logfile="idm-actions.log", 
                     dry=False, 
                     manual=False, 
                     confirm=True, 
                     cluster="")

# Optional Arguments
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

parser.add_argument(  "-c", "--cluster", dest="cluster", type=str, 
                    help="specify the cluster, [mountmoran, petalibrary,...]")

# Positional Arguments
parser.add_argument(  'groupname', nargs=1, help="Project group name")
parser.add_argument(  'piname',    nargs=1, help="PI user name for project")
parser.add_argument(  'projdesc',  nargs=1, help="Description of project")

# create parser
args = parser.parse_args()

loglevel="CRITICAL"
if args.verbose:
	loglevel="INFO"
	idm_manage.VERBOSE,VERBOSE = True,True

logging.basicConfig(format='%(asctime)s :: %(message)s', level=loglevel)
#logging.info("START")
logging.debug(args)

dstring =""
if args.dry:
	dstring = "--dry-run selected, no changes will be made to idm regardless of confirmation!\n"
        idm_manage.DRYRUN,DRYRUN = True,True

# add the group entries in idm
gid = {}
#gid['orig'] = grpinfo.getNextProj()
gid['legacy'] = grpinfo.get_next_proj_gid(legacy=True)
gid['best']   = grpinfo.get_next_proj_gid(legacy=False)

idm_manage.addidmgroup( args.groupname[0], 
                        gid[gid_select], 
                        args.piname[0], 
                        args.projdesc[0],
                        args.cluster )

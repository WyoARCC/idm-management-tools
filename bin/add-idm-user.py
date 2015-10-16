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
import idmManAdd

__version__='1.0'

# argparser and auto generate help

# add-idm-user usage
usage = "%(prog)s [<username>[:<shell>] ]* [options]"

parser = argparse.ArgumentParser(prog='add-idm-user.py', usage=usage,
                    description='Add users to idm with attributes from windows.uwyo.edu')

# version
parser.add_argument('--version', action='version', version="%(prog)s "+__version__)

# default arg values
parser.set_defaults(verbose=True,logfile="idm-actions.log", dry=False, defShell='bash', manual=False)

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
    idmManAdd.manualadd()

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
    logging.debug("opening userfile to import users: " + args.filename)
    with open(args.filename) as userfile:
        usernames = userfile.readlines()
    logging.debug("user import success, " + args.filename + " closed.")
    args.usernames = args.usernames + usernames
    userfile.close()

# verify user args and shell option
logging.info("validating shell options...")
logging.debug(args.usernames)

if not args.usernames:
    logging.error("no users to add")
    exit()

for uname in args.usernames:
    # remove eofline '\n' and whitespace from username args
    uname=uname.rstrip()
    uname=uname.replace(" ","")    
    if ":" in uname:
        username=uname.split(":")[0]
        shell=uname.split(":")[1].lower()
        # verify username is not blank
        if username=='':
            logging.error("blank username encountered, abort!")
            exit()
    else:
        username=uname
        shell=''

    logging.debug("checking user shell option: " + username + " " + shell)

    if shell=='bash' or shell=='dash' or shell=='tcsh':
        logging.debug( shell + " valid for " + username)
    elif shell=='':
        logging.debug( "no shell set for " + username + " default to " + args.defShell)
    else:
        logging.warning(shell + " invalid! Shell for " + username + 
                       " set to default (" + args.defShell + ")")


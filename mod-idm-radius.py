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

import sys
sys.path.insert(0, './lib/')
import subprocess
import argparse
import logging
import idm_manage

__version__='1.0'

# argparser and auto generate help

# add-idm-group usage
usage = "%(prog)s <new_rad_name>"

parser = argparse.ArgumentParser(prog='mod-idm-radius.py', usage=usage,
                    description='rad stuff')

# default arg values
parser.set_defaults(verbose=False,logfile="idm-actions.log")

# args
parser.add_argument(  "-v","--verbose", action="store_true", dest="verbose", 
                    help="print additional status messages to stdout")
parser.add_argument(  "-q", "--quiet", action="store_false", dest="verbose", 
                    help="don't print status messages to stdout")
parser.add_argument(  "-l", "--logfile", dest="logfile", 
                    help="change logfile location")
parser.add_argument(  'newrad', nargs='+')

# create parser
args = parser.parse_args()

print args.newrad[0]

cmd="ipa user-find | grep 'User login:' | cut -d : -f 2" 

# run the cmd
searchresult = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
searchresult = searchresult.communicate()[0].split()


for user in searchresult:
  idm_manage.modradius(user, args.newrad[0])
  #ipacmd="ipa user-mod " + user + " --radius=" + args.newrad[0]
  #print ipacmd

  # run the ipacmd
  #searchresult = subprocess.Popen(ipacmd, stdout=subprocess.PIPE, shell=True)
  #searchresult = searchresult.communicate()[0].split()

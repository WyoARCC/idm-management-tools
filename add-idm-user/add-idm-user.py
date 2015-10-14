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

from optparse import OptionParser

usage = "usage: %prog [<username>[:<shell>]] [options]"

parser = OptionParser(usage=usage)

parser.set_defaults(verbose=True,logfile="/var/log/idm-log.log", dry=False)

parser.add_option(  "-f", "--file", dest="filename", 
                    metavar="FILE", help="add users from FILE")
parser.add_option(  "-s", "--shell", dest="defShell", 
                    metavar="SHELL", help="override default shell for added users \
                    valid shell options: bash, dash, tcsh")
parser.add_option(  "-v", "--verbose", action="store_true", dest="verbose", 
                    help="don't print status messages to stdout")
parser.add_option(  "-q", "--quiet", action="store_false", dest="verbose", 
                    help="don't print status messages to stdout")
parser.add_option(  "-n", "--dry-run", action="store_true", dest="dry",
                    help="run but do not add users to idm")
parser.add_option(  "-l", "--logfile", dest="logfile", 
                    help="change logfile location")


(options,args) = parser.parse_args()

#!/usr/bin/python

###
#
# get-idm-grouplist.py
#
# Troy Axthelm
# Advanced Research Computing Center
# University of Wyoming
# troy.axthelm@uwyo.edu
#
# Created: 6 May 2016
#
#
# Modified: <initials> <day> <month> <year> <change notes>
#
###

import sys
sys.path.insert(0, './lib/')
import logging
import operator
import subprocess
import argparse

__version__='1.0'

# argparser and auto generate help

# get-idm-group usage
usage = "%(prog)s"

parser = argparse.ArgumentParser(prog='add-idm-group.py', usage=usage,
                    description='Add groups (projects) to idm')

parser.set_defaults(printList=True,nextProj=False)

# version
parser.add_argument('--version', action='version', version="%(prog)s "+__version__)
parser.add_argument('--no-print', action='store_false', dest='printList', 
                    help="do not print the full list of groups")
parser.add_argument('--next-proj', action='store_true', dest='nextProj',
                    help="return the value of the next project gid")

# create parser
args = parser.parse_args()

ldapcmd = "ldapsearch -LLL -x -h arccidm1.arcc.uwyo.edu -b 'cn=groups,cn=accounts,dc=arcc,dc=uwyo,dc=edu' gidNumber cn"

logging.debug(ldapcmd)

# run the ldap cmd
searchresult = subprocess.Popen(ldapcmd, stdout=subprocess.PIPE, shell=True)
searchresult = searchresult.communicate()[0]

# lists to keep different group members
nonpos=[]
aduser=[]
sysuser=[]
projgrp=[]
other=[]

searchresult = searchresult + "\ndn"

cn=""
gid=""

# parse the results, get the cn and gidNumber for each entry, some gidNuber will be empty
for line in searchresult.splitlines():
	if line.startswith('dn:'):
		if cn != "":
			if gid == "":
				nonpos.append(cn)
			elif int(gid) >= 10000000:
				aduser.append((cn,gid))
			elif int(gid) >= 6000000 and int(gid) <= 6999999:
				projgrp.append((cn,gid))
			elif int(gid) >= 5000000 and int(gid) <= 5999999:
				sysuser.append((cn,gid))
			else:
				other.append((cn,gid))
	
		cn=""
		gid=""
	elif line.startswith('cn:'):
		cn=line.split(':')[1].strip()
	elif line.startswith('gidNumber:'):
		gid=line.split(':')[1].strip()

# sort the project group by GID (ascending order)
projgrp.sort(key= operator.itemgetter(1))

if args.printList == True:
	print "Non-Posix Groups:\n"
	for group in nonpos:
		print group

	print "\nAD_Users:\n"
	for group in aduser:
		print ":".join(group)

	print "\nARCC Accounts:\n"
	for group in sysuser:
		print ":".join(group)

	print "\nProjects:\n"
	for group in projgrp:
		print ":".join(group)

	print "\nOther Groups:\n"
	for group in other:
		print ":".join(group)

if args.nextProj == True:
	print projgrp[-1]

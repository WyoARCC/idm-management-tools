#!/usr/bin/python

###
#
# get-group-info.py
#
# Troy Axthelm
# Advanced Research Computing Center
# University of Wyoming
# troy.axthelm@uwyo.edu
#
# Created: 15 June 2016
#
#
# Modified: <initials> <day> <month> <year> <change notes>
#
###

import logging
import operator
import subprocess

def getNextProj():
	#ldapcmd = "ldapsearch -LLL -x -h arccidm1.arcc.uwyo.edu -b 'cn=groups,cn=accounts,dc=arcc,dc=uwyo,dc=edu' gidNumber cn"
      
        ipacmd = "ipa group-find --posix | grep GID: | cut -d : -f 2 | sed 's/^[[:space:]]*//' | sort" 

	logging.debug(ipacmd)

	# run the ldap cmd
	searchresult = subprocess.Popen(ipacmd, stdout=subprocess.PIPE, shell=True)
	searchresult = searchresult.communicate()[0].split()

	# lists to keep different group members
	projgrp=[]
    
	gid=""

	# parse the results, get the cn and gidNumber for each entry, some gidNuber will be empty
	for gid in searchresult:
		if gid != "":
			if int(gid) >= 6000000 and int(gid) <= 6999999:
				projgrp.append(gid)
	# sort the project group by GID (ascending order)
	projgrp.sort()

	return int(projgrp[-1])+1

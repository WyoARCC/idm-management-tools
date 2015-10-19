###
#
# idm_manage.py
#
# Troy Axthelm
# Advanced Research Computing Center
# University of Wyoming
# troy.axthelm@uwyo.edu
#
# Created: 19 October 2015
#
#
# Modified: <initials> <day> <month> <year> <change notes>
#
###

import logging
import subprocess

__version__='1.0'

def addidmusers(userlist):
	for user in userlist:
		if user[5] == '':
			idmcmd = ("ipa user-add %s --first=\"%s\" --last=\"%s\" --cn=\"%s\" --displayname=\"%s\" --email=\"%s\" --phone=\"%s\" --orgunit=\"%s\" --title=\"%s\"\
 --shell=\"%s\"" % (user[0], user[1], user[2], user[0], user[3], user[4], user[7], user[8], user[9], user[10]))
		else:
			idmcmd = ("ipa user-add %s --first=\"%s\" --last=\"%s\" --cn=\"%s\" --displayname=\"%s\" --email=\"%s\" --uid=%s --gidnumber=%s --phone=\"%s\" --orgunit=\"%s\" --title=\"%s\"\
 --shell=\"%s\"" % (user[0], user[1], user[2], user[0], user[3], user[4], user[5], user[6], user[7], user[8], user[9], user[10]))

	# run the idm user-add  cmd
        idmaddresult = subprocess.Popen(idmcmd, stdout=subprocess.PIPE, shell=True)
        idmaddresult = idmaddresult.communicate()[0]

	


def printaddidmusers(userlist):
	for user in userlist:
		if user[5] == '':
			idmcmd = ("ipa user-add %s --first=\"%s\" --last=\"%s\" --cn=\"%s\" --displayname=\"%s\" --email=\"%s\" --phone=\"%s\" --orgunit=\"%s\" --title=\"%s\"\
 --shell=\"%s\"" % (user[0], user[1], user[2], user[0], user[3], user[4], user[7], user[8], user[9], user[10]))
		else:
			idmcmd = ("ipa user-add %s --first=\"%s\" --last=\"%s\" --cn=\"%s\" --displayname=\"%s\" --email=\"%s\" --uid=%s --gidnumber=%s --phone=\"%s\" --orgunit=\"%s\" --title=\"%s\"\
 --shell=\"%s\"" % (user[0], user[1], user[2], user[0], user[3], user[4], user[5], user[6], user[7], user[8], user[9], user[10]))

		print "\n"+idmcmd+"\n"

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

__version__='1.0'

def addidmusers(userlist):
	for user in userlist:
		idmcmd = ("ipa user-add %s --first=\"%s\" --last=\"%s\" --cn=\"%s\" --displayname=\"%s\" --email=\"%s\" --uid=%s --gidnumber=%s --phone=\"%s\" --orgunit=\"%s\" --title=\"%s\"\
 --shell=\"%s\"" % (user[0], user[1], user[2], user[0], user[3], user[4], user[5], user[6], user[7], user[8], user[9], user[10]))

		print idmcmd

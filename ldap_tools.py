###
#
# ldap_tools.py
#
# Troy Axthelm
# Advanced Research Computing Center
# University of Wyoming
# troy.axthelm@uwyo.edu
#
# Created: 16 October 2015
#
#
# Modified: <initials> <day> <month> <year> <change notes>
#
###

import logging
import subprocess

__version__='1.0'

def ldapsearch(username):
	logging.debug("searching cn=Users for %s" % username)
	# search cn=Users for a matching username (most normal UW accounts will be here
	ldapcmd = 'ldapsearch -LLL -H ldaps://windows.uwyo.edu -x -b "cn=Users,dc=windows,' +\
		  'dc=uwyo,dc=edu" -D "cn=arccserv,ou=Special_Accounts,ou=AdminGROUPS,dc=windows,dc=uwyo,dc=edu"'+\
		  ' -y ~/.holmes/pen name=%s mail' % username
	
	logging.debug(ldapcmd)
	
	# run the ldap cmd
	searchresult = subprocess.Popen(ldapcmd, stdout=subprocess.PIPE, shell=True)
	searchresult = searchresult.communicate()[0]

	logging.debug("ldapsearch cn=users for %s returned: %s" % (username, searchresult))
	
	# no result from ldap search of users
	if searchresult == '':
		logging.debug("no result for %s in cn=Users" % username)
		logging.debug("searching special users for %s" % username)
	
		# search special accounts for user
		searchresult = ldapspecial(username)
	
	# no result from ldap search of Special_Accounts
	if searchresult == '':	
		logging.debug("user %s was not found in ldap cn=Users or ou=Special_Accounts" % username)
		logging.info("Failed to find user %s in AD, abort!" % username)
		return 'nodata'
	else:
		return searchresult

def ldapspecial(username):
	logging.debug("searching ou=Special_Accounts for %s" % username)
	# search cn=Special_Accounts for a matching username
	ldapcmd = 'ldapsearch -LLL -H ldaps://windows.uwyo.edu -x -b "ou=Special_Accounts,ou=AdminGROUPS,dc=windows,' +\
		  'dc=uwyo,dc=edu" -D "cn=arccserv,ou=Special_Accounts,ou=AdminGROUPS,dc=windows,dc=uwyo,dc=edu"'+\
		  ' -y ~/.holmes/pen name=%s mail' % username
	
	logging.debug(ldapcmd)
	
	# run the ldap cmd
	searchresult = subprocess.Popen(ldapcmd, stdout=subprocess.PIPE, shell=True)
	searchresult = searchresult.communicate()[0]
	
	logging.debug("ldap cn=Special_Accounts for %s returned: %s" % (username, searchresult))

	return searchresult

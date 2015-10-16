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

attributes = "givenname sn name displayname mail uidnumber gidnumber telephonenumber department title"

def ldapsearch(username):
	logging.debug("searching cn=Users for %s" % username)
	# search cn=Users for a matching username (most normal UW accounts will be here
	ldapcmd = 'ldapsearch -LLL -H ldaps://windows.uwyo.edu -x -b "cn=Users,dc=windows,' +\
		  'dc=uwyo,dc=edu" -D "cn=arccserv,ou=Special_Accounts,ou=AdminGROUPS,dc=windows,dc=uwyo,dc=edu"'+\
		  ' -y ~/.holmes/pen name=%s %s' % (username, attributes)
	
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
		print("user %s not found in AD, abort!" % username)
	else:
		return searchresult

def ldapspecial(username):
	logging.debug("searching ou=Special_Accounts for %s" % username)
	# search cn=Special_Accounts for a matching username
	ldapcmd = 'ldapsearch -LLL -H ldaps://windows.uwyo.edu -x -b "ou=Special_Accounts,ou=AdminGROUPS,dc=windows,' +\
		  'dc=uwyo,dc=edu" -D "cn=arccserv,ou=Special_Accounts,ou=AdminGROUPS,dc=windows,dc=uwyo,dc=edu"'+\
		  ' -y ~/.holmes/pen name=%s %s' % (username, attributes)
	
	logging.debug(ldapcmd)
	
	# run the ldap cmd
	searchresult = subprocess.Popen(ldapcmd, stdout=subprocess.PIPE, shell=True)
	searchresult = searchresult.communicate()[0]
	
	logging.debug("ldap cn=Special_Accounts for %s returned: %s" % (username, searchresult))

	return searchresult

def parseresult(ldapstring):
	ldapstring = ldapstring.lower()
	attrlist = ldapstring.split("\n")
 
	for element in attrlist:
		element = element.split(": ")
		
		if element[0] =='dn':
		elif element[0] == 'name':	
		elif element[0] == 'givenname':	
		elif element[0] == 'sn':	
		elif element[0] == 'displayname':	
		elif element[0] == 'mail':	
		elif element[0] == 'uidnumber':	
		elif element[0] == 'gidnumber':	
		elif element[0] == '':	
		elif element[0] == 'name':	
		elif element[0] == 'name':	
	



















 

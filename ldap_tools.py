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

def ldapsearch(username, shell):
	logging.debug("\nsearching cn=Users for %s" % username)
	# search cn=Users for a matching username (most normal UW accounts will be here
	ldapcmd = 'ldapsearch -LLL -H ldaps://windows.uwyo.edu -x -b "cn=Users,dc=windows,' +\
		  'dc=uwyo,dc=edu" -D "cn=arccserv,ou=Special_Accounts,ou=AdminGROUPS,dc=windows,dc=uwyo,dc=edu"'+ ' -y /root/.holmes/pen name=%s %s' % (username, attributes)
	
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
		print("user %s not found in AD!" % username)
		#exit()
		
		return "NOUSER"
	else:
		searchresult = parseresult(searchresult)	
		searchresult.append(shell)
		
		#verify that name, gid, uid all have values
		if searchresult[0] == '' or searchresult[5] == '' or searchresult[6] == '':
			logging.critical("no value for [name | gid | uid]")
			exit()	
	
		return searchresult
	
	# should not ever get here but if so, exit with error
	logging.critical("bad ldap search, should not be here")
	exit()	

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
	attrlist = ldapstring.split("\n")
 	
	name=''
	givenname=''
	sn=''
	displayname=''
	mail=''
	uidnumber=''
	gidnumber=''
	telephonenumber=''
	department=''
	title='' 
	
	for element in attrlist:
		element = element.split(": ")
		
		if element[0].lower() =='dn':
			logging.debug("recognized returned ldap string")
		elif element[0].lower() == 'name':
			name = element[1].lower()	
		elif element[0].lower() == 'givenname':	
			givenname = element[1]	
		elif element[0].lower() == 'sn':	
			sn = element[1]	
		elif element[0].lower() == 'displayname':	
			displayname = element[1]	
		elif element[0].lower() == 'mail':	
			mail = element[1].lower()	
		elif element[0].lower() == 'uidnumber':	
			uidnumber = element[1]	
		elif element[0].lower() == 'gidnumber':	
			gidnumber = element[1]	
		elif element[0].lower() == 'telephonenumber':	
			telephonenumber = element[1]	
		elif element[0].lower() == 'department':	
			department = element[1]	
		elif element[0].lower() == 'title':	
			title = element[1]

	attrList = [name, givenname, sn, displayname, mail, uidnumber, gidnumber,  telephonenumber, department, title]
	
	logging.debug("Values parsed for %s: " % name)
	logging.debug(attrList)

	return attrList

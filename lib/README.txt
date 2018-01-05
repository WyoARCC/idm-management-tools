Connecting to AD via LDAP
=========================

Two different methods are used:

-------------------------
1) USE OBJECT OF CLASS UWyoLDAP

This method uses an object of class UWyoLDAP (defined in uwyoldap.py in this 
directory), and doesn't rely on extra OS packages. The object retains the LDAP
connection and can be used for as many LDAP requests as necessary, until 
unbind() is called on it to release the connection.

Example
-------
import uwyoldap
import getpass

# Get credentials to connect to AD
username = raw_input('Username: ')
username = "uwyo\\" + username
password = getpass.getpass()

try:
	srv = uwyoldap.UWyoLDAP(username, password)
	del password
except ldap.INVALID_CREDENTIALS:
	print "Invalid Credentials"
	sys.exit()
except ldap.SERVER_DOWN:
	print "Server appears to be down"
	sys.exit()
except:
	print "An error has occurred on attempting to connect to the UWyo AD server"
	sys.exit()

# Use srv to access AD as needed, e.g.:
ad_groups = srv.search(args.cns, uwyoldap.GROUP, uwyoldap.CN)

srv.unbind()

Used by:                                 Uses:
--------                                 -----
../adtoidm.py <groupname>                ./uwyoldap.py
../find_ad_groups.py <str>

-------------------------
2) USE OS COMMANDS FROM openldap-clients (ldapsearch, ldapadd, ldapdelete, etc.)

This method uses OS package "openldap-clients" which provides the OS commands
"ldapsearch", etc.  All LDAP config (server, URI, credentials, groups, etc.) 
must be provided to the ldap* command, and running it includes establishing a
connection (bind), responding to request, and releasing the connection (unbind),
instead of having an object that retains the connection until unbind() is called
on it (as for the other method).

Example
-------
import ldap_tools

# do the required search...
username = ...
usershell = ...
search_result = (ldap_tools.ldapsearch(username, usershell))
if search_result != "NOUSER":
	# search_result is a list of users - use as needed
else:
	print "The username searched for was not found in AD"
	sys.exit()

Used by:                                 Uses:
--------                                 -----
../add-idm-user.py -f <filename>         ./ldap_tools.py
../update-idm-user.py                    ./get_group_info.py
../disable-idm-user.py
../enable-idm-user.py
../get-ad-status.py <usernames>
../idm-group-info.py
../add-idm-group.py


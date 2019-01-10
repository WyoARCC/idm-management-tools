#!/usr/bin/python
# Karen: modified from find_ad_groups.py to get a list of groups that user is
# a member of
import os
import sys
sys.path.insert(0, './lib/')
import uwyoldap
import getpass
import ldap
import subprocess

def print_usage():
    print "\nfind_user_membership.py <grp-name>"
    print "Argment <grp-name> is required.\n"

# Read argument to get search string
if len(sys.argv) < 2:
    print_usage()
    sys.exit(2)
else:
    search_str = sys.argv[1]

# Search for AD password file
PASSWD_LIST = [os.getenv('HOME') + "/.holmes/pen", "/root/.holmes/pen"]
PASSWD_FILE = ""
for i in PASSWD_LIST:
    if os.path.isfile(i):
        PASSWD_FILE = i
        break
# If found password file, use it
if os.path.isfile(PASSWD_FILE):
	username = "arccserv"
	f = open(PASSWD_FILE, 'r')
	password = f.read()
	f.close()
# Otherwise, prompt for credentials
else:
	username = raw_input('Username: ')
	password = getpass.getpass()

# Connect to UW AD server
username = "uwyo\\" + username
try:
    srv = uwyoldap.UWyoLDAP(username, password)
    del password
except ldap.INVALID_CREDENTIALS:
    print 'Invalid Credentials'
    sys.exit()
except ldap.SERVER_DOWN:
    print 'Server appears to be down.'
    sys.exit()
except:
    print "An error has occurred when attempting to connect to the UWyo AD server."
    sys.exit()

# Search for all AD groups
ad_groups = srv.user_get_groups(search_str, 'OU=Groups,OU=petaLibrary,OU=UWIT-RESEARCH,OU=uwit,OU=Department Managed,DC=windows,DC=uwyo,DC=edu')

if not ad_groups:
    print "No matching groups were found on UW AD server. Exiting..."
else:
    print "List of AD groups found:"
    for ad_group in ad_groups:
        # Attributes of ad_group:
        # ad_group.cn, ad_group.gid, etc.
        print '\t' + ad_group.cn + ' (' + ad_group.gid + ')'

# Disconnect from UW AD server
srv.unbind()

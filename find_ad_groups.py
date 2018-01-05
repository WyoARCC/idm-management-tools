#!/usr/bin/python
# Karen: modified from adtoidm.py to get a list of AD groups
import sys
sys.path.insert(0, './lib/')
import uwyoldap
import getpass
import ldap
import subprocess

def print_usage():
    print "\nget_ad_groups.py <group_search_string>"
    print "Argment <group_search_string> is required.\n"

# Read argument to get search string
if len(sys.argv) < 2:
    print_usage()
    sys.exit(2)
else:
    search_str = sys.argv[1]

# Connect to UW AD server
username = raw_input('Username: ')
username = "uwyo\\" + username
password = getpass.getpass()

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
ad_groups = srv.grp_search_substr(search_str, 'OU=Groups,OU=petaLibrary,OU=UWIT-RESEARCH,OU=uwit,OU=Department Managed,DC=windows,DC=uwyo,DC=edu')

if not ad_groups:
    print "No matching groups were found on UW AD server. Exiting..."
    arcc_d.unbind()
    sys.exit()
else:
    print "List of AD groups found:"
    for ad_group in ad_groups:
        # Attributes of ad_group:
        # ad_group.cn, ad_group.gid, etc.

        print '\t' + ad_group.cn + ' (' + ad_group.gid + ')'

# Disconnect from UW AD server
srv.unbind()

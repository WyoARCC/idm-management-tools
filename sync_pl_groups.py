#!/usr/bin/python
###
# sync_pl_groups.py
#
# Syncs all petalibrary groups from AD to IDM. Based on find_ad_groups.py to
# get list of groups, and calls sync_groups function from adtoidm.py to do sync.
# 
# Created: KM 2018.02.22
#
# Modified: <initials> <year>.<month>.<day> <change notes>
#
###

# Must have Kerberos ticket to access IDM as admin user before running

import sys
sys.path.insert(0, './lib/')
import uwyoldap
import getpass
import ldap
import subprocess
import adtoidm       # for sync_groups function

def print_usage():
    print "\nsync_pl_groups.py"
    print "This script doesn't take any arguments.\n"

# Read arguments...
if len(sys.argv) > 1:
    print_usage()
    sys.exit(2)
    
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

# Connect to IDM
arcc_ldap = 'ldaps://arccidm1.arcc.uwyo.edu'
arcc_d = ldap.initialize(arcc_ldap)
arcc_d.simple_bind_s()

# Search for all AD groups
search_strs = ["UWIT-PL", "UWIT-Research"]
for search_str in search_strs:
    ad_groups = srv.grp_search_substr(search_str, 'OU=Groups,OU=petaLibrary,OU=UWIT-RESEARCH,OU=uwit,OU=Department Managed,DC=windows,DC=uwyo,DC=edu')
    if not ad_groups:
        print "No matching groups were found on UW AD server. Exiting..."
        arcc_d.unbind()
        sys.exit()
    else:
        print "Syncing AD groups..."
        # Sync groups
        if search_str == "UWIT-PL":
            adtoidm.sync_groups(arcc_d, ad_groups, "petalibrary")
        else:
            adtoidm.sync_groups(arcc_d, ad_groups, None)

# Disconnect from UW AD server
srv.unbind()

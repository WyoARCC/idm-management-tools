#!/bin/python
###
# adtoidm.py
#
# Reads group info+membership from AD, and then syncs IDM group to AD group (by
# adjusting membership). Doesn't add users to IDM, just adds existing users to
# groups if necessary.
#
# Created: Corben 2016.10.10
# 
# Modified: <initials> <year>.<month>.<day> <change notes>
# KM  2018.02.22 Used main function to make including in other scripts 
#                side-effect-free, so can call sync_groups from other scripts.
###
import sys
sys.path.insert(0, './lib/')
import uwyoldap
import getpass
import ldap
import subprocess
import argparse
import idm_manage

# Currently just syncs all the groups in OU=Groups,OU=petaLibrary,OU=UWIT-RESEARCH,OU=uwit,OU=Department Managed,DC=windows,DC=uwyo,DC=edu
# function is from Troy's idm-managment.
def checkifusersexist(arcc_d, base, users):
    users_exist = []
    for user in users:
        filt = 'uid=' + user
        # Check if user exists.
        user_info = arcc_d.search_s(base, ldap.SCOPE_SUBTREE, filt)
        if user_info:
            users_exist.append(user)
    return users_exist
# End checkifusersexist function

# Define sync_groups function
def sync_groups(arcc_d, ad_groups, cluster):
    for ad_group in ad_groups:
        base = 'dc=arcc,dc=uwyo,dc=edu'
        filt = 'cn=' + ad_group.cn

        ipa_group = arcc_d.search_s(base, ldap.SCOPE_SUBTREE, filt)

        # Check if a group was returned. Potential problem here if there are
        # multiple groups with the same CN (not sure if that's possible or not).
        # I'll fix this later if necessary.
        if not ipa_group:
            # Note: unable to get group PI from AD, so it is '' below...
            if cluster is None:
                if hasattr(ad_group, 'description'):
                    idm_manage.addidmgroup(ad_group.cn, ad_group.gid, '', ad_group.description)
                else:
                    idm_manage.addidmgroup(ad_group.cn, ad_group.gid, '', " ")
            else:
                if hasattr(ad_group, 'description'):
                    idm_manage.addidmgroup(ad_group.cn, ad_group.gid, '', ad_group.description, cluster)
                else:
                    idm_manage.addidmgroup(ad_group.cn, ad_group.gid, '', " ", cluster)
            idm_users = []
        else:
            #if cluster is not None:
                #print "Group already exists in IDM, ignoring cluster..."
            if ipa_group[0][1]['gidNumber'][0] != ad_group.gid:
                print ipa_group[0][1]['gidNumber'][0]
                print ad_group.gid
                print "GID's don't match. Exiting..."
                sys.exit()
            else:
                if 'memberUid' in ipa_group[0][1].keys():
                    idm_users = ipa_group[0][1]['memberUid']
                else:
                    idm_users = []

        s_ad_users = set([i.lower() for i in ad_group.members.keys()])
        s_ipa_users = set([i.lower() for i in idm_users])

        s_users_to_add = s_ad_users - s_ipa_users
        s_users_to_remove = s_ipa_users - s_ad_users

        users_to_add = checkifusersexist(arcc_d, base, s_users_to_add)
        users_to_remove = checkifusersexist(arcc_d, base, s_users_to_remove)

        if users_to_add:
            idm_manage.adduserstogroup(users_to_add, ad_group.cn)
        if users_to_remove:
            idm_manage.removeusersfromgroup(users_to_remove, ad_group.cn)
        print ad_group.cn, "sync complete"
# End sync_groups function

# Define main function
def main():
    parser = argparse.ArgumentParser(description="Sync a group or groups in the University's AD server to ARCC's IDM server")
    #parser.add_argument('-b', '--base', help="Base of AD server groups. Will sync all groups in the base to the IDM server. For example OU=Groups,OU=petaLibrary,OU=UWIT-RESEARCH,OU=uwit,OU=Department Managed,DC=windows,DC=uwyo,DC=edu would add all sync all the petaLibrary groups on the AD server.")
    parser.add_argument('cns', nargs='*', help="The script will attempt to add the given CNs." )
    parser.add_argument('-u', '--username', default=None, help="The username to be used to access the AD server. The domain uwyo is assumed, so you don't have to specify it.")
    parser.add_argument('-c', '--cluster', dest="cluster", type=str, help="specify the cluster, [mountmoran, petalibrary,...], only used if adding new group to IDM")
    args = parser.parse_args()

    if len(args.cns) == 0:
        print "No groups given. Exiting..."
        sys.exit()

    # Connect to AD
    if args.username is None:
        username = raw_input('Username: ')
    else:
        username = args.username
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

    # Use this line instead of the other ad_groups line to just sync the petaLibrary groups.
    #ad_groups = srv.search([], uwyoldap.GROUP, uwyoldap.EMPTY, base='OU=Groups,OU=petaLibrary,OU=UWIT-RESEARCH,OU=uwit,OU=Department Managed,DC=windows,DC=uwyo,DC=edu')
    ad_groups = srv.search(args.cns, uwyoldap.GROUP, uwyoldap.CN)

    if not ad_groups:
        print "None of the given groups were found on UW AD server. Exiting..."
        arcc_d.unbind()
        sys.exit()

    # Sync groups
    sync_groups(arcc_d, ad_groups, args.cluster)

    srv.unbind()
    arcc_d.unbind()
# End main function

if __name__ == "__main__":
    main()

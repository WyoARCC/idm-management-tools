#!/usr/bin/python
###
# idmtoad.py
#
# Syncs petaLibrary groups with gid in range 5-7 million from IDM to AD. 
# 
# Created: KM 2018.10.18
#
# Modified: <initials> <year>.<month>.<day> <change notes>
#
###

# Accesses IDM anonymously since only needs to read; must login to AD
# interactively with admin (sa) account.

import sys, getopt
sys.path.insert(0, './lib/')
import uwyoldap
import getpass
import ldap
import subprocess

# Define print_usage function
def print_usage():
    print "\nidmtoad.py [-V|--version] [-h|--help|-?] [-d|--dryrun] [-g|--groupname g] [-v|--verbose]"
    print "Options: -V OR --version     : print version info"
    print "         -h OR --help OR -?  : print usage"
    print "         -d OR --dryrun      : do dry-run"
    print "         -g OR --groupname g : only run for group with IDM name (cn) of g"
    print "         -v OR --verbose     : run in verbose mode\n"
# End print_usage function

# Define print_ad_groups function
def print_ad_groups(limit_range):
	search_strs = ["UWIT-PL", "UWIT-Research", "UWIT-Research"]
	group_strs = ['OU=Groups,OU=petaLibrary,OU=UWIT-RESEARCH,OU=uwit,OU=Department Managed,DC=windows,DC=uwyo,DC=edu', 'OU=Groups,OU=petaLibrary,OU=UWIT-RESEARCH,OU=uwit,OU=Department Managed,DC=windows,DC=uwyo,DC=edu', 'OU=IDM_Replicated,OU=UWIT-RESEARCH,OU=uwit,OU=Department Managed,DC=windows,DC=uwyo,DC=edu']
	for search_str, group_str in zip(search_strs, group_strs):
		ad_groups = srv.grp_search_substr(search_str, group_str)
		#ad_groups = srv.grp_search_substr(search_str, 'OU=IDM_Replicated,OU=UWIT-RESEARCH,OU=uwit,OU=Department Managed,DC=windows,DC=uwyo,DC=edu')
		print "\nAD groups in search", search_str
		for grp in ad_groups:
			gid = int(grp.gid)
			if limit_range:
				if (gid >= 5000000) and (gid <= 7000000):
					print grp.cn, gid
			else:
				print grp.cn, gid
# End print_ad_groups function

# Define get_ad_groups function
def get_ad_groups():
	result = {}
	search_strs = ["UWIT-PL", "UWIT-Research", "UWIT-Research"]
	group_strs = ['OU=Groups,OU=petaLibrary,OU=UWIT-RESEARCH,OU=uwit,OU=Department Managed,DC=windows,DC=uwyo,DC=edu', 'OU=Groups,OU=petaLibrary,OU=UWIT-RESEARCH,OU=uwit,OU=Department Managed,DC=windows,DC=uwyo,DC=edu', 'OU=IDM_Replicated,OU=UWIT-RESEARCH,OU=uwit,OU=Department Managed,DC=windows,DC=uwyo,DC=edu']
	for search_str, group_str in zip(search_strs, group_strs):
		ad_groups = srv.grp_search_substr(search_str, group_str)
		#ad_groups = srv.grp_search_substr(search_str, 'OU=IDM_Replicated,OU=UWIT-RESEARCH,OU=uwit,OU=Department Managed,DC=windows,DC=uwyo,DC=edu')
		for grp in ad_groups:
			gid = int(grp.gid)
			if (gid >= 5000000) and (gid <= 7000000):
				result[gid] = [grp.cn, grp.members]
	return result
# End get_ad_groups function

# Define get_idm_groups function
def get_idm_groups(arcc_d):
	result = {}
        base = 'dc=arcc,dc=uwyo,dc=edu'
	# Think ipausergroup is what's needed, but posixgroup gives more groups
        filt = '(objectClass=ipausergroup)'
        #filt = '(objectClass=posixgroup)'
	idm_grps = arcc_d.search_s(base, ldap.SCOPE_SUBTREE, filt, ['cn', 'gidNumber', 'member'])
	for grp in idm_grps:
		if grp[1].get('gidNumber') != None:
			gid = int(grp[1]['gidNumber'][0])
			if (gid >= 5000000) and (gid <= 7000000):
				if grp[1].get('member') == None:
					result[gid] = [grp[1]['cn'][0], []]
				else:
					result[gid] = [grp[1]['cn'][0], grp[1]['member']]
	return result
# End get_idm_groups function

# Define in_groups function
def in_groups(idm_groups, SINGLE_GROUP):
	found_group = False
	for idm_grp_key in idm_groups:
		idm_group_name = idm_groups[idm_grp_key][0]
		if SINGLE_GROUP == idm_group_name:
			found_group = True
			break
	return found_group
# End in_groups function

# Define get_single_group function
def get_single_group(idm_groups, SINGLE_GROUP):
	new_group_dict = {}
	for idm_grp_key in idm_groups:
		idm_group_name = idm_groups[idm_grp_key][0]
		if SINGLE_GROUP == idm_group_name:
			new_group_dict[idm_grp_key] = idm_groups[idm_grp_key]
			break
	return new_group_dict
# End get_single_group function

# Define extract_unames_from_list function
def extract_unames_from_list(idm_mem_list):
	result = []
	for mem in idm_mem_list:
		fields = mem.split(',')
		if fields[0].startswith('uid='):
			pair = fields[0].split('=')
			result.append(pair[1])
		elif fields[0].startswith('cn='):
			print "ALERT: has member group "+mem
		else:
			print "ERROR unexpected IDM member", mem
	return result
# End extract_unames_from_list function

# Define lists_are_same_set function
def lists_are_same_set(lst1, lst2):
	result = True
	for l in lst1:
		if not(l in lst2):
			result = False
	for l in lst2:
		if not(l in lst1):
			result = False
	return result
# End lists_are_same_set function

# Define compare_members function
def compare_members(ad_members, idm_members, verbose):
	ad_unames = map((lambda x: x.lower()), ad_members.keys())
	idm_unames = extract_unames_from_list(idm_members)
	if lists_are_same_set(ad_unames, idm_unames):
		#print "AD and IDM groups have the same membership"
		if verbose:
			print "Verbose info: Group membership is the same:"
			print "   AD members:", ad_unames
			print "   IDM members:", idm_unames
	else:
		print "ALERT: Group membership differs:"
		print "   AD members:", ad_unames
		print "   IDM members:", idm_unames
# End compare_members function

# Define user_in_ad function
def user_in_ad(uname):
	user = srv.searchByCN([uname], 'user')
	if user[0][0] == None:
		result = False
	elif uname.lower() in (user[0][0]).lower():
		result = True
	else:
		result = False
	return result
# End user_in_ad function

# Define get_user_dn function
def get_user_dn(uname):
	user = srv.searchByCN([uname], 'user')
	if user[0][0] == None:
		dn = "ERROR user "+uname+" not found"
	else:
		dn = user[0][0]
	return dn
# End get_user_dn function

# Define sync_groups function
def sync_groups(ad_groups, idm_groups, dry_run, verbose):
	# Compare group existence by gid
	for idm_grp_key in sorted(idm_groups):
		idm_group_name = idm_groups[idm_grp_key][0]
		if idm_grp_key in ad_groups:
			print idm_group_name, "(gid", idm_grp_key, ") found in AD, comparing members..."
			compare_members(ad_groups[idm_grp_key][1], idm_groups[idm_grp_key][1], verbose)
		elif (idm_group_name not in DONT_REPLICATE_GROUPS):
			print "\n"+idm_group_name, "(gid", idm_grp_key, ") NOT in AD, checking if can add it..."
			if idm_group_name.lower().startswith('uwit-'):
				cn = idm_group_name
			else:
				cn = 'UWIT-Research-rIDM-'+idm_group_name
			dn = 'CN='+cn+',OU=IDM_Replicated,OU=UWIT-RESEARCH,OU=uwit,OU=Department Managed,DC=windows,DC=uwyo,DC=edu'
			description = idm_group_name+' replicated from IDM for ARCC'
			gidNumber = idm_grp_key
			if verbose:
				print "Attributes to set:"
				print "cn:", cn
				print "dn:", dn
				print "description:", description
				print "gidNumber:", gidNumber
			members = []
			members_missing_from_ad = []
			# NOTE: This method only gets DIRECT members of IDM 
			# group, and alerts if group contains a member that is
			# a group. If all members, including INDIRECT, are
			# needed, then need to modify to get them.
			for mem in idm_groups[idm_grp_key][1]:
				fields = mem.split(',')
				if fields[0].startswith('uid='):
					pair = fields[0].split('=')
					uname = pair[1]
					if (not user_in_ad(uname)):
						members_missing_from_ad.append(uname)
					#Line below works for typical users, but
					#not for training or other special/admin
					#users, so query AD for user dn instead.
					#members.append('CN='+uname+',CN=Users,DC=windows,DC=uwyo,DC=edu')
					members.append(get_user_dn(uname))
				elif fields[0].startswith('cn='):
					print "ALERT: has member group "+mem
				else:
					print "ERROR unexpected IDM member", mem
			if verbose:
				print "members", members
			### ADD GROUP TO AD
			if len(members_missing_from_ad) == 0:
				if dry_run:
					print "IF WEREN'T DRY-RUN, would attempt to add group:", cn
				else:
					srv.add_ad_group(dn, cn, description, gidNumber, members)
			else:
				print "ALERT: Group "+idm_group_name+" has these members which are NOT in AD: "
				print members_missing_from_ad
				print "Not adding group - either add missing members to AD then rerun script, or can add group to don't-replicate list in script"
# End sync_groups function

#SETUP
DEBUG = False
DONT_REPLICATE_GROUPS = ['admins']
DRY_RUN = False
blVerbose = False
SINGLE_GROUP = False

# Read arguments...
try:
    opts, args = getopt.getopt(sys.argv[1:], "Vhdg:v?", ["version", "help", "dryrun", "groupname=", "verbose"])
except getopt.GetoptError:
    print_usage()
    sys.exit(2)

for opt, arg in opts:
    if opt in ("-V", "--version"):
        print "\nidmtoad.py: No version info. Last updated on 12/05/18.\n"
        sys.exit(0)
    elif opt in ("-h", "--help", "-?"):
        print_usage()
        sys.exit(0)
    elif opt in ("-d", "--dryrun"):
        DRY_RUN = True
        print "Running in dry-run mode..."
    elif opt in ("-g", "--groupname"):
        SINGLE_GROUP = arg
        print "Running only for group", SINGLE_GROUP
    elif opt in ("-v", "--verbose"):
        blVerbose = True
        print "Running in verbose mode..."

# Connect to UW AD server
print "Login with an AD admin account."
username = raw_input('Username: ')
username = "uwyo\\" + username
password = getpass.getpass()

try:
    srv = uwyoldap.UWyoLDAPmodify(username, password)
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
arcc_ldap = 'ldaps://arccidm2.arcc.uwyo.edu'
arcc_d = ldap.initialize(arcc_ldap)
arcc_d.simple_bind_s()

# Search for all AD groups
#print_ad_groups(True)

ad_groups = get_ad_groups()
if not ad_groups:
    print "No matching groups were found on UW AD server. Exiting..."
    arcc_d.unbind()
    sys.exit()
elif DEBUG:
    print "AD groups with gid in range 5000000-7000000:"
    #when gid was second element of list
    #for ad_group in sorted(ad_groups, key=(lambda x: x[1])):
    for ad_grp_key in sorted(ad_groups):
        print ad_grp_key, ad_groups[ad_grp_key]

idm_groups = get_idm_groups(arcc_d)
if not idm_groups:
    print "No matching groups were found on ARCC IDM server. Exiting..."
    arcc_d.unbind()
    sys.exit()
elif DEBUG:
    print "IDM groups with gid in range 5000000-7000000:"
    #when gid was second element of list
    #for idm_group in sorted(idm_groups, key=(lambda x: x[1])):
    for idm_grp_key in sorted(idm_groups):
        print idm_grp_key, idm_groups[idm_grp_key]

# Sync IDM groups to AD
if SINGLE_GROUP:
	if in_groups(idm_groups, SINGLE_GROUP):
		idm_groups = get_single_group(idm_groups, SINGLE_GROUP)
	else:
		print "ERROR group "+SINGLE_GROUP+" not in IDM group list"
		sys.exit(2)
sync_groups(ad_groups, idm_groups, DRY_RUN, blVerbose)

# Disconnect from UW AD server
srv.unbind()

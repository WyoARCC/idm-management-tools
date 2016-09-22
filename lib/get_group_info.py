#!/usr/bin/python

###
#
# get-group-info.py
#
# Troy Axthelm
# Advanced Research Computing Center
# University of Wyoming
# troy.axthelm@uwyo.edu
#
# Created: 15 June 2016
#
#
# Modified: <initials> <day> <month> <year> <change notes>
# JDB 2016.09.22 Updated to minimize range use and better searching
#                However, I have plans now to integrate this into the
#                idm_manage.py module to obtain some benefits of making
#                a single library
#
###

import sys
import logging
import operator
import subprocess

# Verbose and debugging options.
VERBOSE=True

# GID Ranges
GID_BEG = 6000000
GID_END = 6999999
GID = []

def getNextProj():
    #ldapcmd = "ldapsearch -LLL -x -h arccidm1.arcc.uwyo.edu -b 'cn=groups,cn=accounts,dc=arcc,dc=uwyo,dc=edu' gidNumber cn"
      
    ipacmd = "ipa group-find --posix | grep GID: | cut -d : -f 2 | sed 's/^[[:space:]]*//' | sort" 

    logging.debug(ipacmd)

    # run the ldap cmd
    searchresult = subprocess.Popen(ipacmd, stdout=subprocess.PIPE, shell=True)
    searchresult = searchresult.communicate()[0].split()

    # lists to keep different group members
    projgrp=[]
    
    gid=""

    # parse the results, get the cn and gidNumber for each entry, some gidNuber will be empty
    for gid in searchresult:
        if gid != "":
            if int(gid) >= 6000000 and int(gid) <= 6999999:
                projgrp.append(gid)
    # sort the project group by GID (ascending order)
    projgrp.sort()

    return int(projgrp[-1])+1

def ldap_project_gid():

    cmd =  "ldapsearch -LLL -x -h arccidm1.arcc.uwyo.edu -b "
    cmd += "'cn=groups,cn=accounts,dc=arcc,dc=uwyo,dc=edu' gidNumber cn "
    cmd += "| grep gidNumber | cut -d: -f2"

    #print(cmd)

    search = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True)
    out,err = search.communicate()
    rc = search.returncode

    if 0 != rc:
        print("Error ({}): {}".format(rc,err))
        sys.exit(0)

    gid_list = [ int(gid) for gid in out.split() if GID_BEG <= int(gid) <= GID_END ]
    gid_list.sort()

    return gid_list
    
def ipa_project_gid():

    # Modified of the a
    ipa_cmd = "ipa group-find --posix | grep GID | cut -d: -f2"

    if VERBOSE:
        print(":: GID Search")
        print(":: IdM Command")
        print("  {}".format(ipa_cmd))
    
    # Leave shell=True right now due to Linux Pipe, "|" in cmd
    search = subprocess.Popen(
            ipa_cmd,
            stdout=subprocess.PIPE, 
            stderr=subprocess.PIPE, 
            shell=True)
    out,err = search.communicate()
    rc = search.returncode

    if 0 != rc: 
        print("You've likely experienced an error...") #< fix this...
        sys.exit(rc)

    # Generate a list in the defined range and sort
    gid_list = [ int(gid) for gid in out.split() if GID_BEG <= int(gid) <= GID_END ]
    gid_list.sort()

    return gid_list

def get_avail_gid(ldap=False):

    if ldap:
        gid_list = ldap_project_gid()
    else:
        gid_list = ipa_project_gid()


    # Create a lazy sequence of the gid_list range
    gid_range = xrange(gid_list[0],gid_list[-1]+1)

    # Determine all un-used GIDs in the current range and next sequential one
    for i in gid_range:
        if i not in gid_list:
            GID.append(i)
            # break # Break on first value
    GID.append(gid_list[-1]+1)
    
    # Storing GID as a module global, don't return anything
    return None


def get_next_proj_gid(legacy=True,ldap=True):
    """
    Return the best GID to minimize range use or next sequential GID.
    Default is legacy which is the next sequential GID. To be changed.
    """

    # Populate GID if not already done
    if len(GID) == 0: get_avail_gid(ldap=True)

    # legacy return
    if legacy: return GID[-1]

    # return best to minimize range use
    return GID[0]


# Testing examples
if __name__ == "__main__":
    print("  Next best GID:   {gid}".format(gid=get_next_proj_gid(legacy=False)))
    print("  Next legacy GID: {gid}".format(gid=get_next_proj_gid(legacy=True)))


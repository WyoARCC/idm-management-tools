###
#
# idm_manage.py
#
# Troy Axthelm
# Advanced Research Computing Center
# University of Wyoming
# troy.axthelm@uwyo.edu
#
# Created: 19 October 2015
#
#
# Modified: <initials> <day> <month> <year> <change notes>
# JDB 2016.09.19 Adding "--cluster" to main program and support in lib. Also
#                attempting to add better output messages than sole use of
#                logging.
#
###

import logging
import subprocess

__version__='1.0'

VERBOSE = False
DRYRUN  = False
DEBUG   = 0


# 
# Helper functions
#
def info(msg=""):
    print("INFO:: " + msg)
    return None

def warning(msg=""):
    return None

def error(msg="",errno=""):
    return None


def addidmusers(userlist):
    for user in userlist:
        if user[5] == '':
            idmcmd = ("ipa user-add %s --first=\"%s\" --last=\"%s\" --cn=\"%s\" --displayname=\"%s\" --email=\"%s\" --phone=\"%s\" --orgunit=\"%s\" --title=\"%s\"\
 --shell=\"%s\" --user-auth-type=radius --radius=radius-prod" % (user[0], user[1], user[2], user[3], user[3], user[4], user[7], user[8], user[9], user[10]))
        else:
            idmcmd = ("ipa user-add %s --first=\"%s\" --last=\"%s\" --cn=\"%s\" --displayname=\"%s\" --email=\"%s\" --uid=%s --gidnumber=%s --phone=\"%s\" --orgunit=\"%s\" --title=\"%s\"\
 --shell=\"/bin/%s\" --user-auth-type=radius --radius=radius-prod" % (user[0], user[1], user[2], user[3], user[3], user[4], user[5], user[6], user[7], user[8], user[9], user[10]))
        
        
        print (idmcmd + "\n")
        
        # run the idm user-add  cmd
        idmaddresult = subprocess.Popen(idmcmd, stdout=subprocess.PIPE, shell=True)
        idmaddresult = idmaddresult.communicate()[0]

def printaddidmusers(userlist):
    for user in userlist:
        if user[5] == '':
            idmcmd = ("ipa user-add %s --first=\"%s\" --last=\"%s\" --cn=\"%s\" --displayname=\"%s\" --email=\"%s\" --phone=\"%s\" --orgunit=\"%s\" --title=\"%s\"\
 --shell=\"%s\" --user-auth-type=radius --radius=radius-prod" % (user[0], user[1], user[2], user[3], user[3], user[4], user[7], user[8], user[9], user[10]))
        else:
            idmcmd = ("ipa user-add %s --first=\"%s\" --last=\"%s\" --cn=\"%s\" --displayname=\"%s\" --email=\"%s\" --uid=%s --gidnumber=%s --phone=\"%s\" --orgunit=\"%s\" --title=\"%s\"\
 --shell=\"/bin/%s\" --user-auth-type=radius --radius=radius-prod" % (user[0], user[1], user[2], user[3], user[3], user[4], user[5], user[6], user[7], user[8], user[9], user[10]))

        print "\n"+idmcmd+"\n"

def disableidmusers(userlist):
   for user in userlist:
       idmcmd = ("ipa user-disable %s" %user)

       print (idmcmd + "\n")

       # run the idm user-add  cmd
       idmaddresult = subprocess.Popen(idmcmd, stdout=subprocess.PIPE, shell=True)
       idmaddresult = idmaddresult.communicate()[0]

def printdisableidmusers(userlist):
   for user in userlist:
       idmcmd = ("ipa user-disable %s" %(user))
       print (idmcmd + "\n")

def enableidmusers(userlist):
   for user in userlist:
       idmcmd = ("ipa user-enable %s" %user)

       print (idmcmd + "\n")

       # run the idm user-add  cmd
       idmaddresult = subprocess.Popen(idmcmd, stdout=subprocess.PIPE, shell=True)
       idmaddresult = idmaddresult.communicate()[0]

def printenableidmusers(userlist):
   for user in userlist:
      idmcmd = ("ipa user-enable %s" %(user))
      print (idmcmd + "\n")

def updateidmusers(userlist):
   for user in userlist:
       idmcmd = ("ipa user-mod %s %s" % (user[0], user[1]))
       print (idmcmd + "\n")

       # run the idm user-add  cmd
       idmaddresult = subprocess.Popen(idmcmd, stdout=subprocess.PIPE, shell=True)
       idmaddresult = idmaddresult.communicate()[0]

def printupdateidmusers(userlist):
    for user in userlist:
        idmcmd = ("ipa user-mod %s %s" % (user[0], user[1]))
        print (idmcmd + "\n")

def check_group_name(groupname):
    idmcmd = "ipa group-show {}".format(groupname)
    if VERBOSE:
        print(":: Checking Group Name")
        print(":: IdM Command")
        print("  " + idmcmd)
        print("")

    idm_result = subprocess.Popen(idmcmd.split(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err = idm_result.communicate()
    rc = idm_result.returncode

    return rc

def verify_group_add(groupname):
    idmcmd = "ipa group-show {}".format(groupname)
    idm_result = subprocess.Popen(idmcmd.split(),stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err = idm_result.communicate()
    rc = idm_result.returncode
    if 0 != rc:
        print("WARNING: Not yet synced, check again")
    return rc
    


def addidmgroup(groupname, gid, piname, projdesc, cluster=""):
    rc = 0

    valid = check_group_name(groupname)
    if not valid: 
        print("ERROR: The group '{}' already exist!. Aborting".format(groupname)) 
        return valid
    if 2 == valid and VERBOSE:
        print("The group '{}' is not already allocated.".format(groupname))
    else:
        print("WARNING: Unknown exit code from IPA")

    # Add a new group to IPA
    idmcmd = "ipa group-add {} --gid={} --desc=\'{}:\"{}\"\'".format(groupname, gid, piname, projdesc)

    if VERBOSE:
        print(":: Project Information")
        print("  Project:      %s" % (groupname))
        print("  Project ID:   %d" % (gid))
        print("  Project PI:   %s" % (piname))
        print("  Project Desc: %s" % (projdesc))
        print(":: IdM Command")
        print("  " + idmcmd)
        print("")

    if cluster == "":
        info("cluster name not added, you'll need to manually add one later.")
    
    if not DRYRUN:

        cmd = idmcmd.split(" ",4)
        #print(cmd)

        idmaddresult = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out,err= idmaddresult.communicate()
        #print("")
        #print(out)
        #print("")
        rc = idmaddresult.returncode
        if 0 == rc and VERBOSE:
            print(":: Status = Success({})".format(rc))
        if 0 != rc:
            print("ERROR: IPA return code = {}".format(rc))
            print(out)
            print(err)


        if VERBOSE:
            print(":: Verification")
        verify = verify_group_add(groupname)
        print(verify)
        i=0
        while verify != 0 and i < 9:
            verify = verify_group_add(groupname)
            i += 1
            print(i)

        if 0 != verify:
            print("WARNING: Unable to verify the group. Check manually!")
    
        elif verify == 0 and VERBOSE:
            print("  Success")

    cluster_rc = add_group_to_cluster(cluster=cluster,groupname=groupname)

    return rc


def check_cluster_group(cluster=""):
    if "" == cluster: return
    error = check_group_name(cluster)
    if error:
        print("WARNING: the cluster '{}' does not exist. Ignoring.".format(cluster))
        return error
    return error


def add_group_to_cluster(cluster="",groupname=""):

    if cluster == "":
        return 0
    else:
        idmcmd = "ipa group-add-member {} --groups=\"{}\"".format(cluster,groupname)

    error = check_cluster_group(cluster)
    if error: return error

    if VERBOSE:
        print(":: Cluster Information")
        print("  Cluster: {}".format(cluster))
        print(":: IdM Command")
        print("  {}".format(idmcmd))
        print("")

    if DRYRUN: return 0

    #idm_result = subprocess.Popen(idmcmd.split(), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    idm_result = subprocess.Popen(idmcmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    out,err = idm_result.communicate()
    rc = idm_result.returncode
    print("")
    print(rc)
    print(out)
    print(err)
    print("")

    return rc

def addyubikey(username, yubikeyid):
    idmcmd = ("ipa user-mod  %s --addattr=fax=%s" % (username, yubikeyid))

    print (idmcmd + "\n")
    
    idmaddresult = subprocess.Popen(idmcmd, stdout=subprocess.PIPE, shell=True)
    idmaddresult = idmaddresult.communicate()[0]


def modradius(username, radiusserv):
    idmcmd = ("ipa user-mod  %s --radius=%s" % (username, radiusserv))

    print (idmcmd + "\n")

    idmaddresult = subprocess.Popen(idmcmd, stdout=subprocess.PIPE, shell=True)
    idmaddresult = idmaddresult.communicate()[0]


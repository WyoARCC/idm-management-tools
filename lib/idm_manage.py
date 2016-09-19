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

def addidmgroup(groupname, gid, piname, projdesc, cluster=""):
    #global VERBOSE,DRYRUN,DEBUG

    idmcmd = "ipa group-add %s --gid=%s --desc=\'%s:\"%s\"\'" % (groupname, gid, piname, projdesc)

    if VERBOSE:
        print(":: Project Information")
        print("  Project:      %s" % (groupname))
        print("  Project ID:   %d" % (gid))
        print("  Project PI:   %s" % (piname))
        print("  Project Desc: %s" % (projdesc))
        print(":: IdM Command")
        print("  " + idmcmd)
        print("")

    if cluster != "":
        add_group_to_cluster(cluster=cluster,groupname=groupname)
    else:
        info("cluster name not added, you'll need to manually add one later.")

    if DRYRUN: return

    # run the idm user-add  cmd
    idmaddresult = subprocess.Popen(idmcmd, stdout=subprocess.PIPE, shell=True)
    idmaddresult = idmaddresult.communicate()[0]

def add_group_to_cluster(cluster="",groupname=""):

    if cluster == "":
        return None
    else:
        idmcmd = "ipa group-add-member %s --groups=\"%s\"" % (cluster,groupname)

    # TODO Verify that the "cluster" group exist ...

    if VERBOSE:
        print(":: Cluster Information")
        print("  Cluster: %s" % (cluster))
        print(":: IdM Command")
        print("  " + idmcmd)
        print("")

    if DRYRUN: return

    idm_result = subprocess.Popen(idmcmd, stdout=subprocess.PIPE, shell=True)
    idm_result = idm_result.communicate()[0]

    return None

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


#!/usr/bin/env python
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
# JDB 2016.10.12 Shortened the code dramatically.
#
###
import os
import sys
from collections import OrderedDict
import logging
import subprocess

__version__='1.1'

attributes = ( "givenname sn name displayname mail "
               "uidnumber gidnumber telephonenumber department title" )

# Search for the LDAP Password File in special locations
PASSWD_LIST = [os.getenv('HOME') + "/.holmes/pen",
               "/root/.holmes/pen"]
for i in PASSWD_LIST:
    if os.path.isfile(i):
        PASSWD_FILE = i
        break

# LDAP Base
LDAP_DOMAIN = "windows.uwyo.edu"
LDAP_DC = "dc=%s,dc=%s,dc=%s" % tuple(LDAP_DOMAIN.split("."))
LDAP_URI = "ldap://%s" % (LDAP_DOMAIN)
LDAP_BINDDN = ("cn=arccserv,ou=Special_Accounts,ou=AdminGROUPS,"
               "%s " % (LDAP_DC))

LDAP = ("ldapsearch -LLL -x " +
        "-H \"%s\" " % (LDAP_URI) +
        "-y \"%s\" " % (PASSWD_FILE) +
        "-D \"%s\" " % (LDAP_BINDDN) +
        "-b \"%%s,%s\" " % (LDAP_DC)
       )

# Search Areas of AD
AREAS = OrderedDict()
AREAS['users'] = ("cn=Users","General Users")
AREAS['train'] = ("ou=TRAIN,ou=AdminGROUPS", "Training Users")
AREAS['special'] = ("ou=Special_Accounts,ou=AdminGROUPS", "Special Users")
AREAS['extern'] = ("ou=External_Collaborator_Users", "External Collaborators")

# Validation
#print(LDAP % (AREAS['users']))
#print(LDAP % (AREAS['train']))
#print(LDAP % (AREAS['special']))
#print(LDAP % (AREAS['extern']))

def ldapsearch(username, shell="/bin/bash"):

    for key in AREAS.keys():
        logging.info("Searching in %s." % (AREAS[key][1]))
        ldapcmd = "%s name=%s %s." % ( LDAP%AREAS[key][0],username,attributes)
        logging.debug(ldapcmd)

        # run the ldap cmd
        searchresult = subprocess.Popen(ldapcmd, 
                                        stdout=subprocess.PIPE,
                                        shell=True)

        searchresult = searchresult.communicate()[0]

        if searchresult:
            logging.info("Found user, %s, in %s." % (username,AREAS[key][1]))
            break

    if not searchresult: return "NOUSER"

    result = parseresult(searchresult)
    result.append(shell)

    if ( result[0] == '' or result[5] == '' or result[6] == '' ):
        logging.critical("no value for [name | gid | uid]")
        sys.exit(2)    
    
    return result
    
    # should not ever get here but if so, exit with error
    logging.critical("bad ldap search, should not be here")
    sys.exit(1)    

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

    attrList = [name, givenname, sn, displayname, 
                mail, uidnumber, gidnumber,  telephonenumber, 
                department, title]
    
    logging.debug("Values parsed for %s: " % name)
    logging.debug(attrList)

    return attrList

def ldapgetuid(username):

    result = ldapsearch(username)
    if result != 'NOUSER': return int(result[5])
    
    logging.critical("Unable to find UID for %s." % (username))
    return -1

if __name__ == "__main__":
    logging.basicConfig(format='%(levelname)s: %(message)s',
                        level=logging.INFO)
    for each in sys.argv[1:]:
        print(ldapsearch(each))
        print(ldapgetuid(each))


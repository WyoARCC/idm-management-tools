#!/usr/bin/env python
###
#
# user_add.py
#
# Troy Axthelm
# Advanced Research Computing Center
# University of Wyoming
# troy.axthelm@uwyo.edu
#
# Created: 15 October 2015
#
#
# Modified: <initials> <day> <month> <year> <change notes>
#
###

import logging

__version__='1.0'

def manualadd(dstring):
    # if --manual-add, begin interactive process to add IDM user
    logging.debug("begining manual addition process")
    confirm = raw_input("\nYou have selected to manually add a user, continue process (y/n)? [n]: ")

    # check to see if user selected to continue manual process
    if confirm.lower()!='y':
        logging.info("abort manual user process \'%s\', no changes have been made to idm" % confirm)
        exit()

    # prompt for user information
    print("\nPlease fill out the attributes as prompted. (** indicates optional field)\n")

    # username
    username = raw_input("Enter new user's username (eg: arccjdoe): ").replace(" ","")
    firstname = raw_input("**Enter new user's first name (eg: John): ")
    lastname = raw_input("**Enter new user's last name (eg: Doe): ")
    displayname = raw_input("Enter new user's display name (eg: John Doe): ")
    emailaddr = raw_input("**Enter new user's email address (eg: jdoe@mail.com): ")
    phone = raw_input("**Enter new user's phone number (eg: (123)456-789): ")
    orgunit = raw_input("**Enter new user's department or business (eg: Xco, Systems Support): ")
    title = raw_input("**Enter new user's official title or description (eg: Software Specialist): ")
    shell = raw_input("**Enter new user's preffered shell (eg: bash): ")
    
    logging.debug("username: %s, firstname: %s, lastname: %s, displayname: %s, emailAddr: %s, phone: %s, orgunit: %s,\
    title: %s, shell: %s" % (username, firstname, lastname, displayname, emailaddr, phone, orgunit, title, shell))

    # verify that required fields are not empty
    if username=='' or displayname=='':
        logging.error("missing required field to manually add user, abort!")
        exit()

    # confirm user attributes
    print("\n"+dstring+"Please review the user attributes. User will be validated and added to IDM when confirmed.")
    print("\nusername:\t%s\nfirstname:\t%s\nlastname:\t%s\ndisplayname:\t%s\nemailAddr:\t%s\nphone:\t\t%s\norgunit:\t%s\n\
title:\t\t%s\nshell:\t\t%s" % (username, firstname, lastname, displayname, emailaddr, phone, orgunit, title, shell))

    confirm = raw_input("\n"+dstring+"Are all of the above attributes are correct (y/n)? [n]: ") 

    # check to see if user confirmed attributes are correct
    if confirm.lower()!='y':
        logging.info("user attribute not confirmed\'%s\', no changes have been made to idm" % confirm)
        exit()

    logging.info("manual user ready to be added")
    adduser = [username, firstname, lastname, displayname, emailaddr, '','', phone, orgunit, title, shell]
    return adduser

# read in users from a file
def readusers(filename):
    logging.debug("opening userfile to import users: " + filename)
    with open(filename) as userfile:
        usernames = userfile.readlines()
    logging.debug("user import success, " + filename + " closed.")
    userfile.close()
    return usernames

#validate the user shell options
def validateshell(usernames,defShell):
    if not usernames:
        logging.error("no users to add")
        exit()
    
    newnames=[]

    for uname in usernames:
        # remove eofline '\n' and whitespace from username args
        uname=uname.rstrip()
        uname=uname.replace(" ","")
        if ":" in uname:
            username=uname.split(":")[0]
            shell=uname.split(":")[1].lower()
            # verify username is not blank
            if username=='':
                logging.error("blank username encountered, abort!")
                exit()
        else:
            username=uname
            shell=''

        logging.debug("checking user shell option: " + username + " " + shell)

        if shell=='bash' or shell=='dash' or shell=='tcsh':
            logging.debug( shell + " valid for " + username)
	    uname='%s:%s' % (username,shell)
        elif shell=='':
            logging.debug( "no shell set for " + username + " default to " + defShell)
	    uname='%s:%s' % (username,defShell)
        else:
            logging.warning(shell + " invalid! Shell for " + username +
                           " set to default (" + defShell + ")")
	    uname='%s:%s' % (username,defShell)
	
	newnames.append(uname)
    
    return newnames

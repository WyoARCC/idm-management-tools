====================
IDM Management Tools
====================

IDM Management Tools provides tools for implementing IDM requests. Uses LDAP
to access both AD and IDM. Includes scripts for adding AD users to IDM, adding 
projects, system access and other functions. To run a script that accesses IDM,
must first generate a Kerberos ticket.

----------
To generate a Kerberos ticket, use site-specific information.

----------
To sync IDM group membership to AD membership, run (login with AD ID at prompt):

./adtoidm.py <groupname>

----------
To find list of AD groups whose name contains <str>:

./find_ad_groups.py <str>

----------
To add an AD user to IDM:

./add-idm-user.py -f <file_name>
	where <file_name> is a file containing IDs of users to be added, one
	per line

----------


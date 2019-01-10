#!/bin/python
###
# uwyoldap.py
#
# Classes that use LDAP to access UWyo AD server. Originally was going to work 
# with IDM server too, but the two servers are very different. A lot of this 
# code could be better.
#
# 
# Advanced Research Computing Center
# University of Wyoming
# @uwyo.edu
#
# Created: 
# 
# Modified: <initials> <year>.<month>.<day> <change notes>
# KM  2017.09.05 Added function grp_search_substr
# KM  2018.11.08 Added class UWyoLDAPmodify
###

import ldap
import ldap.modlist
import re

URL = 'ldaps://windows.uwyo.edu'
BASE = 'dc=windows,dc=uwyo,dc=edu'
USER = 'Person'
USERS = USER
PERSON = USER
PERSONS = PERSON
GROUP = 'Group' 
GROUPS = GROUP
COMPUTER = 'Computer'
COMPUTERS = COMPUTER
CN = 'cn'
DN = 'dn'
GIDNUMBER = 'gidNumber'
EMPTY = 'empty'

def extractCN(dn):
    """Given the dn on an object, this extracts the cn."""
    return re.findall('CN=(.*?),', dn)[0]


def createLDAPObj(info, ldap_srv):
    """info is the information on the object. This uses the info to
    figure out what type of object it is (computer, user, group) and
    then creates the coresponding LDAPObj."""
    types = {'Person': LDAPUser, 'Group': LDAPGroup,
             'Computer': LDAPComputer}

    objectCat = re.findall('CN=(.*?),', info[1]['objectCategory'][0])

    return types[objectCat[0]](info, ldap_srv)

def createLDAPObjDict(objs):
    """Creates a dictionary from a list of LDAP Obj's. The keys are the cn
    of the object, the value is the object."""
    return {obj.cn: obj for obj in objs}

class UWyoLDAP(object):
    """Uwyo LDAP object. Connects to the ldap server and is used for
    searching."""

    LDAPObjs = {}

    def __init__(self, username, password):
        self.srv = ldap.initialize(URL)
        self.srv.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        self.srv.simple_bind_s(username, password)
        del password

    def unbind(self):
        self.srv.unbind()
    
    def searchByCN(self, cns, cn_type, attrs=None, base=None):
        filt = '(|' + ''.join('(CN={})'.format(n) for n in cns) + ')'
        filt = '(&(objectCategory=' + cn_type + ')' + filt + ')'

        if base:
            b = base
        else:
            b = BASE

        if attrs and type(attrs) is not list:
            attrs = [attrs]

        return self.srv.search_s(b, ldap.SCOPE_SUBTREE, filt, attrs)

    def searchByGID(self, gids, gid_type, attrs=None, base=None):
        filt = '(|' + ''.join('(GID={})'.format(n) for n in gids) + ')'
        filt = '(&(objectCategory=' + gid_type + ')' + filt + ')'

        if base:
            b = base
        else:
            b = BASE

        if attrs and type(attrs) is not list:
            attrs = [attrs]

        return self.srv.search_s(b, ldap.SCOPE_SUBTREE, filt, attrs)

    def emptySearch(self, empty_type, attrs=None, base=None):
        if base:
            b = base
        else:
            b = BASE
        filt = 'objectCategory=' + empty_type
        if attrs and type(attrs) is not list:
            attrs = [attrs]

        return self.srv.search_s(b, ldap.SCOPE_SUBTREE, filt, attrs)

#    def searchByDN(self, dns, dns_type, attrs=None):
#        filt = '(|'
#        for n in dns:
#            new_n = n.split(',')
#            new_n = '&(' + ')('.join(new_n) + ')'
#            filt += '(' + new_n + ')'
#        filt += ')'
#
#        #filts = '(&' + ''.join('({})'.format(x) for n in dns for x in n.split(',')) + ')'
#        print filt
#        #filt = '(|' + ''.join('{})'.format(n) for n in filts) + ')'
#        print filt
#        filt = '(&(objectCategory=' + dns_type + ')' + filt + ')'
#
#        print filt
#
#        if attrs and type(attrs) is not list:
#           attrs = [attrs] 
#
#        return self.srv.search_s(BASE, ldap.SCOPE_SUBTREE, filt, attrs)

    def search(self, vals, objs_type, vals_type, base=None):
        """Search for stuff by given cn's. Result is a list of LDAPObj objects.
        Type must be UWyoLDAP.USERS or UWyoLDAP.GROUPS. Computers aren't
        currently supported. The objects returned will be of the corresponding
        subtype of LDAPObj objects. This stores objects that have already been 
        found once, so they aren't looked up again. This, however, will not work
        if a search with no vals is done (just returning everything in the 
        base)."""
        
        searchers = {'cn': self.searchByCN, 'gidNumber': self.searchByGID}
        
        if type(vals) is not list and vals:
            vals = [vals]
       
        objs = []
        if vals:
            val = vals[:]
        
            for n in val:
                h = '@' + objs_type + '@' + n
                if h in self.LDAPObjs.keys():
                    val.remove(n)
                    objs.append(self.LDAPObjs[h])

            if val == []:
                return objs
            results = searchers[vals_type](val, objs_type, None, base)
        else:
            results = self.emptySearch(objs_type, None, base)

        for result in results:
            if result[0] is not None:
                # Groups with large amounts of users have the users given 
                # in ranges. This handles that.
                if 'member' in result[1]:
                    members_r =  [k for k in result[1].keys() if 'range' in k.lower() and 'member' in k.lower()]
                    if members_r:
                        members_r = result[1][members_r[0]]
                        range_inc = len(members_r)
                        result[1]['member'].extend(members_r)
                        range_v = range_inc
                        while len(members_r) == range_inc:
                            attr = 'member;range=' + str(range_v) + '-' + str((range_v+range_inc)-1)
                            add_info = self.searchByCN([extractCN(result[0])], objs_type, [attr])
                            members_r =  add_info[0][1][add_info[0][1].keys()[0]]
                            range_v += range_inc
                            result[1]['member'].extend(members_r)
                obj = createLDAPObj(result, self)
                self.LDAPObjs['@' + objs_type + '@' + obj.cn] = obj
                self.LDAPObjs['@' + objs_type + '@' + obj.gid] = obj
                #self.LDAPObjs['@' + objs_type + '@' + obj.dn] = obj
                objs.append(obj)
        return objs

    # Function grp_search_substr used by find_ad_groups.py
    def grp_search_substr(self, substr, base=None):
        """Search for groups whose name CONTAINS substr (rather than equals
        a given string). Result is a list of UWyoLDAP.GROUPS (a subtype of
        LDAPObj objects). 
        """
       
	objs_type = GROUP 
        filt = '(&(objectCategory=' + objs_type + ')(cn=*' + substr + '*))'
	## Print DEBUG info:
	#print 'base', base
	#print 'filter', filt

        results = self.srv.search_s(base, ldap.SCOPE_SUBTREE, filt, None)

        objs = []
        for result in results:
            if result[0] is not None:
                obj = createLDAPObj(result, self)
                self.LDAPObjs['@' + objs_type + '@' + obj.cn] = obj
                self.LDAPObjs['@' + objs_type + '@' + obj.gid] = obj
                #self.LDAPObjs['@' + objs_type + '@' + obj.dn] = obj
                objs.append(obj)
        return objs

    # Function user_get_groups
    def user_get_groups(self, uname, base=None):
        """Search for groups that the user uname is a member of. Result is a 
        list of UWyoLDAP.GROUPS (a subtype of LDAPObj objects).
        """
       
	objs_type = GROUP 
        filt = '(&(objectCategory=' + objs_type + ')(cn=' + uname + ',cn=Users))'
	## Print DEBUG info:
	#print 'base', base
	#print 'filter', filt

        results = self.srv.search_s(base, ldap.SCOPE_SUBTREE, filt, None)

        objs = []
        for result in results:
            if result[0] is not None:
                obj = createLDAPObj(result, self)
                self.LDAPObjs['@' + objs_type + '@' + obj.cn] = obj
                self.LDAPObjs['@' + objs_type + '@' + obj.gid] = obj
                #self.LDAPObjs['@' + objs_type + '@' + obj.dn] = obj
                objs.append(obj)
        return objs


class UWyoLDAPmodify(object):
    """Similar to above UWyoLDAP class, but used to modify data in AD instead
    of just searching it."""

    LDAPObjs = {}

    def __init__(self, username, password):
        self.srv = ldap.initialize(URL)
        self.srv.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
        self.srv.simple_bind_s(username, password)
        del password

    def unbind(self):
        self.srv.unbind()
    
    def searchByCN(self, cns, cn_type, attrs=None, base=None):
        filt = '(|' + ''.join('(CN={})'.format(n) for n in cns) + ')'
        filt = '(&(objectCategory=' + cn_type + ')' + filt + ')'

        if base:
            b = base
        else:
            b = BASE

        if attrs and type(attrs) is not list:
            attrs = [attrs]

        return self.srv.search_s(b, ldap.SCOPE_SUBTREE, filt, attrs)

    # Function grp_search_substr
    def grp_search_substr(self, substr, base=None):
        """Search for groups whose name CONTAINS substr (rather than equals
        a given string). Result is a list of UWyoLDAP.GROUPS (a subtype of
        LDAPObj objects). 
        """
       
	objs_type = GROUP 
        filt = '(&(objectCategory=' + objs_type + ')(cn=*' + substr + '*))'
	## Print DEBUG info:
	#print 'base', base
	#print 'filter', filt

        results = self.srv.search_s(base, ldap.SCOPE_SUBTREE, filt, None)

        objs = []
        for result in results:
            if result[0] is not None:
                obj = createLDAPObj(result, self)
                self.LDAPObjs['@' + objs_type + '@' + obj.cn] = obj
                self.LDAPObjs['@' + objs_type + '@' + obj.gid] = obj
                #self.LDAPObjs['@' + objs_type + '@' + obj.dn] = obj
                objs.append(obj)
        return objs

    # Function add_ad_group
    def add_ad_group(self, dn, cn, description, gidNumber, members):
        """Add group to AD
        """
      
	moddict = {'cn': [cn], 'name': [cn], 'sAMAccountName': [cn], 'description': [description], 'gidNumber': [str(gidNumber)], 'member': members, 'objectClass': ['top', 'group']}
	modlist = ldap.modlist.addModlist(moddict)
 
	## Print DEBUG info:
	#print 'dn', dn
	#print 'modlist', modlist

	try:
        	self.srv.add_s(dn, modlist)
	except ldap.LDAPError, e:
		print "Error on attempt to add group:"
		print e
	else:
		print "Added group "+cn


class LDAPObj(object):
    """Base class for ldap objects. The subclasses are LDAPUser, LDAPGroup, and
    LDAPComputer."""
    def __init__(self, info, ldap_srv):
        self.dn = info[0]
        self.cn = extractCN(self.dn)
        self.memberOf = {}
        self.info = info

        if self.info[1]['gidNumber'][0]:
            self.gid = self.info[1]['gidNumber'][0]
        try:
            self.description = self.info[1]['description'][0]
        except:
            pass

        # Just a list of CN's.
        if 'memberOf' in info[1]:
            for obj in info[1]['memberOf']:
                self.memberOf[extractCN(obj)] = obj


class LDAPUser(LDAPObj):
    """User object"""
    def __init__(self, info, ldap_srv):
        super(LDAPUser, self).__init__(info, ldap_srv)
        if 'department' in info[1]:
            self.departments = info[1]['department'][0].split('|')
        else:
            self.departments = None

        self._ldap_srv = ldap_srv
        self.isFaculty = False
        self.isEmployee = False
        self.isStudent = False
        self.isARCCEmployee = False
        self.isRetired = False
        if 'UW Employees' in self.memberOf:
            self.isEmployee = True
            if self.departments and ('IT-Research Support' in self.departments \
                    or 'IT/Research Support' in self.departments):
                self.isARCCEmployee = True
        if 'UW Faculty' in self.memberOf \
                or 'UW Academic Professionals' in self.memberOf:
            self.isFaculty = True
        if 'Enrolled Students' in self.memberOf:
            self.isStudent = True
        if 'Retired' in self.memberOf:
            self.isRetired = True

    def getCollege(self):
        """Attempts to get the college(s) that the user belongs to. Doesn't
        currently work on undergraduate students (it's possible to identify
        some undergrad's colleges but not all.) It will return an empty list
        for them. This will also return an empty list for non-undergrads who
        don't work for a specific college. Some users seem to belong
        to multiple colleges, so this returns a list of colleges."""
        self.college = []
        for group in self.memberOf.keys():
            if group.startswith("DEPT_"):
                groupObj = self._ldap_srv.search([group], GROUP, CN)
                for member in groupObj[0].memberOf.keys():
                    if member.startswith('DIV_College of '):
                        self.college.append(member[len('DIV_College of '):])
        return self.college


class LDAPGroup(LDAPObj):
    """LDAP group."""
    def __init__(self, info, ldap_srv):
        super(LDAPGroup, self).__init__(info, ldap_srv)
        self.members = {}
        # Create dictionary of CN's and their corresponding DN's
        if 'member' in info[1]:
            for obj in info[1]['member']:
                self.members[extractCN(obj)] = obj


class LDAPComputer(LDAPObj):
    """Nothing is done here currently."""
    def __init__(self, info, ldap_srv):
        super(LDAPComputer, self).__init__(info, ldap_srv)
       # Not finished. I don't think ARCC will need this, anyway

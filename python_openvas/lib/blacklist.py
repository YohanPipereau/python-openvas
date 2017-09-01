import textwrap
from . import color

class Blacklist:
    blacklist_filepath = '/opt/python-openvas/etc/blacklist.conf'

    def __init__(self):
        with open(self.blacklist_filepath, 'r') as blacklistFile:
            self.content = [line.strip() for line in blacklistFile.readlines()]

    def AddOid(self, oidList):
        """
            Function used to add a new oid to /etc/blacklist.conf.
        """
        fileContent = set(self.content)
        fileContent.update(set(oidList)) #set don't duplicate an element
        self.content = sorted(fileContent)
        with open(self.blacklist_filepath, 'w') as blacklistFile:
            blacklistFile.write('\n'.join(self.content))
        print(color.GREEN + str(oidList) + ' added to blacklist.conf.' + color.END)

    def RemoveOid(self, oidList):
        """
            Function used to remove an oid in /etc/blacklist.conf
        """
        self.content = sorted(set(self.content) - set(oidList))
        with open(self.blacklist_filepath, 'w') as blacklistFile:
            blacklistFile.write('\n'.join(self.content))
        print(color.GREEN + str(oidList) + ' removed from blacklist.conf.' + color.END)

    def BlacklistInfo(self, oidinfo):
        """
            Print Information about blacklisted OID.
        """
        print(color.GREEN + 'Blacklisted OID information :' + color.END)
        for oid in self.content:
            try:
                d = oidinfo.get(oid)
                message = '''
                ** {0} , {1} **
                * Family of Vulnerability : {2}
                * CVE : {3}
                * BID : {4}
                * URL : {5}
                * Grade : {6}
                * Description: {7}\n'''.format(d['name'], oid, d['family'], d['CVE'], d['BID'], d['URL'], d['grade'], d['description'])
                print(textwrap.dedent(message))
            except KeyError:
                print(color.BLUE + oid.strip() + ' is blacklisted but can be removed safely because it is an ancient or wrong plugin.' + color.END)
        return 0

    def removeBlacklistedOid(self, oidList):
        return(list(set(oidList) - set(self.content)))

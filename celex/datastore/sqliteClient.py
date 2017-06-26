# TODO build general parser for the alphabet to be queried.
#   ex: CPA -> PhonSylCPA, PhonCPA based on config.json
# TODO write function for query of pronunciation
# TODO write function for query of syllabification
import sqlite3
import json
import io
from contextlib import closing
from collections import OrderedDict

# Important: multithreading is not currently supported
class SQLiteClient:

    def __init__(self, databaseContext):
        self._databaseContext = databaseContext
        print self._databaseContext
        self.config = self._loadConfiguration()
        self.connection = sqlite3.connect(self.config[databaseContext]["path"])

    # string tableName
    # OrderedDict columnsAndTypes: column_name:column_datatype
    # ***columnsAndTypes not protected against SQL injection
    def createTable(self, tableName, columnsAndTypes):
        self._checkPermissions("write_permissions")
        columnInserts = ""
        for columnAndTypeTuple in columnsAndTypes.items():
            columnInserts += columnAndTypeTuple[0] + " " + columnAndTypeTuple[1] + ", "
        SQL = """ CREATE TABLE %s (%s) """ % (self._scrubParameter(tableName),columnInserts.strip(', '))
        print SQL
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(SQL)
            self.connection.commit()

    # string tableName: Table must exist
    def truncateTable(self, tableName):
        self._checkPermissions("write_permissions")
        self._checkProtected(tableName)
        SQL = """ DELETE FROM %s """ % self._scrubParameter(tableName)
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(SQL)
            self.connection.commit()

    # string tableName: Table must exist
    def dropTable(self, tableName):
        self._checkPermissions("write_permissions")
        self._checkProtected(tableName)
        SQL = """ DROP TABLE IF EXISTS %s """ % self._scrubParameter(tableName)
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(SQL)
            self.connection.commit()

    # string tableName: Table must exist
    # dictionary dataDict: Contains key-value pairs for all defined table columns
    def insertIntoTable(self, tableName, dataDict):
        self._checkPermissions("write_permissions")
        places = ','.join(['?'] * len(dataDict))
        keys = ','.join(dataDict.iterkeys())
        values = tuple(dataDict.itervalues())
        SQL = """ INSERT INTO %s({}) VALUES ({}) """ % self._scrubParameter(tableName)
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(SQL.format(keys, places), values)
            self.connection.commit()

    #----------------#
    #   "Private"    #
    #----------------#

    def _loadConfiguration(self):
        with open('celex/datastore/config.json') as json_data_file:
            data = json.load(json_data_file)
        return data

    # string whichpermission can be: "read_permissions" OR "write_permissions"
    def _checkPermissions(self, whichPermission):
        if(not self.config[self._databaseContext][whichPermission]):
            raise PermissionsException("User does not have permission: " + whichPermission)
        else:
            return True

    def _checkProtected(self, tableName):
        if tableName in self.config[self._databaseContext]["protected_tables"]:
            raise PermissionsException("Cannot execute: %s is a protected table" % tableName)
        else:
            return True

    # guards against SQL injection. Only works for single parameter
    def _scrubParameter(self, SQLParameter):
        return ''.join( chr for chr in SQLParameter if chr.isalnum() )


class PermissionsException(Exception):
    pass

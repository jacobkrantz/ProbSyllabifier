import sqlite3
from contextlib import closing



# Important: multithreading not possible without external library or
# db migration
class SQLiteClient:

    def __init__(self):
        self._database_context = "wordforms_db"
        self.connection = sqlite3.connect(
            "../../../wordforms.db"
        )

    def create_table(self, table_name, columns_and_types):
        """
        :param table_name: string
        :param columns_and_types: OrderedDict, column_name:column_datatype
            not protected against SQL injection
        :return: None
        """
        column_inserts = ""
        for column_and_type_tuple in columns_and_types.items():
            column_inserts += (column_and_type_tuple[0] + " "
                               + column_and_type_tuple[1] + ", ")
        sql = """ CREATE TABLE %s (%s) """ % (
            self._scrub_parameter(table_name),
            column_inserts.strip(', ')
        )
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(sql)
            self.connection.commit()

    def truncate_table(self, table_name):
        """
        :param table_name: string, Table must exist
        :return: None
        """
        sql = """ DELETE FROM %s """ % self._scrub_parameter(table_name)
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(sql)
            self.connection.commit()

    def drop_table(self, table_name):
        """
        :param table_name: Table must exist
        :return: None
        """
        sql = (""" DROP TABLE IF EXISTS %s """
               % self._scrub_parameter(table_name))
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(sql)
            self.connection.commit()

    def insert_into_table(self, table_name, data_dict):
        """
        :param table_name: string, Table must exist
        :param data_dict: dict, contains key/value pairs for all
            defined table columns
        :return: None
        """
        places = ','.join(['?'] * len(data_dict))
        keys = ','.join(data_dict.iterkeys())
        values = tuple(data_dict.itervalues())
        sql = (""" INSERT INTO %s (%s) VALUES %s """
               % (self._scrub_parameter(table_name), keys, values))
        with closing(self.connection.cursor()) as cursor:
            cursor.execute(sql)
            self.connection.commit()

    # ---------------- #
    #    "Private"     #
    # ---------------- #

    def _scrub_parameter(self, sql_parameter):
        """ Guards against SQL injection. Only works for single parameter

        :param sql_parameter: string
        :return: string
        """

        return ''.join(char for char in sql_parameter if char.isalnum())


class PermissionsException(Exception):
    pass

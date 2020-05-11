from interface.database.rdbms.include.Commands import Commands
from interface.database.rdbms.mysql.scripts.Templates import *
from base.database_types import *
import json


class Field:
    @staticmethod
    def create_fields_for_install(fields):
        flds = []
        for field in fields:
            flds.append(Field.create_field(field, fields[field]))

        return ",".join(flds)

    @staticmethod
    def generate_appropriate_type(type, database_type='mysql'):
        return DataBaseTypes.types[database_type][type]

    @staticmethod
    def create_field(title, properties):
        # print(properties)
        s = title + " "

        if "type" in properties:
            s += Field.generate_appropriate_type(properties["type"])

        if "key" in properties and properties["key"]:
            s += " PRIMARY KEY AUTO_INCREMENT "

        if "default" in properties:
            s += " DEFAULT " + properties["default"] + " "

        if "relations" in properties and properties["relations"] != "" and properties["relations"] is not None:

            to_comments = []
            for relation in properties["relations"]:
                # to_comment={}
                # if relation['type'] in relation:
                #     to_comment['type'] = relation['type']

                to_comment = {'type': relation['type'] if 'type' in relation else None, 'table': relation['table'] if 'table' in relation else None,
                              'field': relation['field'] if 'field' in relation else None,
                              'middle_table': relation['middle_table'] if 'middle_table' in relation else None}

                if to_comment['middle_table'] is not None:
                    md_tb_nm = to_comment['middle_table']
                    flds = str(md_tb_nm).split('_')
                    connection = mysql.connector.connect(host="localhost", user="root", passwd="", database="bme_db")
                    fn = str.format(Commands.sqls["table.create"], table_name=md_tb_nm,
                                    fields=str.format("id INTEGER UNSIGNED PRIMARY KEY AUTO_INCREMENT , {first} INTEGER UNSIGNED DEFAULT 0, {second} INTEGER UNSIGNED DEFAULT 0",
                                                      first=flds[0], second=flds[1]))
                    print(fn)
                    connection.cursor().execute(fn)

                    # create mid table if not exists
                    pass

                to_comment2 = {}
                for k in to_comment:
                    if to_comment[k] is not None:
                        to_comment2[k] = to_comment[k]

                to_comments.append(to_comment2)

            com = json.dumps(to_comments)
            s += " COMMENT \'" + com + "\' "

        # if "extra" in properties:
        #     if "ai" in properties['extra']:
        #         s += " AUTO_INCREMENT "
        #
        #     if "not null" in properties['extra']:
        #         s += " NOT NULL "
        s += " NOT NULL "
        return s

    @staticmethod
    def get_fields(table, connection=None):
        connection.cursor().execute(str.format(Templates.sqls['table.get.fields'], table_name=table))
        return connection.cursor.fetchall()

    @staticmethod
    def get_available_fields(table, data, connection=None):
        all_fields = Field.get_fields(table, connection)
        fields = {}
        for field in all_fields:
            if field[0] in data:
                fields[field[0]] = data[field[0]]
        return fields

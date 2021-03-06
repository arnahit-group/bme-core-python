import mysql.connector
from interface.database.rdbms.mysql.scripts.Templates import *
from base.models import *
import inflect
from interface.database.rdbms.include.Commands import *
from config.base import *
from config.connection import *
from interface.database.rdbms.mysql.scripts.Field import *
from interface.database.rdbms.mysql.scripts.Table import *


class Database:
    connection = None
    cursor = None
    host = None
    user = None
    password = None
    database = None

    def __init__(self, host, user, password, database):
        self.database = database
        self.host = host
        self.user = user
        self.password = password

    def open(self):
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            passwd=self.password,
            database=self.database
        )

    def close(self):
        self.connection.close()

    def get_data(self, table="all"):
        self.open()
        models = Models.base.copy()
        output = {}
        if table == "all":
            for model_name in models:
                try:
                    if models[model_name]['has_properties']:
                        output[model_name] = self.parse_data(model_name, True)
                    else:
                        output[model_name] = self.parse_data(model_name, False)
                except NameError as error:
                    print(error)
                except mysql.connector.errors.ProgrammingError as error:
                    print(error.msg)
            return output
        else:
            try:
                if models[table]['has_properties']:
                    return self.parse_data(table, True)
                else:
                    return self.parse_data(table, False)
            except NameError as error:
                print(error)
            except mysql.connector.errors.ProgrammingError as error:
                print(error.msg)

    def parse_data(self, table, has_property=False):
        engine = inflect.engine()
        cursor = self.connection.cursor()
        cursor.execute(str.format(Commands.sqls['table.select.simple'], fields='*', table_name=engine.plural(str.lower(table))))
        columns = cursor.column_names
        result = cursor.fetchall()

        datas = []
        for x in result:
            data = {}
            for y in columns:
                data[y] = x[columns.index(y)]
            datas.append(data)

        if has_property:
            datas = self.parse_properties(table, datas)

        return datas

    def parse_properties(self, model_name, datas):
        try:
            cursor = self.connection.cursor()
            cursor.execute(str.format(Commands.sqls['table.select.simple'], fields='*', table_name=str.lower(model_name) + "_properties"))
            properties = cursor.fetchall()
            prp_keys = cursor.column_names
            cursor = self.connection.cursor()
            cursor.execute(
                str.format(Commands.sqls['table.select.simple'] + " ORDER BY item", fields='*', table_name=str.lower(model_name) + "_assigned_properties"))
            assigned_properties = cursor.fetchall()
            ass_keys = cursor.column_names
            ass_prps = []
            for data in datas:
                ass_prp = {}
                id = data['id']
                tmp_assg = []
                for assigned_property in assigned_properties:
                    if assigned_property[ass_keys.index('item')] == id:
                        tmp_assg.append(assigned_property)

                for tmp in tmp_assg:
                    for prp in properties:
                        if tmp[ass_keys.index("property")] == prp[prp_keys.index("id")]:
                            ass_prp[prp[prp_keys.index("title")]] = tmp[ass_keys.index("value")]

                ass_prps.append(ass_prp)
                data['properties'] = ass_prp
        except mysql.connector.errors.ProgrammingError as error:
            print(error)
        return datas

    def install(self):
        engine = inflect.engine()
        models = Models.base.copy()
        for model_name in models:
            print("--------------" + model_name + "--------------------")
            try:
                fn = str.format(Commands.sqls["table.create"], table_name=str(engine.plural(model_name).lower()),
                                fields=Field.create_fields_for_install(models[model_name]['fields']))
                print(fn)
                self.connection.cursor().execute(fn)

                if models[model_name]['has_properties']:
                    template = Templates.tables['properties']
                    # print(engine.plural(model_name,1))
                    fn = str.format(Commands.sqls["table.create"], table_name=str.format(template["title"], engine.plural(model_name, 1).lower()),
                                    fields=",".join(template["fields"]))
                    self.connection.cursor().execute(fn)
                    template = Templates.tables['assigned_properties']
                    fn = str.format(Commands.sqls["table.create"], table_name=str.format(template["title"], engine.plural(model_name, 1).lower()),
                                    fields=",".join(template["fields"]))
                    self.connection.cursor().execute(fn)

                if models[model_name]['has_settings']:
                    template = Templates.tables['settings']
                    fn = str.format(Commands.sqls["table.create"], table_name=str.format(template["title"], engine.plural(model_name, 1).lower()),
                                    fields=",".join(template["fields"]))
                    self.connection.cursor().execute(fn)
                    template = Templates.tables['assigned_settings']
                    fn = str.format(Commands.sqls["table.create"], table_name=str.format(template["title"], engine.plural(model_name, 1).lower()),
                                    fields=",".join(template["fields"]))
                    self.connection.cursor().execute(fn)

            except NameError as error:
                print(error)
            except mysql.connector.errors.ProgrammingError as error:
                print(error.msg)

        # for model_name in models:
        #     for relation in models[model_name]['relations']:
        #         try:
        #             type = relation['type']
        #             if type == "hasOne":
        #                 print("hasOne")
        #             elif type == "belongsTo":
        #                 model = relation['model']
        #                 fn = str.format(Commands.sqls["table.add.fields"], table_name=engine.plural(str.lower(model_name)),
        #                                 fields=str.lower(model) + " UNSIGNED INT NOT NULL DEFAULT 0")
        #                 self.connection.cursor.execute(fn)
        #                 print("belongsTo")
        #
        #             elif type == "hasMany":
        #
        #                 # fn = str.format(Commands.sqls["table.add.fields"], table_name=str(model), fields=",".join(model_name))
        #                 # self.connection.cursor.execute(fn)
        #                 print("hasMany")
        #
        #             elif type == "belongsToMany":
        #                 if "model" in relation:
        #                     model = relation['model']
        #                     if Table.search(self.connection, str.format("{0}_{1}", model_name, model)) == False and Table.search(self.connection,
        #                                                                                                                          str.format("{0}_{1}", model, model_name) == False):
        #                         if "template" not in relation:
        #                             flds = "id UNSIGNED INT PRIMARY KEY NOT NULL AUTO_INCREMENT"
        #                             flds += "," + str.lower(model_name) + " UNSIGNED INT NOT NULL"
        #                             flds += "," + str.lower(model) + " UNSIGNED INT NOT NULL"
        #                             fn = str.format(Commands.sqls["table.create"], table_name=str.format("{0}_{1}", str.lower(model_name), str.lower(model)), fields=flds)
        #                             self.connection.cursor.execute(fn)
        #                         else:
        #                             template = relation['template']
        #
        #                         print("belongsToMany")
        #
        #                 elif "template" in relation:
        #                     template = relation['template']
        #                     fn = str.format(Commands.sqls["table.create"], table_name=engine.plural(str.lower(model_name)),
        #                                     fields=str.lower(model) + " UNSIGNED INT NOT NULL DEFAULT 0")
        #                     self.connection.cursor.execute(fn)
        #                     print("belongsToMany")
        #         except:
        #             print("error")
        #
        #     self.connection.close()


def update(self, table, item_id, data):
    print("hello world")

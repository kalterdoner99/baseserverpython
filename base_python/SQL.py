import mysql.connector
import os
from dotenv import load_dotenv
from . import com
load_dotenv()
class SQL_Abfrage:

    def __init__(self, host="localhost", user="root", password=os.environ["PASSWORD"], database="homeserver",):
        self.database = database
        self.db = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
        )
        self.cursor = self.db.cursor()


    def Execute_Command(self, Abfrage, Additional_Info=None):
        if Additional_Info == None:
            self.cursor.execute(Abfrage)
        else:
            self.cursor.execute(Abfrage, Additional_Info)
        return self.cursor


    def Describe_Tabel(self, Tabel):
        self.cursor.execute("DESCRIBE "+Tabel)
        return self.cursor


    def Show_Tabels(self):
        self.cursor.execute("SHOW TABLES")
        LIST = list()
        for x in self.cursor:
            LIST.append(x)
        return LIST


    def SQL_Return_Too_List(self, SQL_Return, singel=True):
        if singel==True:
            list1 = []
            var = list(SQL_Return)
            for x in var:
                var2 = list(x)
                list1.append(var2[0])
            return list1
        else:
            list1 = []
            var = list(SQL_Return)
            for x in var:
                list2 = []
                for xx in x:
                    list2.append(xx)
                list1.append(list2)
            return list1
    def Return_In_List(self, Abfrage, Additional_Info=None, singel=True):
        var = self.Execute_Command(Abfrage, Additional_Info)
        return self.SQL_Return_Too_List(var, singel)


    def Print_Info_SQL(self, Info):
        for x in Info:
            print(x)


    def Print_List(self, List):
        for x in range(List.__len__()):
            print(List[x])

'''
'''


class Tabel:

    def __init__(self, tabel,  SQL:SQL_Abfrage, database='homeserver'):
        self.database = database
        self.tabel = tabel
        self.SQL = SQL

    #writes into sql tabel: key = value : colum = value
    def basic_write(self, **kwargs):
        #
        colums = ''.join([f"`{x}`," for x in kwargs])
        colums = colums[:len(colums)-1]

        values = ''.join([f"'{kwargs[x]}'," for x in kwargs])
        values = values[:len(values)-1]


        self.SQL.cursor.execute(f"INSERT INTO `{self.database}`.`{self.tabel}` ({colums}) VALUES ({values})")
        self.SQL.db.commit()

    #basic filter   args = colum ;  kwargs: where key = value
    def filter_basic(self, *args, **kwargs):
        # list to str
        selected = str(args)[1:len(str(args))-2].replace("'", "")
        #dicit to key = value and ...
        where_info = [f"{x} = '{kwargs[x]}' and " for x in kwargs]
        where_info = ''.join(where_info)
        where_info = where_info[:len(where_info)-5]

        if kwargs != {}:
            Query = f"SELECT {selected} FROM {self.database}.{self.tabel} WHERE {where_info}"
        else:
            Query = f"SELECT {selected} FROM {self.database}.{self.tabel}"
        return self.SQL.Return_In_List(Query, singel=False)


#SQL INFO is some sort of the django models; it creates the class Tabel for the mysql tabels, these can be accesed by the Information
class SQL_INFO(com.comunication):

    Information = {

    }

    def __init__(self, SQL:SQL_Abfrage):
        self.SQL = SQL
        self.database = self.SQL.database
        self.Setup()

    def Setup(self):
        TABELS = self.SQL.Show_Tabels()
        for x in TABELS:
            self.Information[str(x[0])] = Tabel(str(x[0]),  self.SQL, self.database,)

    #use to find the Tabel class and perform things on the tabel
    def get_tabel_info(self, name):
        return self.get(name)

class profile:

    def __init__(self):
        self.profiles = dict()

    def create_profile(self, name, user, password):
        self.profiles[name] = [user, password]

prof = profile()
#setups a sql class in com(=communication), multi = if there can be multiple sql classes in the same com
def sql_setup(com, database):

    prof.create_profile('READ', os.environ['USER_READ'], os.environ['PASW_READ'])
    prof.create_profile('WRITE', os.environ['USER_WRITE'], os.environ['PASW_WRITE'])

    if not 'READ' in prof.profiles.keys() and not 'WRITE' in prof.profiles.keys():
        raise NoSetupOfSqlProfiles
    host = os.environ['HOST']


    com[database] = {}

    com[database]['SQL'] = SQL_Abfrage(host, prof.profiles['READ'][0], prof.profiles['READ'][1], database)
    com[database]['SQL_WRITE'] = SQL_Abfrage(host, prof.profiles['WRITE'][0], prof.profiles['WRITE'][1], database)
    com[database]['SQL_TABEL'] = SQL_INFO(com[database]['SQL_WRITE'])

class NoSetupOfSqlProfiles(Exception):
    pass


import pymysql as SQL

print("to register please complete all entries")
print("    SALESMANAGER Setup   ")
print("----------------------------------------\n----------------------------------------")

class SalesManager_Setup():
    def __init__(self):
        self.db_connect = SQL.connect('localhost', 'root', '')
        self.db_cursor  = self.db_connect.cursor()
        self.option = input("""Enter c top create database if you are using app first time \nEnter r to register a new exporter \nEnetr q to quit   >>> """)
        if self.option == "c" or self.option == "C":
            self.Create_Database()
        elif self.option == "r" or self.option == "R":
            self.Registration()
        elif self.option == "q" or self.option == "Q":
            self.quit()
        else:
            Cls = SalesManager_Setup()

    def Create_Database(self):
        sql_query_3 = """ CREATE DATABASE IF NOT EXISTS salesmanager_clients """
        sql_query_4 = """ CREATE TABLE IF NOT EXISTS salesmanager_clients.exporter_clients (
                          full_name CHAR(18) NOT NULL,
                          email TEXT NOT NULL,
                          username CHAR(16) NOT NULL,
                          password CHAR(32) NOT NULL,
                          number_phone CHAR(10) NOT NULL,
                          serial_code CHAR(8) NOT NULL,
                          db_name CHAR(32) NOT NULL,
                          PRIMARY KEY (username),
                          UNIQUE (serial_code, db_name)) """
        
        queries = [sql_query_3, sql_query_4]
        for query in queries:
            self.db_cursor.execute(query)
        self.db_connect.commit()
        print('Database Craeted')
        Cls = SalesManager_Setup()
    
    def Registration(self):
        first_name = input('first name     >>>  ')
        last_name  = input('last name      >>>  ')
        email      = input('email          >>>  ')
        username   = input('username       >>>  ')
        password   = input('password       >>>  ')
        num_phone  = input('number phone   >>>  ')
        ser_code   = input('serial code    >>>  ')
        db_name    = input('database name  >>>  ')
        check_username_query   = """ SELECT * FROM salesmanager_clients.exporter_clients WHERE username='%s' """%username
        check_serialcode_query = """ SELECT * FROM salesmanager_clients.exporter_clients WHERE serial_code='%s' """%ser_code
        check_dbname_query     = """ SELECT * FROM salesmanager_clients.exporter_clients WHERE db_name='%s' """%db_name
        check_username   = self.db_cursor.execute(check_username_query)
        check_serialcode = self.db_cursor.execute(check_serialcode_query)
        check_dbname     = self.db_cursor.execute(check_dbname_query)
        if check_username == 0:
            if check_serialcode == 0:
                if check_dbname == 0:
                    sql_query_1 =""" CREATE USER %s@localhost IDENTIFIED BY '%s' """%(username, password)
                    sql_query_5 = """ INSERT INTO salesmanager_clients.exporter_clients (full_name, email, username, password, number_phone, serial_code, db_name)
                                      VALUES 
                                     ('%s', '%s', '%s', '%s', '%s', '%s', '%s')"""%(first_name+' '+last_name, email, username, password, num_phone, ser_code, db_name)
                    sql_query_6 = """CREATE DATABASE {}""".format(db_name)
                    sql_query_2 =""" GRANT ALL PRIVILEGES ON %s.* TO %s@localhost """%(db_name, username)
                    sql_query_7 = """CREATE TABLE {}.clients (ID INT NOT NULL AUTO_INCREMENT,
                                                            Full_Name CHAR(32) NOT NULL,
                                                            Email CHAR(32) NULL,
                                                            Username CHAR(32) NOT NULL,
                                                            Password CHAR(32) NOT NULL,
                                                            Number_Phone CHAR(12) NOT NULL,
                                                            PRIMARY KEY (ID))""".format(db_name)
                    sql_query_8 = """CREATE TABLE {}.products (ID INT NOT NULL AUTO_INCREMENT,
                                                            Product_Name CHAR(64) NOT NULL,
                                                            Quantity INT NOT NULL,
                                                            Unit_Price FLOAT NOT NULL,
                                                            Product_Code CHAR(8) NOT NULL,
                                                            PRIMARY KEY (Product_Code),
                                                            KEY (ID))""".format(db_name)
                    sql_query_9 = """CREATE TABLE {}.requests (ID INT NOT NULL AUTO_INCREMENT,
                                                            Client CHAR(32) NOT NULL,
                                                            Product_Name CHAR(64) NOT NULL,
                                                            Quantity INT NOT NULL,
                                                            Request_Date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                                                            Status INT NOT NULL,
                                                            PRIMARY KEY (ID))""".format(db_name)
                    queries = [sql_query_1, sql_query_5, sql_query_6, sql_query_2, sql_query_7, 
                               sql_query_8, sql_query_9]
                    for query in queries:
                        self.db_cursor.execute(query)
                    self.db_connect.commit()
                    print('Registered')
                else: print('Database Name is Exist!')
            else: print('Serial Code is Exist!')
        else: print('Username is Exist!')
        Cls = SalesManager_Setup()
                    
    def quit(self):
        self.db_cursor.close()
        self.db_connect.close()



if __name__ == "__main__":
    setup_cls = SalesManager_Setup()
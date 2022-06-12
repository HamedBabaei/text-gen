import psycopg2

class PostgreSQLDatabase():

    def __init__(self, database:str, user:str, password:str, host:str, port:str):
        self.conn = psycopg2.connect(database=database, 
                                    user=user, 
                                    password=password, 
                                    host= host, 
                                    port= port)
        self.conn.autocommit = True
        self.cursor = self.conn.cursor()
        self.__ping()
        try:
            self.__create_db(database)
        except:
            print("Database already exist!")
        try:
            self.__create_table()
        except:
            print("Table already exist!")

    def __ping(self):
        self.cursor.execute("select version()")
        print("Connection established to: ", self.cursor.fetchone())
    
    def __create_db(self, db_name:str):
        sql = f'''CREATE database {db_name}'''
        self.cursor.execute(sql)
        print("Database created successfully........")
    
    def __create_table(self):
        sql = '''CREATE TABLE TEXTGEENERATOR(
                    QUERY VARCHAR(500) NOT NULL,
                    NERS VARCHAR(500),
                    TEXTGEN VARCHAR(2000) NOT NULL
                    )
              '''
        self.cursor.execute(sql)
        print("Table created successfully........")
        self.conn.commit()        

    def __insert(self, query:str, ners:str, textgen:str):
        sql = f'''INSERT INTO TEXTGEENERATOR(QUERY, NERS, TEXTGEN) 
                  VALUES ('{query}', '{ners}', '{textgen}')'''
        self.cursor.execute(sql)
        self.conn.commit()

    def display(self, get=False):
        sql = '''SELECT * FROM TEXTGEENERATOR'''
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if get:
            return results
        else:
            for result in results:
                print(' ||'.join(result))

    def delete(self):
        sql = '''DELETE FROM TEXTGEENERATOR'''
        self.cursor.execute(sql)

    def instert(self, query:str, ners:str, results:list):
        for result in results:
            self.__insert(query, ners, result)
        
    def is_exist(self, textgen):
        sql = f'''SELECT * FROM TEXTGEENERATOR WHERE TEXTGEN='{textgen}' '''
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        # print("EXISTANCE:", result)
        return False if len(result) == 0 else True


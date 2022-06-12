"""
    PostgreSQL Database Interface to store data
"""
import psycopg2


class PostgreSQLDatabase():
    """
        PostgreSQL Database Interface
    """

    def __init__(self, database:str, user:str, password:str, host:str, port:str):
         """
            Initialize PostgreSQLDatabase
        :param database: database name
        :param user: username
        :param password: password
        :param host: host
        :param port: port
        :return:
        """
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
        """
            Check the connection
        :return:
        """
        self.cursor.execute("select version()")
        print("Connection established to: ", self.cursor.fetchone())
    
    def __create_db(self, db_name:str):
        """
            Create PostgreSQLDatabase database if it is not been created
        :param db_name: database name
        :return:
        """
        sql = f'''CREATE database {db_name}'''
        self.cursor.execute(sql)
        print("Database created successfully........")
    
    def __create_table(self):
        """
            Create table if it is not created
        :return:
        """
        sql = '''CREATE TABLE TEXTGEENERATOR(
                    QUERY VARCHAR(500) NOT NULL,
                    NERS VARCHAR(500),
                    TEXTGEN VARCHAR(2000) NOT NULL
                    )
              '''
        self.cursor.execute(sql)
        print("Table created successfully........")
        self.conn.commit()        

    
    def display(self, get=False):
        """
            Display Items from the table
        :param get: whatever to return results or not
        :return:
        """
        sql = '''SELECT * FROM TEXTGEENERATOR'''
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        if get:
            return results
        else:
            for result in results:
                print(' ||'.join(result))

    def delete(self):
        """
            delete items from the table
        :return:
        """
        sql = '''DELETE FROM TEXTGEENERATOR'''
        self.cursor.execute(sql)

    def __insert(self, query:str, ners:str, textgen:str):
        """
            insert row to table
        :param query: input text
        :param ners: joined ners
        :param textgen: generated text
        :return:
        """
        sql = f'''INSERT INTO TEXTGEENERATOR(QUERY, NERS, TEXTGEN) 
                  VALUES ('{query}', '{ners}', '{textgen}')'''
        self.cursor.execute(sql)
        self.conn.commit()

    def instert(self, query:str, ners:str, results:list):
        """
            Insert Items to the table
        :param query: input text
        :param ners: joined ners
        :param textgen: generated texts list
        :return:
        """
        for result in results:
            self.__insert(query, ners, result)
        
    def is_exist(self, textgen):
        """
            Check what ever and item exist in the database
        :param textgen: generated text to check with old generations
        :return:
        """
        sql = f'''SELECT * FROM TEXTGEENERATOR WHERE TEXTGEN='{textgen}' '''
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return False if len(result) == 0 else True

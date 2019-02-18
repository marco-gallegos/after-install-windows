import pymysql.cursors
import os


class MysqlManager(object):
    def __init__(self):
        self.host = None
        self.port = None
        self.user = None
        self.password = None
        self.DB_Exclusiones = [
            "mysql",
            "information_schema",
            "performance_schema",
            "sys",
        ]

    def load_config(self):
        pass

    def respaldar_mysql(self, app):
        DB_Exclusiones = [
            "mysql",
            "information_schema",
            "performance_schema",
            "sys",
        ]
        DB_Respaldar = []

        # Connect to the database
        connection = pymysql.connect(
            host=app.db_data['host'],
            user=app.db_data['user'],
            password=app.db_data['password'],
            port=int(app.db_data['port']),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "show databases"
                cursor.execute(sql)
                databases = cursor.fetchall()
                for database in databases:
                    if database["Database"] not in DB_Exclusiones:
                        DB_Respaldar.append(database["Database"])
        except:
            print("error en la conexion a la db")
        finally:
            connection.close()

        carpeta_destino = app.openFolderName()

        if carpeta_destino != None:
            for db in DB_Respaldar:
                comand = str(
                    f"mysqldump -u {app.db_data['user']} -p{app.db_data['password']} -v --databases {db} > {carpeta_destino}/{db}.sql"
                )
                print(comand)
                os.system(comand)

    def restaurar_mysql(self, app):
        filename = "output.csv"
        DB_Exclusiones = [
            "mysql",
            "information_schema",
            "performance_schema",
            "sys",
        ]
        DB_restaurar = []

        carpeta_origen = app.openFolderName()
        carpeta_origen = carpeta_origen.replace("/", "\\")
        comand = str(f"dir /b  {carpeta_origen}\*.sql > {filename}")
        comand_output = os.system(comand)

        outputfile = open(filename, "r")

        BDS_in_folder = outputfile.readlines()

        # Connect to the database
        connection = pymysql.connect(
            host=app.db_data['host'],
            user=app.db_data['user'],
            password=app.db_data['password'],
            port=int(app.db_data['port']),
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor)

        for nombre_respaldo in BDS_in_folder:
            nombre_respaldo = nombre_respaldo[:-1]
            nombre_respaldo = nombre_respaldo.split(".")
            nombre_respaldo = nombre_respaldo[0]
            DB_restaurar.append(nombre_respaldo)

        with connection.cursor() as cursor:
            # Read a single record
            sql = "show databases"
            cursor.execute(sql)
            databases = cursor.fetchall()
            for database_installed in databases:
                if (database_installed["Database"] in DB_Exclusiones and database_installed["Database"] in DB_restaurar)\
                        or database_installed["Database"] in DB_restaurar:
                    DB_restaurar.remove(database_installed["Database"])

            for database_to_restore in DB_restaurar:
                create_db_command = str(f"create database {database_to_restore}")
                restore_command = str(
                    f"mysql -u {app.db_data['user']} -p{app.db_data['password']} -h {app.db_data['host']} "
                    f"-P {app.db_data['port']} -v {database_to_restore} < {carpeta_origen}\{database_to_restore}.sql")
                cursor.execute(create_db_command)
                os.system(restore_command)

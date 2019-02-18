from qtComponent import *
from MysqlManager import *

## iniciamos  el componente qt
qapp = QApplication(sys.argv)
app = App()

MysqlManager = MysqlManager()

if __name__ == "__main__":
    opc = 0
    opc_mysql = 0
    while opc != 99:
        opc = int(input("1 : mysql\n2 : chocolatey\n-> "))
        if opc == 1:
            while opc_mysql != 99:
                opc_mysql = int(input("1 : respaldar\n2 : restaurar\n-> "))
                if opc_mysql == 1:
                    MysqlManager.respaldar_mysql(app)
                elif opc_mysql == 2:
                    MysqlManager.restaurar_mysql(app)
        elif opc == 2:
            pass

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QFileDialog


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 file dialogs - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.fileName = None
        self.folder = None
        #self.initUI()
        self.db_data = {}
        self.load_config()

    def load_config(self):
        conf_file = open("config.ini","r")
        data_list_csv = conf_file.readlines()
        for data in data_list_csv:
            data = data.split(",")
            self.db_data[data[0]] = data[1]


    def initUI(self):
        self.setWindowTitle(self.title)


        self.setGeometry(self.left, self.top, self.width, self.height)

        self.openFileNameDialog()
        self.openFileNamesDialog()
        self.saveFileDialog()

        #self.show()


    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        if fileName:
            print(fileName)

    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileNames(self, "QFileDialog.getOpenFileNames()", "",
                                            "All Files (*);;Python Files (*.py)", options=options)
        if files:
            print(files)

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            print(fileName)

    def openFolderName(self):
        folder = QFileDialog.getExistingDirectory(self, "Selecciona el directorio")
        self.folder = folder
        return self.folder

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    ex.openFolderName()
    #sys.exit(app.exec_())
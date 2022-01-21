import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from Ui_view import Ui_Form
from main import main


class MyMainForm(QMainWindow, Ui_Form):
    def __init__(self, parent=None) -> None:
        super(MyMainForm, self).__init__(parent)
        self.setupUi(self)

        self.startButton.clicked.connect(self.display)

    def display(self):
        react_path = self.react_lineEdit.text()
        dic = self.dic_lineEdit.text() if self.dic_lineEdit.text() else {}

        tag = self.tag_lineEdit.text()
        appcode = self.ac_lineEdit.text()
        creator = self.creator_lineEdit.text()

        outputpath = self.outputpath_lineEdit.text() if self.outputpath_lineEdit.text() else '..'

        self.startButton.setText("国际化已经开始，请勿重复点击！！！")
        print(react_path, dic)

        main(react_path, tag, dic=dic, appCode=appcode, creator=creator, outputpath=outputpath).start()

        
        self.startButton.setText("国际化已经完成！！！")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainForm()
    myWin.show()
    sys.exit(app.exec_())

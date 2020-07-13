from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot,pyqtSignal
import sys
import bilibili as b
class Objects():
    setting=b.UserSetting()
class Ui_Gui(object):
    def bvGot(self,text):
        self.lineEdit.clear()
        video=b.Bilibili(setting=Objects.setting,bv=text)
        content=video.str()
        if video.isYingXiaoHao():
            content+="疑似营销号！"
        else:
            content+="不是营销号！"
        self.isYingXiaoHao_Dis.setText(content)
    def textGot(self):
        return self.lineEdit.text()
    def main(self):
        text=self.textGot()
        self.bvGot(text)
    def setupUi(self, Gui):
        self.icon=QtGui.QIcon(Objects.setting.icon)
        Gui.setWindowIcon(self.icon)
        Gui.setObjectName("Gui")
        Gui.resize(443, 369)
        Gui.setMaximumSize(QtCore.QSize(443, 369))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(11)
        labelFont=QtGui.QFont()
        labelFont.setFamily("微软雅黑")
        labelFont.setPointSize(10)
        Gui.setFont(font)
        self.centralwidget = QtWidgets.QWidget(Gui)
        self.centralwidget.setObjectName("centralwidget")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(30, 30, 191, 31))
        self.lineEdit.setObjectName("lineEdit")
        self.isYingXiaoHao_Dis = QtWidgets.QLabel(self.centralwidget)
        self.isYingXiaoHao_Dis.setGeometry(QtCore.QRect(80, 90, 261, 191))
        self.isYingXiaoHao_Dis.setFont(labelFont)
        self.isYingXiaoHao_Dis.setAlignment(QtCore.Qt.AlignCenter)
        self.isYingXiaoHao_Dis.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.isYingXiaoHao_Dis.setObjectName("isYingXiaoHao_Dis")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(220, 30, 91, 31))
        self.pushButton.setMaximumSize(QtCore.QSize(91, 31))
        btnfont = QtGui.QFont()
        btnfont.setBold(True)
        btnfont.setWeight(75)
        self.pushButton.setFont(btnfont)
        self.pushButton.setObjectName("pushButton")
        self.Label = QtWidgets.QLabel(self.centralwidget)
        self.Label.setGeometry(QtCore.QRect(30, 0, 71, 31))
        self.Label.setAlignment(QtCore.Qt.AlignCenter)
        self.Label.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.Label.setObjectName("Label")
        Gui.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(Gui)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 443, 26))
        self.menubar.setObjectName("menubar")
        Gui.setMenuBar(self.menubar)
        self.retranslateUi(Gui)
        self.pushButton.clicked.connect(self.main)
        QtCore.QMetaObject.connectSlotsByName(Gui)
    def retranslateUi(self, Gui):
        _translate = QtCore.QCoreApplication.translate
        Gui.setWindowTitle(_translate("Gui", "鉴别真假营销号工具"))
        self.isYingXiaoHao_Dis.setText(_translate("Gui", "TextLabel"))
        self.pushButton.setText(_translate("Gui", "Submit"))
        self.Label.setText(_translate("Gui", "键入BV号"))
def run():
    app=QtWidgets.QApplication(sys.argv)
    widget=QtWidgets.QMainWindow()
    ui=Ui_Gui()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())

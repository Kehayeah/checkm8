# This Python file uses the following encoding: utf-8
import sys
import requests
import re
import json

from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QApplication

class Main(QObject):
    def __init__(self):
        QObject.__init__(self)

    # Greetings
    @pyqtSlot()
    def openIp(self):
        file , check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                                       "", "All Files (*);;Python Files (*.py);;Text Files (*.txt)")
        if check:
            engine.rootObjects()[0].setProperty('ipFile', file)

    @pyqtSlot(str)
    def checkIp(self, arg1):
        if (arg1):
            URL = "https://www.ipvoid.com/ip-blacklist-check/"

            bad_ones = []
            with open(arg1) as f:
                for ip in f.readlines():
                    str1 = ""
                    for ele in ip:
                        str1 += ele
                    r = requests.post(url = URL, data = {"ip":ip.strip()})
                    text = r.text
                    bad_ones.append((str1 , re.findall(r'<i class="fa fa-minus-circle text-danger" aria-hidden="true"></i> (.+?)</td>', text)))
                    print (ip)
            print(json.dumps(bad_ones, indent=4, sort_keys=True))
            engine.rootObjects()[0].setProperty('blackOut', json.dumps(bad_ones, indent=4, sort_keys=True))

    @pyqtSlot(str)
    def exportBlacklist(self, arg1):
        if (arg1):
            fileName, _ = QFileDialog.getSaveFileName(None,"QFileDialog.getSaveFileName()","","JSON Files (*.json);;All Files (*)")
            file = open(fileName,'w')
            file.write(arg1)
            file.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)

    engine = QQmlApplicationEngine()
    main = Main()
    engine.rootContext().setContextProperty("main", main)
    engine.quit.connect(app.quit)
    engine.load('view.qml')

    sys.exit(app.exec())





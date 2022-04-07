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

    # Saves JSON with Ip blacklist
    @pyqtSlot(str)
    def exportBlacklist(self, arg1):
        if (arg1):
            fileName, _ = QFileDialog.getSaveFileName(None,"QFileDialog.getSaveFileName()","","JSON Files (*.json);;All Files (*)")
            file = open(fileName,'w')
            file.write(arg1)
            file.close()

    #Open CSV for linkwise (txt for tests)
    @pyqtSlot()
    def openCSV(self):
        file , check = QFileDialog.getOpenFileName(None, "QFileDialog.getOpenFileName()",
                                                       "", "CSV Files (*.csv);;Text Files (*.txt);;All Files (*)")
        if check:
            engine.rootObjects()[0].setProperty('csvFile', file)

    @pyqtSlot(str, int)
    def parseLinkwise(self, arg1, arg2):
        rType = "https://"
        #print (arg1, arg2)
        if (arg1):
            if (arg2 != -1):
                site = ""
                if (arg2 == 0):
                    site = "www.inizio.gr/"
                elif (arg2 == 1):
                    site = "www.amelies.gr/"
                elif (arg2 == 2):
                    site = "www.ifos.gr/"
                elif (arg2 == 3):
                    site = "www.pervedere.gr/"
                #Set my URL
                URL = rType + site + "helpdesk/get_linkwise_stats.php"
                #fetch data from the file. We will handle txt for now, CSV when proof of consept is done
                prods = ""
                with open(arg1) as f:
                    count = 0
                    for pID in f.readlines():
                        if (count == 0):
                            prods += pID.strip()
                        else:
                            prods += ", " + pID.strip()
                        count += 1
                print (prods)
                r = requests.post(url = URL, data = {"order_id":(prods)})
                text = r.text
                print(json.dumps(text, indent=4, sort_keys=True))
                #engine.rootObjects()[0].setProperty('blackOut', json.dumps(bad_ones, indent=4, sort_keys=True))


if __name__ == "__main__":
    app = QApplication(sys.argv)

    engine = QQmlApplicationEngine()
    main = Main()
    engine.rootContext().setContextProperty("main", main)
    engine.quit.connect(app.quit)
    engine.load('view.qml')

    sys.exit(app.exec())





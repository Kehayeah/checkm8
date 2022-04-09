# This Python file uses the following encoding: utf-8
import sys
import requests
import re
import json
import xlrd
import xlwt
import os

from xlwt import Workbook
from PyQt5.QtGui import QGuiApplication
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QApplication, QErrorMessage

class Main(QObject):
    def __init__(self):
        QObject.__init__(self)

    def initialize(self):
        #Open our config file and set parameters
        fileName = "config.json"
        file = open(fileName)
        data = json.load(file)
        file.close()
        engine.rootObjects()[0].setProperty('authKey', data["authKey"])


    # Saves JSON with Auth Key and other settings, if they exist
    @pyqtSlot(str)
    def saveAuth(self, arg1):
        if (arg1):
            fileName = "config.json"
            file = open(fileName)

            data = json.load(file)
            file.close()
            file = open(fileName,'w')
            data["authKey"] = arg1
            file.write(json.dumps(data, indent=2))
            file.close()

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
                                                       "", "XLS Files (*.xls);;Text Files (*.txt);;All Files (*)")
        if check:
            engine.rootObjects()[0].setProperty('csvFile', file)

    @pyqtSlot(str, int, str)
    def parseLinkwise(self, arg1, arg2, arg3):
        rType = "https://"
        #print (arg1, arg2)
        if (arg1):
            if (arg2 != -1):
                site = ""
                siteType = ""
                if (arg2 == 0):
                    site = "www.inizio.gr/"
                    siteType = "Joomler"
                elif (arg2 == 1):
                    site = "www.amelies.gr/"
                    siteType = "Joomler"
                elif (arg2 == 2):
                    site = "www.ifos.gr/"
                    siteType = "Joomler"
                elif (arg2 == 3):
                    site = "www.pervedere.gr/"
                    siteType = "Magentos"
                #Set my URL
                URL = rType + site + "helpdesk/get_linkwise_stats.php"
                #fetch data from the file. We will handle txt for now, CSV when proof of consept is done
                prods = ""
                wb = xlrd.open_workbook(arg1)
                sheet = wb.sheet_by_index(0)
                sheet.cell_value(2,1)
                count = 0
                for i in range(1, sheet.nrows):
                    if (count == 0):
                        prods += sheet.cell_value(i, 1).strip()
                    else:
                        prods += ", " + sheet.cell_value(i, 1).strip()
                    count += 1

                prodFinal = prods.replace("a", "")
                r = requests.post(url = URL, data = {"order_id":(prodFinal), "authKey": arg3})
                text = r.text
                if (text == "No access"):
                    error_dialog = QErrorMessage()
                    error_dialog.showMessage('Your Auth is probably wrong. Go in the security tab and fix it')
                    error_dialog.exec()
                    engine.rootObjects()[0].setProperty('statLink', "Status: Wrong Auth Key")
                    return
                parsed = json.loads(text)
                # We now have everything we need to start writting in the excel file
                #Copy our file into a var
                data = []
                for row in range(sheet.nrows):
                    data.append([sheet.cell_value(row, col) for col in range(sheet.ncols)])
                #data = [sheet.cell_value(0, col) for col in range(sheet.ncols)]

                #Start new file
                workbook = xlwt.Workbook()
                headStyle = xlwt.easyxf('font: bold 1; align: horiz center')
                bodStyle  = xlwt.easyxf('align: horiz center')
                sheet2 = workbook.add_sheet('Worksheet', cell_overwrite_ok=True)
                count = 0
                for index, value in enumerate(data):
                    for col, val in enumerate(value):
                        if (count == 0):
                            sheet2.write(index, col, val, headStyle)
                        else:
                            sheet2.write(index, col, val, bodStyle)

                    count += 1

                #Translate the texts
                if (siteType == "Joomler"):
                    for i in range (len(parsed)):
                        if (parsed[i] == "COM_VIRTUEMART_ORDER_STATUS_SHIPPED"):
                            parsed[i] = "Απεστάλη"
                        elif (parsed[i] == "COM_VIRTUEMART_ORDER_STATUS_CONFIRMED"):
                            parsed[i] = "Επιβεβαιωμένη"
                        elif (parsed[i] == "COM_VIRTUEMART_ORDER_STATUS_REFUNDED"):
                            parsed[i] = "Επιστροφή χρημάτων"
                        elif (parsed[i] == "COM_VIRTUEMART_ORDER_STATUS_CANCELLED"):
                            parsed[i] = "Ακυρώθηκε"
                        elif (parsed[i] == "COM_VIRTUEMART_ORDER_STATUS_PENDING_RECEIVE"):
                            parsed[i] = "Σε αναμονή παραλαβής"
                        elif (parsed[i] == "COM_VIRTUEMART_ORDER_STATUS_UNDER_MOD"):
                            parsed[i] = "Υπό Επεξεργασία"
                elif (siteType == "Magentos"):
                    #Parse magento stuffs when you know what it looks like
                    for i in range (len(parsed)):
                        if (parsed[i] == "COM_VIRTUEMART_ORDER_STATUS_SHIPPED"):
                            parsed[i] = "Απεστάλη"
                        elif (parsed[i] == "COM_VIRTUEMART_ORDER_STATUS_CONFIRMED"):
                            parsed[i] = "Επιβεβαιωμένη"
                        elif (parsed[i] == "COM_VIRTUEMART_ORDER_STATUS_REFUNDED"):
                            parsed[i] = "Επιστροφή χρημάτων"
                        elif (parsed[i] == "COM_VIRTUEMART_ORDER_STATUS_CANCELLED"):
                            parsed[i] = "Ακυρώθηκε"
                        elif (parsed[i] == "COM_VIRTUEMART_ORDER_STATUS_PENDING_RECEIVE"):
                            parsed[i] = "Σε αναμονή παραλαβής"
                        elif (parsed[i] == "COM_VIRTUEMART_ORDER_STATUS_UNDER_MOD"):
                            parsed[i] = "Υπό Επεξεργασία"
                #Add the values we got from the website
                for i in range(1, sheet.nrows):
                    sheet2.write(i, 5, parsed[i-1], bodStyle)

                #Adjust col width
                sheet2.col(0).width = 256 * 12
                sheet2.col(1).width = 256 * 17
                sheet2.col(2).width = 256 * 18
                sheet2.col(3).width = 256 * 12
                sheet2.col(4).width = 256 * 20
                sheet2.col(5).width = 256 * 30
                workbook.save(os.path.basename(arg1).split('.')[0] + "_Updated.xls")
                engine.rootObjects()[0].setProperty('statLink', "Status: Done")
#                    sheet2.write(0, index, value)




if __name__ == "__main__":
    app = QApplication(sys.argv)

    engine = QQmlApplicationEngine()
    main = Main()
    engine.rootContext().setContextProperty("main", main)
    engine.quit.connect(app.quit)
    engine.load('view.qml')
    main.initialize()

    sys.exit(app.exec())





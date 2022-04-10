import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.11

ApplicationWindow {
    visible: true
    width: 600
    height: 400
    title: "Check M8"

    property string version: ""
    property string buildnum: ""
    property string ipFile: ""
    property string csvFile: ""
    property string blackOut: ""
    property string authKey: ""
    property string statLink: "Status: Not Started"
    property string usernam: ""
    property string pass: ""
    property string monRes: ""
    property string hailStatus: "Status: Not Started"

    TabBar {
        id: tabBar
        x: 0
        y: 0
        width: 600
        height: 41
        currentIndex: 0

        TabButton {
            id: tabButton
            x: 0
            y: 0
            width: 107
            height: 41
            text: qsTr("Linkwise")
            checked: false
        }

        TabButton {
            id: tabButton1
            x: 113
            y: 0
            width: 107
            height: 41
            text: qsTr("Ip Checker")
            checked: true
        }

        TabButton {
            id: tabButton4
            x: 221
            y: 0
            width: 107
            height: 41
            text: qsTr("Security")
            checked: false
        }

        TabButton {
            id: tabButton5
            x: 329
            y: 0
            width: 107
            height: 41
            text: qsTr("Usage Mon.")
            checked: false
        }

        TabButton {
            id: tabButton3
            x: 442
            y: 0
            width: 107
            height: 41
            text: qsTr("About")
            checked: false
        }


    }

    StackLayout {
        id: stackLayout
        x: 0
        y: 52
        width: 600
        height: 313
        currentIndex: tabBar.currentIndex

        Item{
            id: primaryTab

            TextField {
                id: csvSelection
                x: 29
                y: 121
                placeholderText: qsTr("Text Field")
                text: csvFile
            }

            Button {
                id: button
                x: 245
                y: 123
                width: 83
                height: 36
                text: qsTr("Open")
                onClicked: {
                    // call the slot to process the text
                    main.openCSV()
                }
            }

            Text {
                id: text1
                x: 59
                y: 56
                text: "Totaly not a sketchy program that steals your data xD"
                font.pixelSize: 20
            }

            ComboBox {
                id: siteSelection
                x: 425
                y: 121
                currentIndex: -1
                model: ["Inizio", "Amelie's", "Ifos"]
            }

            Button {
                id: button1
                x: 183
                y: 197
                width: 235
                height: 40
                text: qsTr("Let's Get Em")
                onClicked: {
                    // call the slot to process the text
                    main.parseLinkwise(csvSelection.text, siteSelection.currentIndex, authKeyText.text)
                }
            }

            Text {
                id: statusLinkw
                x: 0
                y: 256
                width: 600
                height: 19
                text: statLink
                font.pixelSize: 16
                horizontalAlignment: Text.AlignHCenter
            }
        }

        Item{
            id: secondaryTab

            Text {
                id: text2
                x: 143
                y: 39
                width: 314
                height: 32
                text: qsTr("Check all your IPs, Lazy boy")
                font.pixelSize: 25
                minimumPixelSize: 25
            }

            TextField {
                id: ipList
                x: 27
                y: 96
                width: 198
                height: 28
                placeholderText: qsTr("File with IPs")
                text: ipFile
            }

            TextField {
                id: blacklistFile
                x: 27
                y: 179
                width: 198
                height: 28
                hoverEnabled: false
                placeholderText: qsTr("File with Blacklists")
            }

            Button {
                id: openIP
                x: 231
                y: 96
                width: 82
                height: 28
                text: qsTr("Open")

                onClicked: {
                    // call the slot to process the text
                    main.openIp()
                }
            }

            CheckBox {
                id: checkBox
                x: 27
                y: 140
                width: 154
                height: 33
                text: qsTr("Default Blacklists")
                font.pointSize: 9
                checkState: Qt.Checked
            }

            Button {
                id: openBl
                x: 231
                y: 179
                width: 82
                height: 28
                text: qsTr("Open")
            }

            Button {
                id: checkIPs
                x: 27
                y: 228
                width: 286
                height: 32
                text: qsTr("Let's Check")

                onClicked: {
                    // call the slot to process the text
                    main.checkIp(ipList.text)
                }
            }

            Flickable {
                id: flickable
                anchors.fill: parent
                anchors.bottomMargin: 53
                anchors.topMargin: 96
                anchors.leftMargin: 319

                TextArea.flickable: TextArea {
                    id: blacklistOut
                    x: 0
                    y: 0
                    width: 224
                    height: 168
                    text: "<pre style='color:red'>"+blackOut+"</pre>"
                    verticalAlignment: Text.AlignTop
                    textFormat: Text.RichText
                    renderType: Text.QtRendering
                    placeholderText: qsTr("The Output will be here")
                }

                ScrollBar.vertical: ScrollBar { }
            }

            Button {
                id: saveBlack
                x: 346
                y: 266
                width: 228
                height: 32
                text: qsTr("Save JSON")

                onClicked: {
                    // call the slot to process the text
                    main.exportBlacklist(blackOut)
                }
            }


        }

        Item{
            id: fourthTab

            TextField {
                id: authKeyText
                x: 93
                y: 79
                width: 227
                height: 40
                placeholderText: qsTr("Auth Key")
                text: authKey
            }

            Text {
                id: text6
                x: 25
                y: 20
                text: qsTr("You set your keys here, because we are secure af")
                font.pixelSize: 25
            }

            Button {
                id: saveKey
                x: 354
                y: 79
                text: qsTr("Save")

                onClicked: {
                    // call the slot to process the text
                    main.saveAuth(authKeyText.text)
                }
            }

            TextField {
                id: username
                x: 75
                y: 186
                hoverEnabled: false
                text: usernam
                placeholderText: qsTr("Plesk Username")
            }

            TextField {
                id: passwd
                x: 326
                y: 186
                hoverEnabled: true
                placeholderText: qsTr("Plesk Password")
                text: pass
                echoMode: TextInput.Password
                passwordCharacter: "*"
            }

            Button {
                id: saveCreds
                x: 251
                y: 244
                text: qsTr("Save Credentials")
                onClicked: {
                    // call the slot to process the text
                    main.savePlsk(username.text, passwd.text)
                }
            }

            Label {
                id: label
                x: 216
                y: 157
                text: qsTr("Plesk Credentials for IP Monitoring")
            }


        }

        Item{
            id: fifthTab

            Label {
                id: label1
                x: 8
                y: 8
                text: qsTr("Definitely the most complex part of the whole program")
            }

            Label {
                id: label2
                x: 8
                y: 27
                text: qsTr("Add your credentials in the security tab. Then select the server you want to monitor.")
            }

            ComboBox {
                id: monServer
                x: 8
                y: 80
                width: 182
                height: 40
                currentIndex: -1
                model: ["oramacms.gr", "oramacms1.gr", "oramacms2.gr", "oramacms3.gr", "oramacms4.gr", "oramacms5.gr", "Olympic Stores", "RThess", "Personal"]
            }

            Button {
                id: checkMon
                x: 212
                y: 80
                text: qsTr("Fetch Stats")
                onClicked: {
                    // call the slot to process the text
                    main.monitorPlsk(monServer.currentIndex, usernam, pass, 0)
                }
            }

            Label {
                id: label3
                x: 8
                y: 56
                text: qsTr("Fetch Individual Servers")
                font.pointSize: 11
            }

            Label {
                id: label4
                x: 8
                y: 141
                text: qsTr("Fetch everything (saves to xls)")
                font.pointSize: 11
            }

            Button {
                id: checkMonAll
                x: 8
                y: 165
                width: 202
                height: 40
                text: qsTr("Hail Mary")
                onClicked: {
                    // call the slot to process the text
                    main.monitorPlskAll(usernam, pass)
                }
            }

            Flickable {
                id: flickable1
                x: 318
                y: 80
                width: 268
                height: 225

                TextEdit {
                    id: monStat
                    x: 0
                    y: 0
                    width: 268
                    height: 225
                    text: "<pre style='color:red'>"+monRes+"</pre>"
                    verticalAlignment: Text.AlignTop
                    textFormat: Text.RichText
                    renderType: Text.QtRendering
                    font.pixelSize: 12
                }
            }

            Label {
                id: label5
                x: 318
                y: 56
                text: qsTr("Results")
                font.pointSize: 11
            }

            Text {
                id: hStat
                x: 8
                y: 211
                width: 202
                height: 19
                text: hailStatus
                font.pixelSize: 16
            }


        }

        Item{
            id: thirdTab

            Rectangle{

            }

            Text {
                id: text3
                x: 19
                y: 70
                text: qsTr("Created By the greatest, laziest computer boi of all time")
                font.pixelSize: 23
                minimumPixelSize: 12
            }

            Text {
                id: text4
                x: 270
                y: 134
                text: qsTr("ME :)")
                font.pixelSize: 25
            }

            Text {
                id: text5
                x: 223
                y: 187
                text: qsTr("v"+version+" - build "+buildnum)
                font.pixelSize: 14
            }
        }




    }

}

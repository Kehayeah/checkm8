import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.11

ApplicationWindow {
    visible: true
    width: 600
    height: 400
    title: "Check M8"

    property string ipFile: ""
    property string csvFile: ""
    property string blackOut: ""

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
            x: 0
            y: 0
            width: 107
            height: 41
            text: qsTr("Ip Checker")
            checked: true
        }

        TabButton {
            id: tabButton3
            x: -1
            y: 9
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
                    main.parseLinkwise(csvSelection.text, siteSelection.currentIndex)
                }
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
                    text: blackOut
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
                    main.exportBlacklist(blacklistOut.getText (0, blacklistOut.length) )
                }
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
                text: qsTr("v0.1 - build 0604222151")
                font.pixelSize: 14
            }
        }


    }

}

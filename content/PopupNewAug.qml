
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import AugmentationThingie

Rectangle{
    id : wrapTangle
    required property string title
    required property var confirm_callback
    color: "transparent"

    x: (parent.width - pipelineChangeNamePopup.width) / 2
    y: (parent.height - pipelineChangeNamePopup.height) / 2
    function open(){
        nameInputTextField.text = ""
        pipelineChangeNamePopup.x = parent.x
        pipelineChangeNamePopup.y = parent.y
        pipelineChangeNamePopup.open()
    }
    Popup {
        id: pipelineChangeNamePopup


        width: 300
        height: 130
        modal: true
        focus: true

        background: Rectangle {
            color: "lightgrey"
            radius: 10
        }

        x: parent.x
        y: parent.y

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 10

            Label {
                text: wrapTangle.title
                font.pixelSize: 20
                Layout.alignment: Qt.AlignCenter
                Layout.fillWidth: true

                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                MouseArea {
                    anchors.fill: parent
                    property point pressPos
                    visible: true
                    onPressed: (mouse) => {
                        pressPos = Qt.point(mouse.x, mouse.y)
                    }

                    onPositionChanged: (mouse) => {
                        var dx = mouse.x - pressPos.x
                        var dy = mouse.y - pressPos.y
                        pipelineChangeNamePopup.x += dx
                        pipelineChangeNamePopup.y += dy
                    }
                }
            }

            TextField {
                id: nameInputTextField
                background: Rectangle {
                    color: "white"
                    radius: 10
                }
                validator:RegularExpressionValidator{
                        regularExpression: new RegExp("[a-zA-Z0-9_]{1,20}")
                    }
                placeholderText: "Insert name here..."
                Layout.fillWidth: true
                Layout.fillHeight: true

                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
            }

            RowLayout {
                Layout.alignment: Qt.AlignCenter
                Button {
                    text: "Confirm"
                    onClicked: {
                        // verify that the name is valid
                        if (nameInputTextField.text.length > 0) {
                            wrapTangle.confirm_callback(nameInputTextField.text);
                            pipelineChangeNamePopup.close();
                        }
                        console.log("invalid name")
                    }
                }

                Button {
                    text: "Cancel"
                    onClicked: {
                        pipelineChangeNamePopup.close();
                    }
                }
            }
        }
    }
}

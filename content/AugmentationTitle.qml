import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import AugmentationThingie

Rectangle {
    required property var popupChangeName
    required property var pipelineName

    id: augmentationTitle
    height: 100
    color: "#00ffffff"
    anchors.left: parent.left
    anchors.right: parent.right
    anchors.top: parent.top
    anchors.leftMargin: 0
    anchors.rightMargin: 0
    anchors.topMargin: 0
    Text {
        MouseArea {
            id: mouseArea
            hoverEnabled: true
            anchors.fill: parent
            cursorShape: Qt.OpenHandCursor
            onPositionChanged: {
                toolTip.x = mouseX + 10
                toolTip.y = mouseY + 10
            }
            onClicked: {
                popupChangeName.open()
            }
        }
        ToolTip {
            id: toolTip
            text: "Click to edit augmentation name"
            delay: 1000
            parent: mainWindow.contentItem
            visible: mouseArea.containsMouse
        }
        id: augmentationTitleText
        color: "#cbcece"
        text: pipelineName
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.leftMargin: 0
        font.pixelSize: 70
        horizontalAlignment: Text.AlignLeft
        verticalAlignment: Text.AlignVCenter
        font.weight: Font.Medium
        minimumPointSize: 50
        minimumPixelSize: 50
        fontSizeMode: Text.Fit
        styleColor: "#ffffff"

        wrapMode: Text.WrapAnywhere
        elide: Text.ElideRight
    }
}
import QtQuick 6.5
import QtQuick.Controls 6.5

MenuItem {
    id: menuItem

    property bool isMouseOver: false
    property string menuItemText: "Remove"


    background: Rectangle {
        color: menuItem.isMouseOver ? "black" : "darkgray"
    }

    MouseArea {
        id: mouseAreaMenu
        anchors.fill: parent
        hoverEnabled: true
        onEntered: menuItem.isMouseOver = true
        onExited: menuItem.isMouseOver = false
        onClicked: menuItem.triggered()
    }

    contentItem: Text {
        text: menuItemText
        color: "white"
    }

    onTriggered: {
        // Add the item
    }
}
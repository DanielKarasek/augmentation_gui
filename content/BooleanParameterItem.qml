
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle{
    id: root
    required property var model

    color: "transparent"

    height: rowLayout.childrenRect.height
    RowLayout{
        id: rowLayout
        anchors.left: parent.left
        Label{
            id: label
            text: model.name
            color: "#ffffff"
        }

        CheckBox{
            id: checkbox
            padding: 0
            checked: model.value
            onClicked: {
                model.value = checked
            }
        }

    }

}
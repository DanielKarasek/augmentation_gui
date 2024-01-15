import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle{
    id: root
    property var tupleParameterModel
    height: row.childrenRect.height + label.height
    color: "transparent"
    Label{
        id: label
        text: tupleParameterModel.name
        color: "#ffffff"
        horizontalAlignment: Text.AlignHCenter
        verticalAlignment: Text.AlignVCenter
        clip: true
        background: Rectangle {
            color: "transparent"
        }
    }

    RowLayout {
        id: row
        anchors.top: label.bottom
        anchors.left: parent.left
        anchors.topMargin: 5
        spacing: 5
        Repeater {
            model: tupleParameterModel.items

            delegate: Loader {
                width: sourceComponent.implicitWidth
                required property var modelData
                sourceComponent: modelData.type === "description" ? descriptionComponent : textInputComponent

                Component {
                    id: descriptionComponent
                    Label {
                        color: "#ffffff"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        clip: true
                        background: Rectangle {
                            color: "transparent"
                        }
                        text: modelData.description
                    }
                }

                Component {
                    id: textInputComponent

                    ParameterValueTextField {
                        value_constraints: modelData.constraints
                        Layout.minimumWidth: 100
                        Layout.fillWidth: false
                        text: modelData.value
                        onTextChangedSuccessfully: {
                            modelData.value = text
                        }
                    }
                }
            }
        }
    }
}
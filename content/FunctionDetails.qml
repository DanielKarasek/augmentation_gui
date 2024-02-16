import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import AugmentationThingie

Rectangle {
    id: parameteresContainer
    color: "#101215"
    radius: 40
    required property var functionModel
    Layout.fillWidth: true
    Layout.maximumWidth: 280
    Layout.minimumWidth: 280
    Layout.fillHeight: true
    Rectangle {
        id: parameteresSubContainer
        color: "#00ffffff"
        anchors.fill: parent
        anchors.leftMargin: 10
        anchors.rightMargin: 10
        anchors.topMargin: 15
        anchors.bottomMargin: 40

        Label {
            id: functionLabel
            color: "#ffffff"
            text: functionModel.activeFunction.name
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.bottom: parametersList.top
            anchors.bottomMargin: 0
            font.pixelSize: 20
            horizontalAlignment: Text.AlignHCenter
            verticalAlignment: Text.AlignTop
            wrapMode: Text.WordWrap
            font.underline: false
            font.italic: false
            font.bold: false
        }
        ListView {
            id: parametersList
            anchors.fill: parent
            anchors.topMargin: 60
            spacing: 10
            model: functionModel.activeFunction.parameters

            delegate: Item {
                implicitHeight: parameterLoader.implicitHeight
                Loader {
                    id: parameterLoader
                    anchors.fill: parent
                    sourceComponent: modelData.type === "numberparameter" ? numberParameterComponent
                        : modelData.type === "tupleparameter" ? tupleParameterComponent
                            : booleanParameterComponent
                    property var parameter: modelData
                    Component {
                    id: numberParameterComponent

                    SliderParameterItem {
                        id : sliderParameterItem
                        title: parameter.name
                        value: parameter.value
                        constraints: parameter.constraints

                        implicitHeight: height
                        onValueChanged: {
                            parameter.value = value
                            console.log("sliderParameterItem", parameter.value)
                        }

                        Component.onCompleted: {
                            console.log("sliderParameterItem", parameter.constraints.min_value)
                        }
                        }
                    }
                    Component {
                        id: tupleParameterComponent
                        ToupleParameterItem {
                            tupleParameterModel: parameter
                            implicitHeight: height
                        }
                    }

                    Component {
                        id: booleanParameterComponent
                        BooleanParameterItem {
                            model: parameter
                            implicitHeight: height
                        }
                    }
                }
            }
        }
    }
}

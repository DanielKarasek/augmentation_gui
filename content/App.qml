// Copyright (C) 2021 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import AugmentationThingie

Window {
    width: 1920
    height: 1080
    visible: true
    color: "#000000ff"
    title: "AugmentationThingie"


    PopupMethodChoice{
        id: popupMethodChoice
    }
    Rectangle {
        id: bg
        color: "#1d2226"
        border.color: "#1d2226"
        border.width: 0
        anchors.fill: parent
        anchors.leftMargin: 0
        anchors.rightMargin: 0
        anchors.topMargin: 0
        anchors.bottomMargin: 0

        Rectangle {
            id: titlebar

            height: 44
            color: "#0c0f10"
            border.color: "#404040"
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.leftMargin: 0
            anchors.rightMargin: 0
            anchors.topMargin: 0
        }

        Rectangle {
            id: contentPages
            color: "#1d2226"
            border.color: "#1d2226"
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: titlebar.bottom
            anchors.bottom: parent.bottom
            anchors.leftMargin: 50
            anchors.rightMargin: 50
            anchors.topMargin: 0
            anchors.bottomMargin: 50

            Rectangle {
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
                    id: augmentationTitleText
                    color: "#cbcece"
                    text: augmentationString

                    property var model: augmentationTitleTextModel
                    property var augmentationString: model.augmentationString
                    anchors.fill: parent
                    anchors.leftMargin: 0
                    font.pixelSize: 70
                    horizontalAlignment: Text.AlignLeft
                    verticalAlignment: Text.AlignVCenter
                    font.weight: Font.Medium
                    minimumPointSize: 50
                    minimumPixelSize: 50
                    fontSizeMode: Text.Fit
                    styleColor: "#ffffff"
                }
            }
            RowLayout {
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: augmentationTitle.bottom
                anchors.topMargin: 0
                anchors.bottom: parent.bottom
                spacing: 40

                TreeView {
                    id: treeView
                    model: myModel

                    property var currentIndex: null
                    transformOrigin: Item.Center
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.maximumWidth: 260
                    Layout.minimumWidth: 260


                    delegate: Item {
                        id: treeDelegate

                        Component.onCompleted: {
                            console.log("model", model.display)
                        }
                        MouseArea {
                            id: mouseArea
                            anchors.fill: parent
                            acceptedButtons: Qt.RightButton | Qt.LeftButton
                            onClicked: (mouse) => {
                                           if (mouse.button === Qt.LeftButton) {

                                               treeView.currentIndex = index
                                               if (treeDelegate.isTreeNode && mouse.x <
                                                   treeDelegate.indent * (treeDelegate.depth + 1)) {
                                                   treeView.toggleExpanded(row)
                                               }
                                           }
                                           if (mouse.button === Qt.RightButton)
                                           contextMenu.popup()
                                       }
                        }
                        Menu {
                            id: contextMenu
                            CustomMenuItem {
                                menuItemText: "Add"
                                onTriggered: {
                                    popupMethodChoice.chosenIndex = treeView.currentIndex
                                    popupMethodChoice.open()
                                }
                            }
                            CustomMenuItem {
                                menuItemText: "Remove"
                            }
                        }

                        Rectangle {
                            id: highlightRect
                            color: treeView.currentIndex === index ? "#214283" : "transparent"
                            anchors.fill: parent
                        }

                        implicitWidth: padding + label.x + label.implicitWidth + padding
                        implicitHeight: label.implicitHeight * 1.5

                        readonly property real indent: 20
                        readonly property real padding: 5

                        // Assigned to by TreeView:
                        required property TreeView treeView
                        required property bool isTreeNode
                        required property bool expanded
                        required property int hasChildren
                        required property int depth

                        TapHandler {
                            onTapped: treeView.toggleExpanded(row)
                        }

                        Text {
                            id: indicator
                            visible: treeDelegate.isTreeNode && treeDelegate.hasChildren
                            x: 5 + padding + (treeDelegate.depth * treeDelegate.indent)
                            anchors.verticalCenter: label.verticalCenter
                            text: "▸"
                            rotation: treeDelegate.expanded ? 90 : 0
                            Component.onCompleted:{
                            console.log("indicator", treeDelegate.hasChildren);}
                        }

                        Text {
                            id: label
                            x: 5 + padding + (treeDelegate.isTreeNode ? (treeDelegate.depth + 1) * treeDelegate.indent : 0)
                            width: treeDelegate.width - treeDelegate.padding - x
                            clip: true
                            text: model.display.name
                            anchors.verticalCenter: parent.verticalCenter
                            color: "white"

                        }

                    }
                }
                Rectangle {
                    id: parameteresContainer
                    color: "#101215"
                    radius: 40

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

                        TextArea {
                            id: text1
                            color: "#ffffff"
                            text: functionModel.name
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
                            model: functionModel.parameters

                            Component.onCompleted: {
                                console.log("parameterLoader", functionModel.parameters)
                            }
                            delegate: Item {
                                width: ListView.view.width
                                height: parameterLoader.implicitHeight
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
                                        onValueChanged: {
                                            parameter.value = value
                                            console.log("sliderParameterItem", parameter.value)
                                        }

                                        implicitHeight: 50

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
                Rectangle {
                    id: augmentPreviewContainer
                    x: 0
                    y: 100
                    color: "#00ffffff"
                    Layout.fillWidth: true

                    Layout.preferredWidth: parent.width*0.6
                    Layout.fillHeight: true
                    Rectangle {
                        id: augmentPreviewSubContainer
                        color: "#494949"
                        radius: 40
                        anchors.fill: parent
                        anchors.leftMargin: 0
                        anchors.rightMargin: 0
                        anchors.topMargin: 0
                        anchors.bottomMargin: 0
                    }
                }







            }
        }
    }


}


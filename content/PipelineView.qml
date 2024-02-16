
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import AugmentationThingie


TreeView {
    id: treeView
    property var currentIndex: null
    onCurrentIndexChanged:{
        if (currentIndex !== null) {
            let index = treeView.model.getIndex(currentIndex)
            treeView.model.setActiveFunction(index)
        }
    }
    transformOrigin: Item.Center
    Layout.fillWidth: true
    Layout.fillHeight: true
    Layout.maximumWidth: 260
    Layout.minimumWidth: 260
    interactive: true

    delegate: Item {
        id: treeDelegate

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
                           {
                               treeView.currentIndex = index
                               contextMenu.popup();
                           }
                       }
            onDoubleClicked: {
                   treeView.currentIndex = index
                   contextMenu.popup();
                }

        }
        Menu {
            id: contextMenu
            CustomMenuItem {
                menuItemText: "Add after"
                height: model.display.name !== "Empty" ? menuItemText.implicitHeight : 0
                onTriggered: {
                    popupMethodChoice.chosenIndex = treeView.model.getIndex(index)
                    popupMethodChoice.insert_into = false
                    popupMethodChoice.open()
                }
            }
            CustomMenuItem{
                menuItemText: "Add into"
                height: model.display.expects_sub_functions() ?
                            (model.display.name !== "Empty" ? menuItemText.implicitHeight : 0) : 0
                onTriggered: {
                    popupMethodChoice.chosenIndex = treeView.model.getIndex(index)
                    popupMethodChoice.insert_into = true
                    popupMethodChoice.open()
                }
            }
            CustomMenuItem {
                menuItemText: "Remove"
                height: model.display.name !== "Empty" ? menuItemText.implicitHeight : 0
                onTriggered: {
                    treeView.model.removeItemAtIndex(treeView.model.getIndex(index))
                }
            }
            CustomMenuItem {
                menuItemText: "Replace"
                height: model.display.name === "Empty" ? menuItemText.implicitHeight : 0
                onTriggered: {
                    popupMethodChoice.chosenIndex = treeView.model.getIndex(index)
                    popupMethodChoice.insert_into = false
                    popupMethodChoice.open()
                }
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
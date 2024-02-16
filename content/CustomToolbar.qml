import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import AugmentationThingie

Rectangle {
    id: toolbarWrapper


    height: fileButton.implicitHeight+1
    anchors.left: parent.left
    anchors.top: parent.top
    anchors.right: parent.right
    color: "#ffffff"

    ToolBar {
        id: titlebar
        anchors.left: parent.left
        anchors.top: parent.top
        //
        // background: Rectangle {
        //     color: "#0c0f10"
        //     border.color: "#404040"
        // }

        RowLayout {
            anchors.fill: parent
            Layout.alignment: Qt.AlignLeft

            ToolButton {
                id: fileButton
                text: "File"
                onClicked: fileMenu.open()
                Menu {
                    id: fileMenu
                    MenuItem {
                        text: "Open"
                        onTriggered: {
                            loadPipelineFileDialog.open()
                        }
                    }
                    MenuItem {
                        text: "Save"
                        onTriggered: {
                            savePipelineFileDialog.open()
                        }
                    }
                    MenuItem {
                        text: "Save As"
                        onTriggered: {
                            savePipelineFileDialog.open()
                        }
                    }
                    MenuItem {
                        text: "New Pipeline"
                        onTriggered: {
                            popupNewAug.open()
                        }
                    }
                    MenuItem{
                        text: "Load Dataset"
                        onTriggered: {
                            loadDatasetFolderDialog.open()
                        }

                    }
                    // Add more menu items here
                }
            }

            ToolButton {
                text: "Edit"
                onClicked: editMenu.open()
                Menu {
                    id: editMenu
                    MenuItem {
                        text: "Cut"
                    }
                    MenuItem {
                        text: "Copy"
                    }
                    MenuItem {
                        text: "Paste"
                    }
                    // Add more menu items here
                }
            }

            // Add more ToolButtons for other menus
        }
    }
}
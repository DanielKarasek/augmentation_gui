
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import AugmentationThingie


Rectangle {
    id: augmentPreviewContainer
    x: 0
    y: 100
    color: "#444444"
    Layout.fillWidth: true

    radius: 20
    Layout.preferredWidth: parent.width*0.6
    Layout.fillHeight: true
    TableView {
        id: augmentPreviewSubContainer

        anchors.fill: parent
        anchors.leftMargin: 20
        anchors.rightMargin: 20
        anchors.topMargin: 20
        anchors.bottomMargin: 20
        model: imageTableModel
        clip: true
        ScrollBar.vertical: ScrollBar {
            active: true
            width: 10
            contentItem: Rectangle {
                implicitWidth: 8
                radius: 4
                color: "grey"
            }

        }
        ScrollBar.horizontal: ScrollBar {
            active: true
            height: 10
            contentItem: Rectangle {
                implicitHeight: 8
                radius: 4
                color: "grey"
            }

        }
        delegate: Item {
            implicitWidth: 264
            implicitHeight: 264
            Loader {
                anchors.fill: parent
                anchors.margins: 10 // adjust this value to change the spacing between items

                sourceComponent: imageComponent
                property var imageSource: model.image_source
            }
            Component {
                id: imageComponent

                Image {
                    anchors.fill: parent
                    source: "image://image_provider/" + imageSource + "?id=" + Math.random()

                    MouseArea {
                        anchors.fill: parent

                        cursorShape: Qt.OpenHandCursor
                        onClicked: {
                            imagePopup.imageSource = imageSource
                            imagePopup.open()
                            }
                    }
                }
            }
        }
    }
}
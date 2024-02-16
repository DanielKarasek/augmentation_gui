import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import AugmentationThingie

ColumnLayout {

    Layout.fillWidth: true
    Layout.fillHeight: true
    PipelineView {
        id: pipelineView
        model: backendModel.treeModel
    }
    RowLayout {
        spacing: 5
        Button {
            Layout.fillWidth: true
            Layout.preferredWidth: parent.width/3
            background: Rectangle {
                color: "#ff8500"
                border.width: 0
                radius: 5
            }
            onPressed: {
                background.color = "#cc7000" // Change color to a darker shade
            }
            onReleased: {
                background.color = "#ff8500" // Change color back to original
            }
            onClicked: {
                backendModel.create_augmented_examples()
            }
            text: "Preview augmentations"
            contentItem: Text
            {
                text: parent.text
                color: "#ffffff"
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                font.pointSize: 14
                font.weight: Font.DemiBold
            }
        }

        // Button {
        //     Layout.fillWidth: true
        //     Layout.preferredWidth: parent.width/3
        //     text: "save"
        //     onClicked: {
        //         savePipelineFileDialog.open()
        //     }
        // }
        // Button {
        //     Layout.fillWidth: true
        //     Layout.preferredWidth: parent.width/3
        //     text: "load"
        //     onClicked: {
        //         loadPipelineFileDialog.open()
        //     }
        // }
    }
}
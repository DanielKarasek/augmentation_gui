// Copyright (C) 2021 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only

import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Dialogs
import AugmentationThingie

Window {
    width: 1920
    height: 1080
    visible: true
    color: "#000000ff"
    title: "AugmentationThingie"
    
    FileDialog {
        id: savePipelineFileDialog
        title: "Save File"
        fileMode: FileDialog.SaveFile
        nameFilters: ["Model files (*.json)"]
        selectedFile: "default.json"
        onAccepted: {
            backendModel.save_model_to_file(savePipelineFileDialog.selectedFile)
        }
    }
    FileDialog{
        id: loadPipelineFileDialog
        title: "Load File"
        fileMode: FileDialog.ExistingFile
        nameFilters: ["Model files (*.json)"]
        onAccepted: {
            backendModel.load_model(loadPipelineFileDialog.selectedFile)
        }
    }

    FolderDialog{
        id: loadDatasetFolderDialog
        title: "Load Dataset"
        options: FolderDialog.ReadOnly
        onAccepted: {
            backendModel.load_dataset(loadDatasetFolderDialog.selectedFolder)
        }
    }

    PopupNewAug {
        id: popupNewAug
        title: "New Pipeline"
        confirm_callback: backendModel.create_new_pipeline
    }

    Popup {
        x: 10
        y: (contentPages.height - imagePopup.height)/2 + toolbar.height + 8
        id: imagePopup
        property string imageSource
        property real minDimension: Math.min(contentPages.height - 4, contentPages.width - augmentPreviewContainer.width - 20)

        height: minDimension
        width: minDimension
        Image {
            anchors.fill: parent
            source: "image://image_provider/" + imagePopup.imageSource + "?id=" + Math.random()
        }
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

        CustomToolbar {id: toolbar}
        Rectangle {
            id: contentPages

            property var backendModel: AugmentationModel



            PopupNewAug{
                id: popupChangeName
                title: "Change pipeline name"
                confirm_callback: backendModel.change_pipeline_name
            }

            PopupMethodChoice{
                id: popupMethodChoice
                functionDatabaseModel: backendModel.functionDatabase
            }
            color: "#1d2226"
            border.color: "#1d2226"
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: toolbar.bottom
            anchors.bottom: parent.bottom
            anchors.leftMargin: 50
            anchors.rightMargin: 50
            anchors.topMargin: 0
            anchors.bottomMargin: 50

            AugmentationTitle{
                id: augmentationTitle
                popupChangeName: popupChangeName
                pipelineName: backendModel.augmentationString
            }

            RowLayout {
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: augmentationTitle.bottom
                anchors.topMargin: 0
                anchors.bottom: parent.bottom
                spacing: 40
                PipelineViewContainer{}
                FunctionDetails{functionModel: backendModel.treeModel}
                AugmentationPreview{id: augmentPreviewContainer}
            }
        }
    }
}


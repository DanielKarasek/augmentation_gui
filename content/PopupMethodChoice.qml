import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Popup {
    id: methodsPopup
    width: 200
    height: 300
    x: (parent.width - width) / 2
    y: (parent.height - height) / 2
    closePolicy: "NoAutoClose"
    clip : true

    background: Rectangle{
        width: 200
        height: 300
        color: "gray"
        border.width: 0
        radius: 10

    }
    property var chosenIndex: -1
    property bool insert_into: false
    required property var functionDatabaseModel
    modal: true
    focus: true
    padding: 0
    Rectangle {
        id: topBar
        width: parent.width
        height: 30
        color: "lightgray"
        border.width: 0

        MouseArea {
            id: dragArea
            anchors.fill: parent
            property point pressPos
            visible: true
            onPressed: (mouse) => {
                pressPos = Qt.point(mouse.x, mouse.y)
            }

            onPositionChanged: (mouse) => {
                var dx = mouse.x - pressPos.x
                var dy = mouse.y - pressPos.y
                methodsPopup.x += dx
                methodsPopup.y += dy
            }
        }

        Text {
            text: "Choose a method"
            anchors.centerIn: parent
        }
    }
    ListView {
        id: methodsList
        model: functionDatabaseModel
        property int selectedIndex: -1
        anchors.left: parent.left
        anchors.right: parent.right
        clip: true
        interactive: false
        ScrollBar.vertical: ScrollBar {
            id: scrollBar
            contentItem: Rectangle {
                id: dragHandle
                implicitWidth: 5
                radius: 2
                color: "darkgray"
            }
            MouseArea {
                id: mouseArea
                anchors.fill: parent
                hoverEnabled: true
                property real startY: 0
                onPressed: (mouse) => {
                    startY = mouse.y
                }
                onPositionChanged: (mouse) => {
                    if (!mouseArea.pressed)
                        return
                    let dy = mouse.y - startY
                    let newHandleY = dragHandle.y + dy
                    let newContentY = newHandleY / (scrollBar.height - dragHandle.height) * (methodsList.contentHeight - methodsList.height)
                    if (newContentY < 0)
                        newContentY = 0
                    else if (newContentY > methodsList.contentHeight - methodsList.height)
                        newContentY = methodsList.contentHeight - methodsList.height
                    methodsList.contentY = newContentY
                }
                onReleased: {
                    startY = 0
                }

                onEntered: {
                    colorAnimation.from = "darkgray";
                    colorAnimation.to = "lightgray";
                    colorAnimation.start();
                }

                onExited: {
                    colorAnimation.from = "lightgray";
                    colorAnimation.to = "darkgray";
                    colorAnimation.start();
                }
                ColorAnimation {
                    id: colorAnimation
                    target: dragHandle
                    property: "color"
                    from: "gray"
                    to: "lightgray"
                    duration: 200
                }

            }
        }

        delegate: Item {
            width: methodsList.width
            height: 30
            Rectangle {
                anchors.fill: parent
                color: index === methodsList.selectedIndex ? "lightblue" : "transparent" // Change the color based on whether the item is selected

            }


            Text {
                text: modelData.name
                color: "white"
                anchors.centerIn: parent
            }

            MouseArea
            {
                anchors.fill: parent
                onClicked: methodsList.selectedIndex = index // Set the selectedIndex to the index of the clicked item
                onWheel: (wheel) => {
                    if (wheel.angleDelta.y > 0)
                    {
                        if (methodsList.contentY < 20)
                            methodsList.contentY = 0
                        else
                            methodsList.contentY -= 20
                    }
                    else
                    {
                        if (methodsList.contentY > methodsList.contentHeight - methodsList.height - 20)
                            methodsList.contentY = methodsList.contentHeight - methodsList.height
                        else
                            methodsList.contentY += 20
                    }
                }
            }


        }
        anchors.leftMargin: 0
        anchors.rightMargin: 0
        anchors.topMargin: 0
        anchors.bottomMargin: 0
        anchors.top: topBar.bottom
        anchors.bottom: buttonsRow.top

    }
    RowLayout {
        id: buttonsRow
        width: parent.width
        height: buttonAdd.height
        anchors.bottom: parent.bottom
        anchors.horizontalCenter: parent.horizontalCenter
        spacing: 0

        Button {
            id: buttonAdd
            text: "Add"
            Layout.fillWidth: true
            width: parent.width / 2
            onClicked: {
                let x = methodsList.model[methodsList.selectedIndex].get_function_model(true);
                console.log(chosenIndex, x, insert_into);
                backendModel.treeModel.addItemAtIndex(chosenIndex, x, insert_into);
            }
        }
        Button {
            id: buttonCancel
            text: "Cancel"
            Layout.fillWidth: true
            width: parent.width / 2
            onClicked: {
                methodsPopup.close()
            }
        }
    }

}

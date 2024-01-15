
import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle{
    id: root
    property var title: "Change Value"
    required property var constraints
    required property var value
    height: rowLayout.height + titleLabel.height + 5
    color: "transparent"
    Label {
        id: titleLabel
        anchors.left: parent.left
        anchors.right: parent.right // Set your title text here
        color: "#ffffff"
        text: title
        anchors.top: parent.top
        anchors.leftMargin: 0
        anchors.rightMargin: 0
    }
    RowLayout {
        id: rowLayout
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: titleLabel.bottom
        anchors.bottom: parent.bottom
        spacing: 5
        anchors.topMargin: 5
        Slider {
            id: slider

            width: 188
            height: 31
            value: root.value
            live: true
            Layout.fillWidth: true
            Layout.fillHeight: true
            from: constraints.min_value
            to: constraints.max_value
            stepSize: constraints.step_size
            onValueChanged:
            {
                root.value = slider.value;
            }
        }
        ParameterValueTextField
        {
            id: sliderValue2
            text: slider.value.toFixed(2)
            value_constraints: root.constraints
            onTextChangedSuccessfully:
            {
                slider.value = parseFloat(text);
                root.value = parseFloat(text);
            }
        }
    }
}


import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

Rectangle{
    id: root
    property var title: "Change Value"
    required property var constraints
    required property var value
    height: rowLayout.childrenRect.height + titleLabel.height + 5
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
            value: root.value
            live: true
            Layout.fillWidth: true // Slider will take up the rest of the available space
            Layout.fillHeight: true
            Layout.minimumWidth: 180
            from: constraints.min_value
            to: constraints.max_value
            stepSize: constraints.step_size
            onValueChanged:
            {
                if (constraints.data_type === "int")
                {
                    sliderValue2.text = parseInt(slider.value);
                    root.value = parseInt(slider.value);

                }
                else if (constraints.data_type === "float")
                {
                    sliderValue2.text = slider.value.toFixed(2);
                    root.value = parseFloat(slider.value);
                }
            }
        }
        ParameterValueTextField
        {
            id: sliderValue2
            text: slider.value.toFixed(2)
            value_constraints: root.constraints
            onTextChangedSuccessfully:
            {
                console.log("text changed successfully");
                if (constraints.data_type === "int")
                {
                    slider.value = parseInt(text);
                    root.value = parseInt(text);
                }
                else if (constraints.data_type === "float")
                {
                    slider.value = parseFloat(text);
                    root.value = parseFloat(text);
                }
            }
        }
    }
}

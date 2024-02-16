import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

TextField {
    signal textChangedSuccessfully(string newText) // Declare the signal

    id: sliderValue
    horizontalAlignment: Text.AlignHCenter // Align the text horizontally to the center
    verticalAlignment: Text.AlignVCenter // Align the text vertically to the center
    Layout.minimumWidth: 60
    Layout.maximumWidth: 60
    Layout.minimumHeight: 30
    Layout.maximumHeight: 30
    Layout.fillHeight: true
    Layout.fillWidth: true
    Layout.alignment: Qt.AlignCenter
    background: Rectangle {
        color: "#494949"
    }
    color: "#ffffff"
    text: "val"
    property string previous_valid_value: text
    selectedTextColor: "#ffffff"
    selectionColor: "#5e9dfc"
    placeholderTextColor: "#000000"
    placeholderText: qsTr("value")

    required property var value_constraints
    validator: RegularExpressionValidator
    {
        id: doubleChecker
        regularExpression: value_constraints.data_type === "float"  ? new RegExp("^-?[0-9]+([.][0-9]{1,2})?$") : new RegExp("^-?[0-9]+$")
    }
    property int decimal: value_constraints.data_type === "float" ? 2 : 0
    onEditingFinished:
            {
                let value = parseFloat(text);
                if (isNaN(value))
                {
                    text = previous_valid_value;
                    return
                }
                if ( value < value_constraints.min_value)
                    text = value_constraints.min_value.toFixed(decimal);
                else if (value > value_constraints.max_value)
                    text = value_constraints.max_value.toFixed(decimal);
                else
                    text = value.toFixed(decimal);
                previous_valid_value = text;
                textChangedSuccessfully(text); // Emit the signal

            }
    Component.onCompleted: {
        previous_valid_value = text;
    }

}

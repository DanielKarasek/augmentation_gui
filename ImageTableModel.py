from PySide6.QtCore import QAbstractTableModel, Qt, QByteArray
from PySide6.QtGui import QImage
from PySide6.QtQuick import QQuickImageProvider


class ImageProvider(QQuickImageProvider):
    def __init__(self, image_data):
        super().__init__(QQuickImageProvider.Image)

        self._image_data = image_data

    def requestImage(self, id, size, requested_size):
        try:
            row, col = id.split(',')
        except ValueError:
            return QImage()
        col = col.split('?')[0]
        row, col = int(row), int(col)
        image = QImage(self._image_data[row][col].data.tobytes(),
                       self._image_data[row][col].shape[1],
                       self._image_data[row][col].shape[0],
                       QImage.Format_RGB888)
        return image

    def setImageData(self, image_data):
        self._image_data = image_data


class ImageTableModel(QAbstractTableModel, QQuickImageProvider):
    ImageRole = Qt.UserRole + 1

    def __init__(self, image_data, parent=None):
        super(ImageTableModel, self).__init__(parent)
        self._image_data = image_data
        self._image_provider = ImageProvider(image_data)

    def rowCount(self, parent=None):
        return len(self._image_data)

    def columnCount(self, parent=None):
        return len(self._image_data[0]) if self._image_data else 0

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid() and role == self.ImageRole:
            return f"{index.row()},{index.column()}"

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                return f"Column {section}"
            else:
                return f"Row {section}"

    def roleNames(self):
        roles = super().roleNames()
        roles[ImageTableModel.ImageRole] = QByteArray(b'image_source')
        return roles

    def setImageData(self, image_data):
        self.beginResetModel()
        self._image_data = image_data
        self._image_provider.setImageData(image_data)
        self.endResetModel()


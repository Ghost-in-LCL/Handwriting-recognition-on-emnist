import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from bin.gui import Ui_MainWindow
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt
from PIL import ImageGrab
from tensorflow import keras
import numpy as np
from bin import model2
from bin.model2 import train_model


class MyWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setMouseTracking(False)

        self.pos_xy = []

    def paintEvent(self, event):
        painter1 = QPainter(self)
        painter1.setBrush(Qt.white)
        painter1.drawRect(self.rect())
        painter = QPainter()
        painter.begin(self)
        pen = QPen(Qt.black, 10, Qt.SolidLine)
        painter.setPen(pen)
        if len(self.pos_xy) > 1:
            point_start = self.pos_xy[0]
            for pos_tmp in self.pos_xy:
                point_end = pos_tmp
                if point_end == (-1, -1):
                    point_start = (-1, -1)
                    continue
                if point_start == (-1, -1):
                    point_start = point_end
                    continue
                painter.drawLine(point_start[0], point_start[1], point_end[0], point_end[1])
                point_start = point_end
        painter.end()
        return

    def mouseMoveEvent(self, event):
        pos_tmp = (event.pos().x(), event.pos().y())
        self.pos_xy.append(pos_tmp)
        self.update()
        return

    def mouseReleaseEvent(self, event):
        pos_test = (-1, -1)
        self.pos_xy.append(pos_test)
        self.update()
        return

    def cls(self):
        self.pos_xy = []
        self.update()
        self.label_4.setText("")
        return

    def solve(self):
        bbox = (self.x() + 31, self.y() + 41, self.x() + 299, self.y() + 299)
        im = ImageGrab.grab(bbox)
        img = im.convert("L")
        img = img.resize((28, 28))
        imarr = 255-np.array(img)
        imarr = imarr/255.0
        imarr = imarr.reshape((1, 28, 28))
        # model = keras.models.load_model("model/model.h5")
        model = keras.models.load_model("test/test.h5")

        pre = model.predict(imarr)
        classes = np.argmax(pre, axis=1)
        self.label_4.setNum(classes[0])
        return


if __name__ == "__main__":
    app = QApplication(sys.argv)
    form = MyWindow()
    form.show()
    form.pushButton.clicked.connect(form.cls)
    form.pushButton_2.clicked.connect(form.solve)
    app.exec()

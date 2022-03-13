from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen


class SlideIndicator(QWidget):

    def __init__(self, limits):
        super(SlideIndicator, self).__init__()
        self.set_rails(limits)
        self.value = None
        self.setGeometry(2000, 200, 200, 30)
        self.setWindowTitle('Slide Indicator')

    def paintEvent(self, e):
        qp = QPainter()
        qp.begin(self)
        self.draw_grid(qp)
        self.draw_pointer(qp)
        qp.end()

    def draw_grid(self, qp):
        pen = QPen(Qt.gray, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(0, self.height() - 1, self.width(), self.height() - 1)
        pen.setStyle(Qt.CustomDashLine)
        pen.setDashPattern([1, self.width() / 8.1 - 1])
        qp.setPen(pen)
        qp.drawLine(0, self.height() - 2, self.width(), self.height() - 2)
        qp.drawLine(0, self.height() - 3, self.width(), self.height() - 3)

    def draw_pointer(self, qp):
        pen = QPen(Qt.red, 2, Qt.SolidLine)
        qp.setPen(pen)
        if self.value is not None:
            xpos = (self.value - self.minvalue) / self.span * self.width()
            qp.drawLine(xpos, self.height() - 15, xpos, self.height() - 2)

    def set_rails(self, rails):
        self.minvalue = rails[0]
        self.maxvalue = rails[1]
        self.span = self.maxvalue - self.minvalue
        self.repaint()

    def update_slider(self, value):
        if value >= self.maxvalue:
            value = self.maxvalue
        elif value <= self.minvalue:
            value = self.minvalue
        self.value = value
        self.repaint()


if __name__ == "__main__":
    from EGGS_labrad.clients import runGUI
    runGUI(SlideIndicator, limits=[-5.0, 5.0])
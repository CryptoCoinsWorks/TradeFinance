import webbrowser
from PySide2 import QtWidgets, QtGui

class LabelTitle(QtWidgets.QLabel):
    def __init__(self, link=None, size=20):
        super(LabelTitle, self).__init__()

        # self.font = "Marianne"
        self.fontDB = QtGui.QFontDatabase()
        self.fontDB.addApplicationFont(":/font/Marianne/fontes_desktop/Marianne-Bold.otf")
        self.font = "Marianne"
        self.set_font_size(size)

    def set_font_size(self, size):
        self.setFont(QtGui.QFont(self.font, size))

    def set_link(self, link):
        self.link = link

    def mousePressEvent(self, event) -> None:
        webbrowser.open(self.link)

from PySide2 import QtGui, QtCore, QtWidgets
from libs.events_handler import EventHandler
from libs.widgets.article_itemwidget import ArticlesWidgetItem


class FillListThread(QtCore.QThread):
    def __init__(self, parent=None, articles=None):
        super(FillListThread, self).__init__(parent=parent)

        self.signal = EventHandler()
        self.articles = articles
        self.parent = parent

    def fill_list(self):
        """This method create an item for the list and emit a signal with it
        """
        self.msleep(500)
        try:
            for article in self.articles:
                # article = ArticlesWidgetItem(article=article)
                self.signal.sig_new_item.emit(article)
                self.usleep(100)
        except Exception as error:
            raise error
        finally:
            self.quit()

    def run(self):
        self.fill_list()

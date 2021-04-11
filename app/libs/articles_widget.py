#
# This class set all the articles from a selected compagny.
#

from pprint import pprint
from PySide2 import QtWidgets, QtCore
from libs.events_handler import EventHandler
from libs.thread_list import FillListThread
from libs.thread_pool import ThreadPool
from libs.articles.yahoo_articles import ArticlesYahoo
from libs.widgets.article_itemwidget import ArticlesWidgetItem

class ArticlesWidget(QtWidgets.QListWidget):
    def __init__(self, parent=None, ticker=None):
        super(ArticlesWidget, self).__init__(parent)

        self.signal = EventHandler()
        self.thread_pool = ThreadPool()

        self.thread_pool.signals.sig_thread_result.connect(
            self.teseeeet
        )

    @QtCore.Slot(str)
    def _on_get_articles(self, ticker):
        # articles = self._get_articles_dict(ticker=ticker)
        self.articles = self.thread_pool.execution(
            function=self._get_articles_dict,
            ticker=ticker
        )
        self.clear()

    @QtCore.Slot()
    def teseeeet(self, articles):
        self.thread_list = FillListThread(articles=articles)
        self.thread_list.start()
        self.thread_list.signal.sig_new_item.connect(self.article)

    @QtCore.Slot(object)
    def article(self, articles):
        item = QtWidgets.QListWidgetItem()
        article = ArticlesWidgetItem(article=articles)
        item.setSizeHint(article.sizeHint())
        self.addItem(item)
        self.setItemWidget(item, article)

    def _get_articles_dict(self, ticker):
        article = ArticlesYahoo()
        return article.get_articles_from_compagny(ticker=ticker)



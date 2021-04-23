#
# This class set the default Welcome Page.
#
from pprint import pprint
from PySide2 import QtWidgets
from utils import constants as cst
from libs.articles.yahoo_articles import ArticlesYahoo
from libs.widgets.article_itemwidget import ArticlesWidgetItem


class WelcomeWidget(QtWidgets.QListWidget):
    """
    This is loading all articles from the main Yahoo Page.
    https://finance.yahoo.com/
    """
    def __init__(self, parent=None):
        super(WelcomeWidget, self).__init__(parent)

        articles = self._get_articles_dict()[:5]

        if not cst.DEV:
            for index, article in enumerate(articles):
                article = ArticlesWidgetItem(parent=self,
                                             article=article
                                             )
                item = QtWidgets.QListWidgetItem()
                item.setSizeHint(article.sizeHint())
                self.addItem(item)
                self.setItemWidget(item, article)

    def _get_articles_dict(self):
        article = ArticlesYahoo()
        return article.get_home_articles()




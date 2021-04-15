import os
from utils import utils
from ui.article import Ui_Article
from libs.thread_pool import ThreadPool
from PySide2 import QtWidgets, QtCore, QtGui


class ArticlesWidgetItem(QtWidgets.QWidget, Ui_Article):
    def __init__(self, parent=None, article=None):
        super(ArticlesWidgetItem, self).__init__(parent)
        self.setupUi(self)

        self.thread_pool = ThreadPool()
        self.thread_pool.signals.sig_thread_result.connect(
            self._on_thumbnail_available
        )

        self.set_title(article["title"], article["link"])
        self.set_date(article["published"])
        self.set_description(article["summary"])
        self.set_thumbnail(article["img"])

    def set_compagny(self, text):
        """
        Set Compagny name on the article.
        """
        self.lb_compagny.setText(text)
        self.lb_compagny.setFont(QtGui.QFont("Times", 12))

    def set_title(self, text, link):
        """
        Set Title of the article and link clickable.
        """
        self.lb_title.setText(text)
        self.lb_title.set_link(link)
        self.lb_title.set_font_size(size=14)

    def set_date(self, text):
        """
        Set date published article.
        """
        self.lb_date.setText(text)

    def set_description(self, text):
        """
        Set description of the article.
        """
        self.desc.setText(text)
        self.desc.setFont(QtGui.QFont("Times", 10))

    def set_thumbnail(self, link):
        if link:
            self.thread_pool.execution(
                function=utils.get_image_from_url, url=link
            )
        else:
            image = QtGui.QPixmap(":/img/no_file.png").scaled(self.size(),
                                                              QtCore.Qt.KeepAspectRatio,
                                                              QtCore.Qt.SmoothTransformation
                                                              )
            self.thumbnail.setPixmap(image)

    @QtCore.Slot(object)
    def _on_thumbnail_available(self, image):
        """Called when a thumbnail is available for the company

        :param image: The thumbnail
        :type image: QPixmap
        """
        image = image.scaled(self.size(),
                             QtCore.Qt.KeepAspectRatio,
                             QtCore.Qt.SmoothTransformation
                             )
        self.thumbnail.setPixmap(image)

import os
import json

from PySide2 import QtCore
from utils import constants as cst
from utils import db_models
from libs.events_handler import EventHandler


class FavoritesManager(QtCore.QObject):
    def __init__(self, parent):
        super(FavoritesManager, self).__init__(parent)

        # Constants
        self.signals = EventHandler()

        self.db_connection = db_models.connection_to_db(cst.DATABASE)
        self._favorites = []

    def load_favorite(self) -> list:
        """Load favorite from the file

        :return: The loaded favorite
        :rtype: list
        """
        if not cst.LOGIN:
            return self._favorites
        self._favorites = db_models.get_favorite_for_user(self.db_connection)
        self.signals.sig_favorite_loaded.emit(self._favorites)
        return self._favorites

    def save_favorites(self):
        """Save favorites into the file"""
        for favorite in self._favorites:
            db_models.add_favorite(self.db_connection,
                                   favorite['ticker'],
                                   favorite['name'])
        self.signals.sig_favorite_saved.emit(self._favorites)

    def add_ticker_favorite(self, ticker_data: dict):
        """Add a new ticker to the favorite

        :param ticker_data: The ticker to add
        :type ticker_data: dict
        """
        self._favorites.append(ticker_data)
        self.signals.sig_favorite_added.emit(ticker_data)

    def remove_ticker_favorite(self, ticker_data: dict):
        """Remove a ticker from the favorite

        :param ticker_data: The ticker to remove
        :type ticker_data: dict
        """
        if ticker_data in self._favorites:
            self._favorites.remove(ticker_data)
            db_models.remove_fav(self.db_connection, ticker=ticker_data['ticker'],name=ticker_data['name'])
            self.signals.sig_favorite_removed.emit(ticker_data)

    @QtCore.Slot(dict)
    def _on_add_ticker_favorite(self, ticker_data):
        """Called when a ticker is added to favorite

        :param ticker_data: The added ticker
        :type ticker_data: dict
        """
        self.add_ticker_favorite(ticker_data=ticker_data)

    @QtCore.Slot(dict)
    def _on_remove_ticker_favorite(self, ticker_data: dict):
        """Called when a ticker is removed from favorite

        :param ticker_data: The removed ticker
        :type ticker_data: dict
        """
        self.remove_ticker_favorite(ticker_data=ticker_data)

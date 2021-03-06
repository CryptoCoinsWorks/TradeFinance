import os
import json
import uuid
import random
import datetime
import urllib.request
from utils import constants as cst
from statistics import mean
from modules.yahoo_fin import stock_info as sf
from resources.style import style

from sklearn import preprocessing
import numpy as np
import pandas as pd
from scipy import signal

from PySide2.QtGui import QPixmap
from PySide2.QtWidgets import QApplication
from PySide2 import QtCore, QtWidgets, QtGui


def message_popup(widget, message=""):
    """Create a pop Warning Message
    """
    msg = QtWidgets.QMessageBox.warning(widget, "Warning", message)
    return msg


def normalize_data(data):
    data = data.reshape(1, -1)
    normalized = preprocessing.normalize(np.nan_to_num(data))
    return normalized


def savgol_filter(values, window_length, polyorder=3):
    """Just a savgol filter wrapper

    :param values: The data to be filtered.
    :type values: np.array
    :param window_length: The length of the filter window
    :type window_length: int
    :param polyorder: The order of the polynomial used to fit the samples, defaults to 3
    :type polyorder: int, optional
    :return: The filtered data.
    :rtype: np.array
    """
    return signal.savgol_filter(
        x=values,
        window_length=window_length,
        polyorder=polyorder,
        mode="interp",
    )


def remove_nan(data):
    """
    This method replace Nan value by 0.
    Sinon return float.
    :param data:
    :return: List
    """
    data_format = []
    for i in data:
        if str(i) == "nan":
            i = 0
        data_format.append(float(i))
    return data_format


def _peaks_detection(values, rounded=3, direction="up"):
    """Peak detection for the given data.

    :param values: All values to analyse
    :type values: np.array
    :param rounded: round values of peaks with n digits, defaults to 3
    :type rounded: int, optional
    :param direction: The direction is use to find peaks.
    Two available choices: (up or down), defaults to "up"
    :type direction: str, optional
    :return: The list of peaks founded
    :rtype: list
    """
    data = np.copy(values)
    if direction == "down":
        data = -data
    peaks, _ = signal.find_peaks(data, height=min(data))
    if rounded:
        peaks = [abs(round(data[val], rounded)) for val in peaks]
    return peaks


def get_resistances(values, closest=2):
    """Get resistances in values

    :param values: Values to analyse
    :type values: np.array
    :param closest: The value for grouping. It represent the max difference
    between values in order to be considering inside the same
    bucket, more the value is small, more the result will be precises.
    defaults to 2
    :type closest: int, optional
    :return: list of values which represents resistances
    :rtype: list
    """
    return _get_support_resistances(
        values=values, direction="up", closest=closest
    )


def get_supports(values, closest=2):
    """Get supports in values

    :param values: Values to analyse
    :type values: np.array
    :param closest: The value for grouping. It represent the max difference
    between values in order to be considering inside the same
    bucket, more the value is small, more the result will be precises.
    defaults to 2
    :type closest: int, optional
    :return: list of values which represents supports
    :rtype: list
    """
    return _get_support_resistances(
        values=values, direction="down", closest=closest
    )


def _get_support_resistances(values, direction, closest=2):
    """Private function which found all supports and resistances

    :param values: values to analyse
    :type values: np.array
    :param direction: The direction (up for resistances, down for supports)
    :type direction: str
    :param closest: closest is the maximun value difference between two values
    in order to be considering in the same bucket, default to 2
    :type closest: int, optional
    :return: The list of support or resistances
    :rtype: list
    """
    result = []
    # Find peaks
    peaks = _peaks_detection(values=values, direction=direction)
    # Group by nearest values
    peaks_grouped = group_values_nearest(values=peaks, closest=closest)
    # Mean all groups in order to have an only one value for each group
    for val in peaks_grouped:
        if not val:
            continue
        if len(val) < 3:  # need 3 values to confirm resistance
            continue
        result.append(mean(val))
    return result


def group_values_nearest(values, closest=2):
    """Group given values together under multiple buckets.

    :param values: values to group
    :type values: list
    :param closest: closest is the maximun value difference between two values
    in order to be considering in the same bucket, defaults to 2
    :type closest: int, optional
    :return: The list of the grouping (list of list)
    :rtype: list    s
    """
    values.sort()
    il = []
    ol = []
    for k, v in enumerate(values):
        if k <= 0:
            continue
        if abs(values[k] - values[k - 1]) < closest:
            if values[k - 1] not in il:
                il.append(values[k - 1])
            if values[k] not in il:
                il.append(values[k])
        else:
            ol.append(list(il))
            il = []
    ol.append(list(il))
    return ol


def find_method(module, obj):
    """Return the method obj for the given string module

    >>> module = "wgt_graph.hello_world"
    >>> obj = self
    >>> find_method(module, obj)
    >>> <bound method ... >

    :param module: The module to find
    :type module: string
    :param obj: The object source
    :type obj: object
    :return: The module found
    :rtype: object
    """
    _module, sep, rest = module.partition(".")
    if getattr(obj, _module):
        obj = getattr(obj, _module)

        if sep:
            obj = find_method(module=rest, obj=obj)
    else:
        return None
    return obj


def convert_date_to_timestamp(data):
    final = []
    for date in data.index:
        _date = datetime.datetime.strptime(date, "%Y-%m-%d")
        timestamp = datetime.datetime.timestamp(_date)
        final.append(timestamp)
    return final


def convert_timestamp_to_date(timestamp: int) -> object:
    """Convert a timestamp to a datetime object

    :param timestamp: The timestamp to convert
    :type timestamp: int
    :return: The datetime resulted from the conversion
    :rtype: object
    """
    return datetime.datetime.fromtimestamp(timestamp)


def get_image_from_url(url: str) -> QPixmap:
    """Get an image on the web and return a Qpixmap

    :param url: The url to request
    :type url: str
    :return: The image
    :rtype: QtGui.QPixmap
    """
    data = urllib.request.urlopen(url).read()
    image = QPixmap()
    image.loadFromData(data)
    return image


def get_main_window_instance(name: str = "MainWindow"):
    """Get the main window object

    :param name: The name of the main window, defaults to "MainWindow"
    :type name: str, optional
    :return: The main window object
    :rtype: object
    """
    top_widgets = QApplication.topLevelWidgets()
    for widget in top_widgets:
        if widget.objectName() != name:
            continue
        return widget
    return None


def get_all_tickers():
    """
    This method return a dict of all the compagny for each markets.
    """
    try:
        dow = sf.tickers_dow()
        cac = sf.tickers_cac()
        sp500 = sf.tickers_sp500()
        nasdaq = sf.tickers_nasdaq()

        data = {}
        for i in [cac, dow, nasdaq, sp500]:
            data.update(i)

    except:
        SCRIPT_PATH = os.path.dirname(os.path.dirname(__file__))
        with open(os.path.join(SCRIPT_PATH, "data", "dataset.json"), "r") as f:
            data = json.load(f)

    return data


def exp_moving_average(values, w):
    weights = np.exp(np.linspace(-1.0, 0.0, w))
    weights /= weights.sum()
    a = np.convolve(values, weights, mode="full")[: len(values)]
    a[:w] = a[w]
    return a


def rolling_mean(values, length):
    """Find the rolling mean for the given data dans the given length

    :param values: All values to analyse
    :type values: np.array
    :param length: The length to calculate the mean
    :type length: int
    :return: The rolling mean
    :rtype: np.array
    """
    ret = np.cumsum(values, dtype=float)
    ret[length:] = ret[length:] - ret[:-length]
    mva = ret[length - 1:] / length

    # Padding
    padding = np.array([np.nan for i in range(length)])
    mva = np.append(padding, mva)

    return mva


def get_compagny_name_from_tick(ticker):
    """
    This method return the Compagny name for his ticker.
    """

    data = get_all_tickers()

    for tick, company in data.items():
        if ticker.startswith(tick):
            return company


def get_last_value(data):
    if data[0] != 0:
        index = 0
        value = data[index]
    else:
        index = 1
        value = data[index]
    return value, index


def format_data(data):
    """
    This method format number with ','.
    exemple:  2,120,350
    :param data:
    :return: List of string
    """
    data_format = []
    for i in remove_nan(data):
        i = f"{int(i):,}"
        data_format.append(i)
    return data_format


def get_rdm_tickers(qty=5):
    """
    This method get a quantity of randoms tickers.
    return: list
    """
    all_tickers = get_all_tickers().keys()
    tickers = random.sample(all_tickers, qty)
    return tickers


def check_french_ticker(ticker):
    """This method split the ticker if endswith '.PA'
    :return: str
    """
    try:
        ticker = ticker.split('.')[0]
    except:
        pass

    return ticker


def clear_layout(layout):
    """
    This method remove all widgets inside a layout.
    :param: QtLayout
    """
    for i in reversed(range(layout.count())):
        layout.itemAt(i).widget().setParent(None)


def get_compagnies_from_secteurs(industry):
    """This method return a list of compagnies from
       the activity sector.
    """
    SCRIPT_PATH = os.path.dirname(__file__)
    with open(os.path.join(SCRIPT_PATH, "data", "industries.json"), "r") as f:
        same = json.load(f)

    for indu, tickers in same.items():
        if industry == indu:
            return tickers

def get_compagny_yield():
    """This method get the % AAA Corporate.
    """
    link = cst.AAA_YIELD_link
    yield_ = pd.read_html(link, header=0)[10].keys()[1]
    yield_ = float(str(yield_.replace('%', '')))
    return yield_

def file_from_path(path):
    if not os.path.exists(os.path.dirname(path)):
        try:
            os.mkdir(os.path.dirname(path))
            return True
        except Exception as error:  # TODO cath correct error
            print(error)
            return False
    if not os.path.exists(path):
        open(path, "w")
    return True
import os
import sys


def resoure_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    # base_path = getattr(
    #     sys,
    #     '_MEIPASS',
    #     os.path.dirname(os.path.abspath(__file__)))
    # return os.path.join(base_path, relative_path)

    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)
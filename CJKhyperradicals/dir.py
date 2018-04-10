import os, sys
import inspect

PROJECT_NAME = 'CJKhyperradicals'
MODULE_ROOT = os.path.abspath(os.path.dirname(inspect.getframeinfo(inspect.currentframe()).filename))


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a tmp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.environ.get("_MEIPASS2", os.path.dirname(MODULE_ROOT))

    return os.path.join(base_path, PROJECT_NAME, relative_path)


def tmp_path(data):
    return resource_path(os.path.join('tmp', data))


def database_path(data):
    return resource_path(os.path.join('database', data))


def chinese_path(data):
    return resource_path(os.path.join('database', 'chinese', data))


def japanese_path(data):
    return resource_path(os.path.join('database', 'japanese', data))

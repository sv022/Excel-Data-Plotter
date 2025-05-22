import ctypes
import locale


def get_locale():
    windll = ctypes.windll.kernel32
    windll.GetUserDefaultUILanguage()
    return locale.windows_locale[ windll.GetUserDefaultUILanguage() ]

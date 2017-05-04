"""
fog node prototype
"""
__version__ = '0.0.1'
__author__ = 'Markus Paeschke'


class ExitStatus:
    """Exit status code constants."""
    OK = 0
    ERROR = 1
    PLUGIN_ERROR = 7

    # 128+2 SIGINT <http://www.tldp.org/LDP/abs/html/exitcodes.html>
    ERROR_CTRL_C = 130

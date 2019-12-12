# coding=utf-8

"""Hello world demo module"""
import sys
from PySide2.QtWidgets import QApplication
from sksurgerycore.configuration.configuration_manager import (
        ConfigurationManager
        )
from sksurgeryeval.widgets.overlay import OverlayApp

def run_demo(configfile, verbose):
    """ Run the application """

    configurer = ConfigurationManager(configfile)

    app = QApplication([])

    configuration = configurer.get_copy()

    if verbose:
        print("Starting overlay app")

    overlay = OverlayApp(configuration)
    overlay.start()

    sys.exit(app.exec_())

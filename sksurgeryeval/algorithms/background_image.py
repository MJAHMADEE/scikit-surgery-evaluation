"""
A class to provide the background image
"""
from numpy import zeros, uint8
from sksurgeryimage.utilities.weisslogo import WeissLogo

class OverlayBackground():
    """
    Provides the background image for the overlay
    window.
    """

    def __init__(self, config):
        """
        Initialises and configures class to provide a background image.
        Image can be a WEISS logo, or blank.
        :param: A configuration dictionary
        :raises: RunTimeError, KeyError
        """
        self._logo_maker = None
        self._blank_image = None
        if config.get("logo"):
            self._logo_maker = WeissLogo()
        else:
            self._blank_image = zeros(shape=[512, 512, 3], dtype=uint8)

    def next_image(self):
        """
        Returns a background image.
        The behaviour is determined by the configuration
        dictionary used at init.
        """
        if self._logo_maker is not None:
            image = self._logo_maker.get_noisy_logo()
        else:
            image = self._blank_image
        return image

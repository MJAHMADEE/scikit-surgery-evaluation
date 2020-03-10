# coding=utf-8

"""Main loop for surgery evaluation"""
from math import isnan
from sksurgeryutils.common_overlay_apps import OverlayBaseApp
from sksurgeryeval.algorithms.algorithms import (
        configure_tracker, np2vtk, add_map)
from sksurgeryeval.algorithms.background_image import \
        OverlayBackground
from sksurgeryeval.shapes.cone import VTKConeModel
from sksurgeryeval.algorithms.locators import Locators
from sksurgeryeval.logging.surgery_logger import Logger


class OverlayApp(OverlayBaseApp):
    """Inherits from OverlayBaseApp, adding code to test the
    proximity of a tracked object to a set of vtk objects"""

    def __init__(self, config):
        """Overides overlay base app's init, to initialise the
        external tracking system. Together with a video source"""
        try:
            super().__init__(None)
        except RuntimeError:
            self.update_rate = 30
            self.img = None
            self.timer = None
            self.save_frame = None

        self._logger = Logger(config)
        if "logo" in config:
            self.bg_image = OverlayBackground(config)
        else:
            default_config = {"logo" : True}
            self.bg_image = OverlayBackground(default_config)

        self._tracker = None
        if "tracker config" in config:
            self._tracker = configure_tracker(config.get("tracker config"))

        self._tracker_handle = 0
        if "tracker handle" in config:
            self._tracker_handle = config.get("tracker handle")

        self._locator = Locators(config)
        maps = add_map(config)

        self._pointer = VTKConeModel(10.0, 5.0, (1.0, 1.0, 1.0), "pointer")
        self.vtk_overlay_window.add_vtk_actor(self._pointer.actor)
        self.vtk_overlay_window.add_vtk_models(self._locator.models)

        if maps is not None:
            self.vtk_overlay_window.add_vtk_models(maps)

        if "camera" in config:
            camera_config = config.get("camera")
            if "bounding box" in camera_config:
                self.vtk_overlay_window.foreground_renderer.ResetCamera(
                    camera_config.get("bounding box"))
            else:
                self.vtk_overlay_window.foreground_renderer.ResetCamera(
                    -300, 300, -300, 300, -200, 0)

        self.vtk_overlay_window.add_vtk_actor(self._locator._text.text_actor)

        self._logger.log(message="OverlayApp init OK")


    def update(self):
        """Update the background renderer with a new frame,
        move the model(s) and render"""
        image = self.bg_image.next_image()

        #add a method to move the pointer
        self._update_tracking()

        self.vtk_overlay_window.set_video_image(image)
        self.vtk_overlay_window.Render()

    def _update_tracking(self):
        """Internal method to move the pointer,
	and check it's distance to the various
	polydata
        """
        port_handles, _, _, tracking, quality = self._tracker.get_frame()


        for ph_index, port_handle in enumerate(port_handles):
            if port_handle != self._tracker_handle:
                continue

            if not isnan(quality[ph_index]):
                self._pointer.actor.SetUserMatrix(np2vtk(tracking[ph_index]))

                self._locator.is_hit(tracking[ph_index], self._logger)

    def __del__(self):
        self._logger.log(message="Closing overlay app")
        del self._logger

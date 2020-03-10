# coding=utf-8

"""Main loop for surgery evaluation"""
from sksurgeryvtk.text.text_overlay import VTKCornerAnnotation
from sksurgeryeval.algorithms.algorithms import (
        populate_models, point_in_locator, random_targets)



class Locators():
    """stores a list of vtk models and corresponding locators,
    and handles associated logic
    """

    def __init__(self, config):
        """Overides overlay base app's init, to initialise the
        external tracking system. Together with a video source"""

        self.models, self._locators = populate_models(config)

        for model in range(len(self.models)):
            self._set_target_inactive(model)

        self._search_radius = 10.0
        if "search radius" in config:
            self._search_radius = config.get("search radius")

        self._targets = random_targets(len(self._locators))
        self._target_index = 0
        self._set_target_active(self._targets[self._target_index])

        self._text = VTKCornerAnnotation()
        self._text.set_text(["Hello World", "", "",
                             str(self._targets[self._target_index])])

    def _set_target_active(self, index):
        self.models[index].actor.GetProperty().SetColor(1.0, 0.0, 0.0)

    def _set_target_inactive(self, index):
        self.models[index].actor.GetProperty().SetColor(1.0, 1.0, 1.0)


    def is_hit(self, tracking, logger):
        """
        Checks whether a target has been hit
        :param: the tracking data (3D point)
        :param: a logger to write notification to
        """
        index, distance = point_in_locator(tracking[0:3, 3],
                                           self._locators,
                                           self._search_radius)



        if self._target_index < len(self._locators):
            self._text.set_text([str(index), str(distance),
                                 str(tracking),
                                 str(self._targets[self._target_index])])

            if index == self._targets[self._target_index]:
                logger.log(message="Hit target:{0}".format(index))
                self._set_target_inactive(self._targets[self._target_index])
                self._target_index = self._target_index + 1
                if self._target_index < len(self._locators):
                    self._set_target_active(self._targets[self._target_index])
                else:
                    self._text.set_text([str(index), str(distance),
                                         str(tracking),
                                         str("Finished")])
                    logger.log(message="All targets hit")
        else:
            self._text.set_text([str(index), str(distance),
                                 str(tracking),
                                 str("Finished")])

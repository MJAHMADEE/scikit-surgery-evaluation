# coding=utf-8
""" Algorithms for the surgery evaluation application """
import vtk
from numpy import inf, eye
from sksurgerynditracker.nditracker import NDITracker
from sksurgeryarucotracker.arucotracker import ArUcoTracker
from sksurgeryvtk.models. vtk_surface_model_directory_loader \
        import VTKSurfaceModelDirectoryLoader
#from sksurgeryeval.shapes.cone import VTKConeModel

def point_in_locator(point, point_locators, radius=1.0):
    """
    Tests whether a point is within a set distance of any of a
    list of point locators.

    :param point: the point to test, in 3D (x,y,z)
    :param point_locators: a list of vtkPointLocators
    :param radius: optional search radius in mm (default=1.0)
    :return locator: the index of the nearest point locator,
    -1 if no locators within radius)
    :return distance: distance to nearest point_locator

    :raises: delegates to vtk
    """

    minumum_distance = inf
    locator_index = -1
    for index, locator in enumerate(point_locators):

        distance = vtk.mutable(0.0)
        if locator.FindClosestPointWithinRadius(radius, point, distance) == -1:
            continue

        if distance > minumum_distance:
            continue

        minumum_distance = distance
        locator_index = index

    return locator_index, minumum_distance


def np2vtk(mat):
    """
    Converts a Numpy array to a vtk matrix
    :param: the number array, should be 4x4
    :return: a vtk 4x4 matrix
    :raises: ValueError when matrix is not 4x4
    """
    if mat.shape == (4, 4):
        obj = vtk.vtkMatrix4x4()
        for i in range(4):
            for j in range(4):
                obj.SetElement(i, j, mat[i, j])
        return obj
    raise ValueError('Array must be 4x4')


def configure_tracker(config):
    """
    Configures the tracking system.
    :param: A dictionary containing configuration data
    :return: The tracker object
    :raises: KeyError if no tracker entry in config
    """
    if "tracker type" not in config:
        raise KeyError('Tracker configuration requires tracker type')

    tracker_type = config.get("tracker type")
    tracker = None
    if tracker_type in ("vega", "polaris", "aurora", "dummy"):
        tracker = NDITracker(config)
    if tracker_type in "aruco":
        tracker = ArUcoTracker(config)

    tracker.start_tracking()
    return tracker


def populate_models(path_name, model_to_world=eye(4, 4)):
    """
    Loads vtk models from a directory and returns
    a list of vtk actors and associated vtkPointLocators

    :param: pathname: directory where models are
    :param: model_to_world: optional

    :return: locators
    :return: actors
    """
    models = []

    loader = VTKSurfaceModelDirectoryLoader(path_name)
    models = loader.models

    locators = []

    for model in models:
        model.set_model_transform(np2vtk(model_to_world))
        model.transform_filter.Update()
        point_locator = vtk.vtkPointLocator()
        point_locator.SetDataSet(model.source)
        locators.append(point_locator)

    return models, locators

# coding=utf-8
""" Algorithms for the surgery evaluation application """
from random import shuffle
import vtk
from numpy import inf, eye, loadtxt, float32
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


def populate_models(config):
    """
    Loads vtk models from a directory and returns
    a list of vtk actors and associated vtkPointLocators

    :param: configuration, should contain a target value
    :param: model_to_world: 4x4 matrix, of dtype float32

    :return: locators
    :return: actors

    :raises: KeyError if target not in config
    """
    models = []
    if "target" not in config:
        raise KeyError("Config must contain target key")

    path_name = config.get("target")

    loader = VTKSurfaceModelDirectoryLoader(path_name)
    models = loader.models

    locators = []

    model_to_world = _set_model_to_world(config)
    transform = vtk.vtkTransform()
    transform.SetMatrix(np2vtk(model_to_world))

    for model in models:
        print(model.source.GetCenter())
        transformer = vtk.vtkTransformPolyDataFilter()
        transformer.SetTransform(transform)
        transformer.SetInputData(model.source)
        target = vtk.vtkPolyData()
        transformer.SetOutput(target)
        transformer.Update()
        model.source = target

        transformer.SetInputConnection(model.normals.GetOutputPort())
        model.mapper = vtk.vtkPolyDataMapper()
        model.mapper.SetInputConnection(transformer.GetOutputPort())
        model.mapper.Update()
        model.actor.SetMapper(model.mapper)

        print("after trans", model.source.GetCenter())
        point_locator = vtk.vtkPointLocator()
        point_locator.SetDataSet(model.source)
        point_locator.Update()
        locators.append(point_locator)

    return models, locators

def add_map(config):
    """
    Loads vtk models from a directory and returns
    a list of vtk actors, with mesh visualisation

    :param: configuration, may contain a "map" key
    :param: model_to_world: 4x4 matrix, of dtype float32

    :return: actors, None if no "map" key
    """
    models = []
    if "map" not in config:
        return None

    path_name = config.get("map")

    loader = VTKSurfaceModelDirectoryLoader(path_name)
    models = loader.models

    model_to_world = _set_model_to_world(config)
    transform = vtk.vtkTransform()
    transform.SetMatrix(np2vtk(model_to_world))

    for model in models:
        transformer = vtk.vtkTransformPolyDataFilter()
        transformer.SetTransform(transform)
        transformer.SetInputData(model.source)
        target = vtk.vtkPolyData()
        transformer.SetOutput(target)
        transformer.Update()
        model.source = target

        transformer.SetInputConnection(model.normals.GetOutputPort())
        model.mapper = vtk.vtkPolyDataMapper()
        model.mapper.SetInputConnection(transformer.GetOutputPort())
        model.mapper.Update()
        model.actor.SetMapper(model.mapper)
        model.actor.GetProperty().SetRepresentationToWireframe()
        model.actor.GetProperty().SetColor(0.7, 0.7, 0.7)
        model.actor.GetProperty().SetOpacity(1.0)
        model.actor.GetProperty().SetBackfaceCulling(False)

    return models


def _set_model_to_world(config):
    """
    Creates a 4x4 model to world matrix
    :param: the configuration, if model to world is defined it will load, if
    not will set a identity model to world
    :return the model to world matrix

    :raises: ValueError if file does not contain a 4x4 matrix

    """
    model_to_world = eye(4, dtype=float32)

    if "model to world" in config:
        model_to_world = loadtxt(config.get("model to world"), dtype=float32)

    if (model_to_world.shape == (4, 4) and model_to_world.dtype == float32):
        return model_to_world

    raise ValueError(('model to world should be a 4x4 matrix of type float32'),
                     model_to_world.shape, model_to_world.dtype)


def random_targets(count):
    """
    Create a list of targets
    """
    list_a = []
    for i in range(count):
        list_a.append(i)

    shuffle(list_a)

    return list_a

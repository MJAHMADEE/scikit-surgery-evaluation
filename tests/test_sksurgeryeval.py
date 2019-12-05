# coding=utf-8

"""scikit-surgery-evaluation tests"""

import pytest
import vtk
import numpy
from sksurgeryvtk.models.vtk_cylinder_model import VTKCylinderModel
from sksurgeryeval.ui.sksurgeryeval_demo import run_demo
from sksurgeryeval.algorithms.algorithms import \
        point_in_locator, np2vtk, configure_tracker, populate_models
# Pytest style

def test_using_pytest_sksurgeryeval():
    """
    Test that the app runs
    """
    with pytest.raises(ValueError):
        run_demo("empty", True)


def test_populate_models():
    """
    Tests that populate models function reads data from
    a directory and returns a list of polydata and pointlocators
    """
    config = {"target" : "data/patches"}
    models, locators = populate_models(config)
    point_in, _ = point_in_locator((570.0, 270.0, -1386.0),
                                   locators, 3.0)
    assert len(models) == 3
    assert len(locators) == 3
    assert point_in == 2


def test_point_in_locator():
    """
    Tests that point locator can find the nearest point in a
    bunch of polydata.
    """
    locators = []
    for x_ord in range(-5, 6, 5):
        for y_ord in range(-5, 6, 5):
            for z_ord in range(-5, 6, 5):
                model = VTKCylinderModel(1.0, 0.5, (1.0, 1.0, 1.0), "name",
                                         0.0, (1.0, 0.0, 0.0), 88,
                                         True, 1.0)

                transform_vector = (1.0, 0.0, 0.0, float(x_ord),
                                    0.0, 1.0, 0.0, float(y_ord),
                                    0.0, 0.0, 1.0, float(z_ord),
                                    0.0, 0.0, 0.0, 1.0)
                transform = vtk.vtkTransform()
                transform.SetMatrix(transform_vector)
                transform_filter = vtk.vtkTransformPolyDataFilter()
                transform_filter.SetTransform(transform)
                source_new = vtk.vtkPolyData()
                transform_filter.SetInputData(model.source)
                transform_filter.SetOutput(source_new)
                transform_filter.Update()

                locator = vtk.vtkPointLocator()
                locator.SetDataSet(source_new)
                locator.Update()

                locators.append(locator)

    point_in, distance = point_in_locator((0.0, 0.0, 0.0), locators, 7.0)
    assert point_in == 13
    numpy.testing.assert_almost_equal(distance, 0.5, 6)


def test_np2vtk_valid():
    """
    Tests np2vtk for a valid matrix.
    """
    np_mat = numpy.eye(4, 4)
    np_mat[0, 3] = -1.7
    np_mat[3, 1] = 2.3
    vtk_mat = np2vtk(np_mat)

    for i in range(4):
        for j in range(4):
            assert (vtk_mat.GetElement(i, j) == np_mat[i, j])


def test_np2vtk_invalid():
    """
    Tests np2vtk throws value error for invalid matrix
    """
    np_mat = numpy.eye(3, 3)

    with pytest.raises(ValueError):
        _ = np2vtk(np_mat)




def test_config_tracker_invalid():
    """
    Tests that configure_tracker throws a KeyError when invalid
    """
    config = {}
    with pytest.raises(KeyError):
        configure_tracker(config)


def test_config_tracker_dummy():
    """
    Tests that configure_tracker for ndi, using dummy
    """
    config = {"tracker type" : "dummy"}
    try:
        configure_tracker(config)
    except ValueError:
        pass


def test_config_tracker_aruco():
    """
    Tests that configure_tracker for ndi, using dummy
    """
    config = {
        "tracker type" : "aruco",
        "video source" : "data/aruco_tag.avi"
        }
    configure_tracker(config)

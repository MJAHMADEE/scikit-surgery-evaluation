# coding=utf-8

"""scikit-surgery-evaluation tests"""

import pytest
import vtk
from sksurgeryeval.ui.sksurgeryeval_demo import run_demo
from sksurgeryeval.algorithms.algorithms import point_in_locator, np2vtk, configure_tracker, populate_models
from sksurgeryvtk.models.vtk_cylinder_model import VTKCylinderModel
# Pytest style

def test_using_pytest_sksurgeryeval():
    with pytest.raises(ValueError):
        run_demo("empty", True)


def test_populate_models():

    populate_models("data")


def test_point_in_locator():

    locators=[]

    for x in range (-2,2,1):
        for y in range (-2,2,1):
            for z in range (-2,2,1):
                model =  VTKCylinderModel(10, 5, (1.0, 1.0, 1.0), "name",
                                          0.0, (1.0, 0.0, 0.0 ), 88,
                                          True, 1.0)

                transform_vector = (1.0, 0.0, 0.0, float(x), 0.0, 1.0, 0.0, float(y), 0.0, 0.0, 1.0, float(z), 0.0, 0.0, 0.0, 1.0)
                transform = vtk.vtkTransform()
                transform.SetMatrix(transform_vector)
	       # print(transform)
                model.transform_filter.SetInputData(model.source)
                model.transform_filter.SetTransform(transform)
                model.mapper.Update()
                locator = vtk.vtkPointLocator()

                locator.SetDataSet(model.source)

                locators.append(locator)

    point_in, distance = point_in_locator ( (0.1,0.0,0.0), locators, 1.0 )
    print (point_in, distance)

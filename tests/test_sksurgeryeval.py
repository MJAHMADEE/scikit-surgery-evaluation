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

    for i in range (10):
        model =  VTKCylinderModel(10, 5, (1.0, 1.0, 1.0), "name",
                                              0.0, (1.0, 0.0, 0.0 ), 88,
                                              True, 1.0)
        locator = vtk.vtkPointLocator()

        locator.SetDataSet(model.source)

        locators.append(locator)

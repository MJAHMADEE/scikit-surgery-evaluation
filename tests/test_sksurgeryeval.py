# coding=utf-8

"""scikit-surgery-evaluation tests"""

import pytest
from sksurgeryeval.ui.sksurgeryeval_demo import run_demo
from sksurgeryeval.algorithms.algorithms import point_in_locator, np2vtk, configure_tracker, populate_models

# Pytest style

def test_using_pytest_sksurgeryeval():
    with pytest.raises(ValueError):
        run_demo("empty", True) 

def test_populate_models():

    populate_models("data")



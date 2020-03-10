# coding=utf-8

"""scikit-surgery-evaluation tests"""

from os import remove, path
from sksurgeryeval.logging.surgery_logger import Logger

def test_empty_config():
    """
    Test that the app runs
    """

    config = {
        "tracker type" : "aruco",
        "video source" : "data/aruco_tag.avi"
        }

    logger = Logger(config)

    logger.log(message="testing")
    logger.close()


def test_non_empty_config():
    """
    Test that the app runs
    """

    config = {
        "logger" : {}
        }

    logger = Logger(config)

    logger.log(message="testing")
    assert path.exists("sks_evaluation.log")

    logger.close()
    remove("sks_evaluation.log")


def test_overwrite():
    """
    Test that overwrite works
    """

    config = {
        "logger" : {
            "log file name" : "testing_log_file.log",
            "overwrite existing" : True
            }
        }

    logger = Logger(config)
    logger.log(message="testing")
    assert path.exists("testing_log_file.log")

    logger.close()
    remove("testing_log_file.log")

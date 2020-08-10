scikit-surgery-evaluation
===============================

.. image:: https://github.com/UCL/scikit-surgery-evaluation/raw/master/project-icon.png
   :height: 128px
   :width: 128px
   :target: https://github.com/UCL/scikit-surgery-evaluation
   :alt: Logo

.. image:: https://github.com/UCL/scikit-surgery-evaluation/workflows/.github/workflows/ci.yml/badge.svg
   :target: https://github.com/UCL/scikit-surgery-evaluation/actions
   :alt: GitHub Actions CI status

.. image:: https://coveralls.io/repos/github/UCL/scikit-surgery-evaluation/badge.svg?branch=master&service=github
    :target: https://coveralls.io/github/UCL/scikit-surgery-evaluation?branch=master 
    :alt: Test coverage

.. image:: https://readthedocs.org/projects/scikit-surgery-evaluation/badge/?version=latest
    :target: http://scikit-surgery-evaluation.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status

.. image:: https://img.shields.io/badge/Cite-SciKit--Surgery-informational
   :target: https://doi.org/10.1007/s11548-020-02180-5
   :alt: The SciKit-Surgery paper


Author: Stephen Thompson

scikit-surgery-evaluation provides an application to evaluate surgical skills. You can provide a set of unstructured grids representing a set of locations that the user is then expected to target using a tracked pointer, utilising a SciKit-Surgery tracking library (scikit-surgeryarucotracker, or scikit-surgerynditracker). You can specify paths for the user to follow, or let the system select target meshes automatically.

scikit-surgery-evaluation is part of the `SciKit-Surgery`_ software project, developed at the `Wellcome EPSRC Centre for Interventional and Surgical Sciences`_, part of `University College London (UCL)`_.

scikit-surgery-evaluation supports Python 3.6.


::

    python sksurgeryeval.py -c configuration.json


Developing
----------

Cloning
^^^^^^^

You can clone the repository using the following command:

::

    git clone https://github.com/UCL/scikit-surgery-evaluation


Running tests
^^^^^^^^^^^^^
Pytest is used for running unit tests:
::

    pip install pytest
    python -m pytest


Linting
^^^^^^^

This code conforms to the PEP8 standard. Pylint can be used to analyse the code:

::

    pip install pylint
    pylint --rcfile=tests/pylintrc sksurgeryeval


Installing
----------

You can pip install directly from the repository as follows:

::

    pip install git+https://github.com/UCL/scikit-surgery-evaluation



Contributing
^^^^^^^^^^^^

Please see the `contributing guidelines`_.


Useful links
^^^^^^^^^^^^

* `Source code repository`_
* `Documentation`_


Licensing and copyright
-----------------------

Copyright 2019 University College London.
scikit-surgery-evaluation is released under the BSD-3 license. Please see the `license file`_ for details.


Acknowledgements
----------------

Supported by `Wellcome`_ and `EPSRC`_.


.. _`Wellcome EPSRC Centre for Interventional and Surgical Sciences`: http://www.ucl.ac.uk/weiss
.. _`source code repository`: https://github.com/UCL/scikit-surgery-evaluation
.. _`Documentation`: https://scikit-surgery-evaluation.readthedocs.io
.. _`SciKit-Surgery`: https://github.com/UCL/scikit-surgery/wiki
.. _`University College London (UCL)`: http://www.ucl.ac.uk/
.. _`Wellcome`: https://wellcome.ac.uk/
.. _`EPSRC`: https://www.epsrc.ac.uk/
.. _`contributing guidelines`: https://github.com/UCL/scikit-surgery-evaluation/blob/master/CONTRIBUTING.rst
.. _`license file`: https://github.com/UCL/scikit-surgery-evaluation/blob/master/LICENSE


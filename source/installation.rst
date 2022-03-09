.. _installation:

Requirements
============
To install memewizard, you need the following:
 * A Chromium-based web browser (e.g: Microsoft Edge or Google Chrome)
 * `Python 3.9 <https://www.python.org/downloads/release/python-390/>`_

(On Linux, X Window System is needed.)

Installation
============

.. code-block:: bash

  pip install memewizard

If you want bleeding edge features, install from the Git repository (assuming you have Git installed)

.. code-block:: bash

  pip install git+https://github.com/themysticsavages/memewizard

After installing, run ``python -m memewizard.cli`` or ``python3 -m memewizard.cli`` on Linux.

Uninstallation
--------------

.. code-block:: bash

  pip uninstall memewizard

(This also applies to the Git version)

**NOTE: Command Prompt and Powershell do not handle ANSI colors correctly, so you will see visual bugs. You can use something like** `Windows Terminal <https://www.microsoft.com/en-us/p/windows-terminal/9n0dx20hk701>`_ **to fix ANSI codes.**
Installation & Contributing
===========================

Installation
~~~~~~~~~~~~


Installation is as simple as you'd expect. With pipenv:

.. code-block:: bash

  $ pipenv install pyaltium

Or with poetry:

.. code-block:: bash

  $ poetry add pyaltium

Or for standard pip:

.. code-block:: bash

  $ pip install pyaltium


Contributing
~~~~~~~~~~~~

Just start with the following:

.. code-block:: bash

  $ pipenv install --dev


If you run into dependency issues:

.. code-block:: bash

  $ pipenv install --dev --skip-lock


Write tests and make them pass, and add documentation for any
externally-visible changes. I'm still getting tox running as of the
time of writing but once it's working, just run ``tox`` to verify it
all. There is also a pre commit hook that can be added with:

.. code-block:: bash

  $ pre-commit install

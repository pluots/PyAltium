Installation & Contributing
===========================

Installation
~~~~~~~~~~~~


Installation is as simple as you'd expect. Everyone should be
using pipenv or poetry (that statement is somewhere between opinion and fact)
so we recommend it for all your packages, though it makes no
difference:

.. code-block:: bash

  $ pipenv install pyaltium

.. code-block:: bash

  $ poetry add pyaltium

Or for pip:

.. code-block:: bash

  $ pip install pyaltium


Contributing
~~~~~~~~~~~~

Here I will force you

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

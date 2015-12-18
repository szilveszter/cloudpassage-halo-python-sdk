Testing
=======

.. toctree::

File locations
--------------
Important locations for testing:

  tests/configs: You'll find a file here called portal.yaml.  Copy it to
  portal.yaml.local and complete the information inside with your API key and
  secret.  the .gitignore settings will keep you from checking in your creds
  if you put them in the .local file.  This file (portal.yaml.local) is
  referenced directly by all tests requiring interaction with the API.

  tests/policies: These are Halo policies, used primarily for integration
  tests.

  tests/tests: This is where you'll find the actual tests.


Running tests
-------------

  Navigate to tests/ and run ``py.test ./tests/`` to run the test suite.

  If you've got the coverage module installed,
  ``py.test --cov=cloudpassage ./tests/`` will show statement test coverage.

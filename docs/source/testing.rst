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

  tests/integration: This is where you'll find the integration tests, which
  require valid API credentials be placed in the
  tests/configs/portal.yaml.local file.

  tests/unit: You'll find the unit tests here, which do not require API
  credentials.

  tests/style: We put style checking tests here.  For now, just pep8-related.


Environmental Requirements
--------------------------

You'll need to have a CloudPassage Halo account available for running the
tests, as many are integration-focused.  These are the things you need to have
(at the very least) to get a clean testing run:

* Servers:
    * Have at least one active Linux and active Windows server.
    * One deactivated server of any type.
* Policies:
    * One firewall policy
    * One alert profile
    * One Linux CSM policy
    * One Linux FIM policy
    * One Windows FIM policy
    * One LIDS policy
* Scans:
    * CSM (Failed scan)
    * FIM (active baseline and successful scan)
    * One CVE exception
* Events:
    * One event produced by a Windows server.
* Server Group:
    * Using the default group is fine.
    * Assign the policies mentioned above to the group.
    * Run FIM baselines against the Linux and Windows servers.
    * Kick off a CSM scan if it doesn't happen automatically


Running tests
-------------

  Navigate to tests/ and run ``py.test ./integration ./unit ./style``
  to run the entire test suite.  You can remove any of these if you
  want to focus on a particular section.  For instance, to run only
  the unit and style tests, you would use ``py.test ./unit ./style``.

  If you've got the coverage module installed,
  ``py.test --cov=cloudpassage ./integration ./unit ./style``
  will show statement test coverage.

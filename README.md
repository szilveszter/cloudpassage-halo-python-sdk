# cloudpassage-halo-python-sdk

## Python SDK for CloudPassage Halo API

### Installation

Requirements:

* requests
* pyaml


Install from pip with ```pip install cloudpassage```.  If you want to make
modifications to the SDK you can install it in editable mode by downloading
the source from this github repo, navigating to the top directory within the
archive and running ```pip install -e .``` (note the . at the end).

### Quick Start

Here's the premise: you store your session configuration information (API
credentials, proxy settings, etc) in the cloudpassage.HaloSession object.
This object gets passed into the various class methods which allow you
to interact with the CloudPassage Halo API.

Practical example:
We'll print a list of all servers in our account:

```python
import cloudpassage

api_key = MY_HALO_API_KEY
api_secret = MY_API_SECRET
session = cloudpassage.HaloSession(api_key, api_secret)
server = cloudpassage.Server(session)

list_of_servers = server.list_all()
for s in list_of_servers:
    print "ID: %s   Name: %s" % (s["id"], s["hostname"])

```

### Testing

Important locations for testing:

  tests/configs: You'll find a file here called portal.yaml.  Copy it to
  portal.yaml.local and complete the information inside with your API key and
  secret.  the .gitignore settings will keep you from checking in your creds
  if you put them in the .local file.  This file (portal.yaml.local) is
  referenced directly by all tests requiring interaction with the API.

  tests/policies: These are Halo policies, used primarily for integration
  tests.

  tests/tests: This is where you'll find the actual tests.


Running tests:

  Navigate to tests/ and run ```py.test ./tests/``` to run the test suite.

  If you've got the coverage module
  installed, ```py.test --cov=cloudpassage ./tests/``` will show
  statement test coverage.

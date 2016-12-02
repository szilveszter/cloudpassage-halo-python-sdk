Contributing
============

.. toctree::

We appreciate pull requests, and will do our best to answer each quickly.
Please issue pull requests against the develop branch, and make sure that
your commit messages follow this format:


::

  ACTION: [AUDIENCE:] COMMIT_MSG [!TAG ...]

  ACTION can be chg, fix, or new
  AUDIENCE can be dev, usr, pkg, test, or doc
  TAG can be refactor, minor, cosmetic, or wip.

  Here's an example:

  chg: usr: Changes a thing that is relevant to users !minor

  AUDIENCE and TAG are optional.  This format is required for our changelog
  generator.  Details can be found in the comments at the beginning of the
  .gitchangelog.rc file, in the root of this repository.

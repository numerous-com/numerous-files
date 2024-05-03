Contribution guidelines
=======================

This document describes guidelines for how work is done on the numerous repository.

Commit messages
---------------

Commit messages should always be formatted as
[conventional commits](https://www.conventionalcommits.org/en/v1.0.0/). This means that
the they follow the following format:

    <type>[optional scope]: <description>

    [optional body]

    [optional footer(s)]


### Types

Often `<type>` will be `fix` for minor changes and bug fixes, or `feat` for new
functionality.

Other valid `<type>`s are `build`, `chore`, `ci`, `docs`, `style`, `refactor`,
`perf`, and `test`.


### Scopes

We use scopes to denote the subprojects the changes are related to, these correspond to
top-level folders in the project, e.g. `api`, `cli`, `client`, `docs`, `domain-config`,
`infrastructure`, `proxy`, `python-sdk`, `shared` and `www`.

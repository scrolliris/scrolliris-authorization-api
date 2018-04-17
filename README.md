# Bern

[![pipeline status][pipeline]][master] [![coverage report][coverage]][master]

[pipeline]: https://gitlab.com/scrolliris/bern/badges/master/pipeline.svg
[coverage]: https://gitlab.com/scrolliris/bern/badges/master/coverage.svg
[master]: https://gitlab.com/scrolliris/bern/commits/master


```txt
 , __
/|/  \
 | __/ _   ,_    _  _
 |   \|/  /  |  / |/ |
 |(__/|__/   |_/  |  |_/

Bern:
```


## Repository

https://gitlab.com/scrolliris/bern



## Requirements

* Python `3.5.5`
* Redis


## Setup

```zsh
: setup python environment (e.g. virtualenv)
% python3.5 -m venv venv
% source venv/bin/activate
(venv) % pip install --upgrade pip setuptools
```

### Development

Use `waitress` as wsgi server.  
Check `Makefile`.

```zsh
% cd /path/to/bern
% source venv/bin/activate

: set env
(venv) % cp .env.sample .env

: install packages
(venv) % ENV=development make setup
```

### Server

```
: run server (waitress)
(venv) % make serve
```

```zsh
: run server (cherrypy)
(venv) % make start
```

### Vet

* flake8
* flake8-docstrings (pep257)
* pylint


```zsh
: add hook
(venv) % flake8 --install-hook git

(venv) % make check
(venv) % make lint

: run both
(venv) % make vet
```

### Test

```zsh
(venv) % make test
```


## CI

You can check it by yourself using `gitlab-ci-multi-runner` on locale machine.
It requires `docker`.

```zsh
% ./tool/setup-gitlab-ci-multi-runner

: use script
% ./tool/ci-runner test
```


## License

```txt
Bern
Copyright (c) 2018 Lupine Software LLC
```

`AGPL-3.0`

The project is distributed as GNU Affero General Public License. (version 3.0)

```txt
This is free software: You can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
```

See [LICENSE](LICENSE).

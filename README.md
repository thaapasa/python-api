# python-api

Trying out a server with an API

## Setup

Install [poetry](https://python-poetry.org/docs/#installation):

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

This can fail if you do not have SSL certificates for Python installed.
The Python distribution should have an `Install Certificates` program
included that you can run to install the certs.

For me, I had to run
`/Applications/Python 3.12/Install Certificates.command`
on a MacBook Pro.

Enter poetry shell:

```bash
poetry shell
```

Then, install dependencies

```bash
poetry install
# or
make install
```

Then, create local copies of config templates:

```bash
cp alembic.ini.tmpl alembic.ini
cp config.py.tmpl config.py
```

Adjust settings (such as database URL) as needed.

You can create the database with:

```bash
make db
```

## Add new DB migration

```bash
poetry rub alembic revision -m "Revision information"
```

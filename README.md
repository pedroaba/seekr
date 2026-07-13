# Seekr

Seekr is a command-line tool for indexing personal files and finding them quickly with fuzzy search.

It is designed to help you search across common local folders, such as Downloads, Documents, Pictures, Videos, Music, and Desktop, from a simple terminal workflow.

## Status

Seekr is in early development.

## Usage

Show the available commands:

```bash
python main.py --help
```

### Scan default folders

Scan Downloads, Documents, Desktop, Pictures, Videos, and Music:

```bash
python main.py init
```

Display the paths found during the scan:

```bash
python main.py init --show
```

### Initialize configuration

Create the local configuration when it does not exist. Existing values are
preserved when `--reset` is omitted:

```bash
python main.py config init
```

Replace the existing configuration with Seekr's defaults:

```bash
python main.py config init --reset
```

### Read configuration

Show the complete configuration as formatted JSON:

```bash
python main.py config show
```

Read one or more specific values:

```bash
python main.py config get ignores
python main.py config get ignores --format
```

Absolute paths in configuration output are redacted to avoid exposing personal
directory names.

### Configure ignored paths

Append existing files or folders to the ignore list:

```bash
python main.py config set ignores --path .venv build
```

Ignore folders by exact nickname:

```bash
python main.py config set ignores --path-nickname __pycache__ .pytest_cache
```

Replace the current ignore list instead of appending:

```bash
python main.py config set ignores --override --path dist
```

Nickname validation rejects empty values, path traversal tokens, path
separators, and glob patterns.

## Development checks

Run the test suite and static checks:

```bash
task test
task lint
task security
task audit
```

## Database migrations

Seekr uses SQLAlchemy models from `seekr/database/models/` and stores Alembic
migrations in `seekr/database/migrations/`.

Create a migration after changing a model:

```bash
task db-generate -m "describe the change"
```

`db-generate` creates a migration file by comparing the SQLAlchemy models with
the current database schema. `db-upgrade` only applies migration files that
already exist.

Apply or revert migrations:

```bash
task db-upgrade
task db-downgrade
task db-history
```

By default, the database is stored in Seekr's user data directory. Override it
with a SQLAlchemy URL when needed:

```bash
SEEKR_DATABASE_URL=sqlite:////absolute/path/seekr.db alembic upgrade head
```

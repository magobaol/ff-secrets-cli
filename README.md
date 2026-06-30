# ff-secrets-cli
The command-line client of **ff-secrets** — it provides the `ff-secrets` command. It gives unified, vendor-agnostic access to secrets by resolving an alias to its value through [`ff-secrets-server`](https://github.com/magobaol/ff-secrets-server) over HTTP. Pure Python standard library, zero dependencies.

## What it is
ff-secrets is one system with several surfaces: a server and the clients that talk to it (this CLI, plus Keyboard Maestro, Drafts and Shortcuts). This repo is the shell-facing one. A consumer asks for a secret by a stable alias (e.g. `acme.api.credential`) and never sees where it comes from. The client holds only the server endpoint: no registry, no backend credential, no vendor SDK. The registry, the backend driver and the bearer all live in ff-secrets-server, so the client cannot reach the backend directly, by design.

## Commands
### read
Print the value of an alias.
```
ff-secrets read acme.api.credential
```
### list
List available aliases, optionally by prefix.
```
ff-secrets list
ff-secrets list acme.
```
### run
Run a command with secrets injected as environment variables, never touching disk.
```
ff-secrets run --env API_TOKEN=acme.api.credential -- ./deploy.sh
ff-secrets run --env-file vars.env -- make release
```
`--env-file` reads `VAR=alias` lines; the child process gets only the requested secrets.
### inject
Resolve `ffsec:<alias>` markers in a template, from stdin or a file.
```
echo 'token = ffsec:acme.api.credential' | ff-secrets inject
ff-secrets inject -i config.tmpl -o config.out
```

## The `ffsec:` marker
To reference a secret from a config or `.env`, put the marker `ffsec:<alias>` as the **value** of an ordinary field and resolve it with `inject`. The field keeps its own semantic name; the value is an opaque pointer.
```
api-token: ffsec:acme.api.credential
```
This keeps the consumer decoupled from the alias naming and from the backend.

## Configuration
One setting in `~/.config/ff-secrets/config.yaml`:
```
server-endpoint: http://SERVER_HOST:8666
```
See `config.example.yaml`. Override the path with `FF_SECRETS_CONFIG`.

## Install
From the source directory:
```
make install
```
This builds a single-file executable with `zipapp` and places it on your `PATH` as `~/.local/bin/ff-secrets`. Being pure standard library, the whole package collapses into one self-contained `.pyz` with a `python3` shebang — no build toolchain and no virtualenv. Override the install prefix with `PREFIX` (default `~/.local`).

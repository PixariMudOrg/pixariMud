# PixariMUD

[![Lint](https://github.com/PixariMudOrg/pixariMud/actions/workflows/lint.yml/badge.svg)](https://github.com/PixariMudOrg/pixariMud/actions/workflows/lint.yml)

## Hi there 👋

# Setup a Development Server

## Set up a virtual environment

After cloning, make your choice of virtual environment manager, such as `uv`, `poetry`, or `conda`; Here's a basic usage of `venv`:

```
python3 -m venv venv

# linux/*nix
source venv/bin/activate

# windows(?)
venv\bin\activate.bat
```

Install libraries.

```
pip install -r requirements.txt
```

Create your local db.

```
cd pixarimud
evennia migrate
```

## Start Evennia

If you used a package manager, you need to activate your virtual environment each time you return to the directory before using Evennia commands. (`source venv/bin/activate`)


Start the server.

```
evennia start -l
```

You'll need to configure a superuser account for your local instance.

## Stop Evennia

Evennia will run in the background. You need to stop the server, or it will keep listening for ports.

```
evennia stop
```

## Connect

Evennia listens on port 4000 for telnet connections, and 4005 for HTTP connections.

```
telnet localhost 4000
```

or browse to [http://localhost:4005](http://localhost:4005)

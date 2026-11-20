# Daymark

Daymark is a polished, dark-themed personal task manager built with Flask, SQLite, HTML, CSS, and vanilla JavaScript. Organize everyday work, track due dates, and keep an eye on what you have completed.

## Features

- Add, edit, complete, reopen, and remove tasks.
- Organize tasks into Work, Personal, Health, and Learning categories.
- Set a priority and optional due date; overdue tasks are highlighted.
- Search tasks and filter by completion status or category.
- See a dashboard summary of open, completed, overdue, and total tasks.
- Responsive interface with a mobile navigation drawer and task editor.
- SQLite persistence with no separate database service required.

## Screenshots

### Dashboard

![Daymark dark dashboard](./app%20screenshots/Screenshot%202026-11-20%20213926.png)

### Task list

![Daymark task list](./app%20screenshots/Screenshot%202026-11-20%20214006.png)

### Completed tasks

![Daymark completed tasks](./app%20screenshots/Screenshot%202026-11-20%20214036.png)

### Category filter

![Daymark category filter](./app%20screenshots/Screenshot%202026-11-20%20214119.png)

## Run locally

### Prerequisites

- Python 3.10 or later
- `pip`

### macOS / Linux

From the project directory:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

### Windows PowerShell

From the project directory:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

If PowerShell blocks activation, allow it for the current terminal session and activate again:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Open [http://localhost:5000](http://localhost:5000). Flask creates the SQLite database automatically at `instance/daymark.sqlite` on first run. Stop the development server with `Ctrl+C`; leave the virtual environment with `deactivate`.

## Run in WSL

Install Python and virtual-environment support in your WSL distribution:

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip
```

Change to the project directory. For a repository stored on the Windows `C:` drive, for example:

```bash
cd /mnt/c/Users/Dell/downloads/flaskapp
```

Then create the environment and start Daymark:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Open [http://localhost:5000](http://localhost:5000) in your Windows browser. WSL forwards the local port automatically. When finished, press `Ctrl+C` in the WSL terminal.

> Tip: for better file-system performance, keep the project inside the WSL Linux filesystem (for example, `~/projects/flaskapp`) instead of `/mnt/c`.

## Run with Docker

Install and start Docker Desktop (with WSL integration enabled when using Docker from WSL), or install Docker Engine in Linux. Run these commands from the directory containing the `Dockerfile`.

The multi-line Docker commands below use Bash syntax (Linux, macOS, or WSL). In Windows PowerShell, run the `docker run` command on one line:

```powershell
docker run -d --name daymark-app --publish 5000:5000 --volume daymark-data:/app/instance daymark:latest
```

Build the image:

```bash
docker build -t daymark:latest .
```

Start a container and keep its SQLite data in a named Docker volume:

```bash
docker run -d \
  --name daymark-app \
  --publish 5000:5000 \
  --volume daymark-data:/app/instance \
  daymark:latest
```

Open [http://localhost:5000](http://localhost:5000).

### List and manage Docker images and containers

```bash
# List locally available images
docker image ls

# List running containers
docker container ls

# List all containers, including stopped containers
docker container ls --all

# Follow the app's logs
docker container logs --follow daymark-app

# Stop or start the container
docker container stop daymark-app
docker container start daymark-app
```

To remove the container, stop it first if it is running:

```bash
docker container stop daymark-app
docker container rm daymark-app
```

The `daymark-data` volume is separate from the container, so removing the container does not delete your database. To remove the database too, explicitly remove the volume:

```bash
docker volume rm daymark-data
```

If port `5000` is already in use, publish another host port, such as `5001`:

```bash
docker run -d \
  --name daymark-app \
  --publish 5001:5000 \
  --volume daymark-data:/app/instance \
  daymark:latest
```

Then visit [http://localhost:5001](http://localhost:5001). If a container named `daymark-app` already exists, remove it before running another container with that name.

## Configuration

- `PORT`: listening port (defaults to `5000`).
- `DATABASE`: SQLite database path (defaults to `instance/daymark.sqlite`).
- `SECRET_KEY`: Flask secret key. Set a unique, private value when deploying beyond local development.

## Run tests

With the project's virtual environment activated:

```bash
python -m unittest discover -s tests -v
```

## Project structure

```text
.
├── app.py
├── Dockerfile
├── requirements.txt
├── taskflow/
│   ├── __init__.py
│   ├── db.py
│   ├── routes.py
│   ├── static/
│   │   ├── css/style.css
│   │   └── js/app.js
│   └── templates/
│       ├── base.html
│       └── dashboard.html
├── tests/
│   └── test_app.py
└── app screenshots/
    └── (application screenshots)
```

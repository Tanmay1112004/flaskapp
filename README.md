# Daymark

A calm, responsive personal task manager built with Flask, SQLite, HTML, CSS, and vanilla JavaScript.

## Features

- Add, edit, complete, reopen, and remove tasks.
- Organize tasks into Work, Personal, Health, and Learning spaces.
- Set a priority and optional due date; overdue tasks are highlighted.
- Search tasks and filter by completion status or category.
- See a live overview of open, completed, overdue, and total tasks.
- Responsive layout with a mobile navigation drawer and task editor.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python app.py
```

Open [http://localhost:5000](http://localhost:5000). The SQLite database is created automatically at `instance/daymark.sqlite`.

Set `DATABASE` to use a different SQLite file. Set `PORT` to change the listening port. For deployment, provide a unique `SECRET_KEY` environment variable.

## Run tests

```bash
python -m unittest discover -s tests
```

## Project layout

```text
.
├── app.py
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
├── requirements.txt
└── Dockerfile
```

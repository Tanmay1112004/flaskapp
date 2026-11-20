from datetime import date

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from .db import get_db

bp = Blueprint("main", __name__)
CATEGORIES = ("Work", "Personal", "Health", "Learning")
PRIORITIES = ("Low", "Medium", "High")


def _task_or_404(task_id):
    task = get_db().execute(
        "SELECT * FROM tasks WHERE id = ?", (task_id,)
    ).fetchone()
    if task is None:
        abort(404)
    return task


def _validated_form():
    title = request.form.get("title", "").strip()
    notes = request.form.get("notes", "").strip()
    category = request.form.get("category", "Personal")
    priority = request.form.get("priority", "Medium")
    due_date = request.form.get("due_date", "").strip() or None

    errors = []
    if not title:
        errors.append("Add a task name before saving.")
    elif len(title) > 120:
        errors.append("Task names must be 120 characters or fewer.")
    if len(notes) > 500:
        errors.append("Notes must be 500 characters or fewer.")
    if category not in CATEGORIES:
        errors.append("Choose a valid category.")
    if priority not in PRIORITIES:
        errors.append("Choose a valid priority.")
    if due_date:
        try:
            date.fromisoformat(due_date)
        except ValueError:
            errors.append("Choose a valid due date.")

    return {
        "title": title,
        "notes": notes,
        "category": category,
        "priority": priority,
        "due_date": due_date,
    }, errors


@bp.get("/")
def dashboard():
    db = get_db()
    tasks = db.execute(
        """
        SELECT * FROM tasks
        ORDER BY completed ASC,
            CASE priority WHEN 'High' THEN 0 WHEN 'Medium' THEN 1 ELSE 2 END,
            CASE WHEN due_date IS NULL THEN 1 ELSE 0 END,
            due_date ASC,
            id DESC
        """
    ).fetchall()
    stats = db.execute(
        """
        SELECT
            COUNT(*) AS total,
            COALESCE(SUM(completed = 0), 0) AS open,
            COALESCE(SUM(completed = 1), 0) AS completed,
            COALESCE(SUM(completed = 0 AND due_date < date('now')), 0) AS overdue
        FROM tasks
        """
    ).fetchone()
    return render_template(
        "dashboard.html",
        tasks=tasks,
        stats=stats,
        today=date.today(),
        categories=CATEGORIES,
        priorities=PRIORITIES,
    )


@bp.post("/tasks")
def create_task():
    task, errors = _validated_form()
    if errors:
        for error in errors:
            flash(error, "error")
        return redirect(url_for("main.dashboard"))

    db = get_db()
    db.execute(
        """
        INSERT INTO tasks (title, notes, category, due_date, priority)
        VALUES (:title, :notes, :category, :due_date, :priority)
        """,
        task,
    )
    db.commit()
    flash("Your task is on the list.", "success")
    return redirect(url_for("main.dashboard"))


@bp.post("/tasks/<int:task_id>/edit")
def edit_task(task_id):
    _task_or_404(task_id)
    task, errors = _validated_form()
    if errors:
        for error in errors:
            flash(error, "error")
        return redirect(url_for("main.dashboard"))

    db = get_db()
    db.execute(
        """
        UPDATE tasks
        SET title = :title, notes = :notes, category = :category,
            due_date = :due_date, priority = :priority
        WHERE id = :id
        """,
        {**task, "id": task_id},
    )
    db.commit()
    flash("Task details updated.", "success")
    return redirect(url_for("main.dashboard"))


@bp.post("/tasks/<int:task_id>/toggle")
def toggle_task(task_id):
    task = _task_or_404(task_id)
    db = get_db()
    db.execute(
        "UPDATE tasks SET completed = ? WHERE id = ?",
        (0 if task["completed"] else 1, task_id),
    )
    db.commit()
    flash("Task completed." if not task["completed"] else "Task reopened.", "success")
    return redirect(url_for("main.dashboard"))


@bp.post("/tasks/<int:task_id>/delete")
def delete_task(task_id):
    _task_or_404(task_id)
    db = get_db()
    db.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    db.commit()
    flash("Task removed.", "success")
    return redirect(url_for("main.dashboard"))

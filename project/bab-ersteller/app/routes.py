from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from app.models import Plane, Report, Task
from app.forms import PlaneForm, ReportForm, TaskForm
from app import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    planes = Plane.query.all()
    return render_template('index.html', planes=planes)

@bp.route('/report/edit/<int:report_id>', methods=['GET', 'POST'])
def edit_report(report_id):
    report = Report.query.get_or_404(report_id)
    form = ReportForm(obj=report)

    # Log the initial state of the report and form
    current_app.logger.info(f"Editing report: {report}")
    current_app.logger.info(f"Initial form tasks data: {form.tasks.data}")

    if form.validate_on_submit():
        # Log that form validation succeeded
        current_app.logger.info("Form validated successfully.")
        current_app.logger.info(f"Submitted form data: {form.data}")

        # Update report details
        report.plane_id = form.plane.data
        report.date = form.date.data
        db.session.commit()

        # Log report update
        current_app.logger.info(f"Updated report: {report}")

        # Clear existing tasks for this report
        Task.query.filter_by(report_id=report.id).delete()
        current_app.logger.info("Existing tasks deleted.")

        # Add new tasks
        for index, task_form in enumerate(form.tasks.data):
            current_app.logger.info(f"Processing task {index + 1}: {task_form}")
            task = Task(
                lfd_nr=index + 1,
                task_description=task_form['task_description'],
                fix_description=task_form['fix_description'],
                reference=task_form['reference'],
                date=form.date.data,  # Use the report's date
                executor=task_form['executor'],
                report_id=report.id
            )
            db.session.add(task)
            current_app.logger.info(f"Task {index + 1} added: {task}")

        db.session.commit()  # Save all tasks
        current_app.logger.info("All tasks saved successfully.")

        flash('Report and tasks updated successfully!')
        return redirect(url_for('main.reports'))

    # Log form validation errors
    if form.errors:
        current_app.logger.warning(f"Form validation errors: {form.errors}")

    return render_template('report_form.html', form=form, report=report)


@bp.route('/planes')
def planes():
    planes = Plane.query.all()
    return render_template('planes.html', planes=planes)


@bp.route('/plane/new', methods=['GET', 'POST'])
def new_plane():
    form = PlaneForm()
    if form.validate_on_submit():
        plane = Plane(name=form.name.data, model=form.model.data, manufacturer=form.manufacturer.data)
        db.session.add(plane)
        db.session.commit()
        flash('Plane added successfully!')
        return redirect(url_for('main.planes'))
    return render_template('plane.html', form=form, plane=None)


@bp.route('/plane/edit/<int:plane_id>', methods=['GET', 'POST'])
def edit_plane(plane_id):
    plane = Plane.query.get_or_404(plane_id)
    form = PlaneForm(obj=plane)
    if form.validate_on_submit():
        plane.name = form.name.data
        plane.model = form.model.data
        plane.manufacturer = form.manufacturer.data
        db.session.commit()
        flash('Plane updated successfully!')
        return redirect(url_for('main.planes'))
    return render_template('plane.html', form=form, plane=plane)

@bp.route('/plane/delete/<int:plane_id>', methods=['POST'])
def delete_plane(plane_id):
    plane = Plane.query.get_or_404(plane_id)
    db.session.delete(plane)
    db.session.commit()
    flash('Plane deleted successfully!')
    return redirect(url_for('main.planes'))

@bp.route('/reports')
def reports():
    reports = Report.query.all()
    return render_template('reports.html', reports=reports)

@bp.route('/report/new', methods=['GET', 'POST'])
def new_report():
    form = ReportForm()

    # Log initial form state
    current_app.logger.info(f"Creating a new report. Initial form tasks data: {form.tasks.data}")

    if form.validate_on_submit():
        # Log validated form data
        current_app.logger.info("Form validated successfully.")
        current_app.logger.info(f"Submitted form data: {form.data}")

        # Create and save the new report
        report = Report(
            plane_id=form.plane.data,
            date=form.date.data
        )
        db.session.add(report)
        db.session.commit()  # Commit to generate the report ID
        current_app.logger.info(f"New report created: {report}")

        # Add tasks to the report
        for index, task_form in enumerate(form.tasks.data):
            current_app.logger.info(f"Processing task {index + 1}: {task_form}")
            task = Task(
                lfd_nr=index + 1,
                task_description=task_form['task_description'],
                fix_description=task_form['fix_description'],
                reference=task_form['reference'],
                date=form.date.data,  # Use the report's date
                executor=task_form['executor'],
                report_id=report.id
            )
            db.session.add(task)
            current_app.logger.info(f"Task {index + 1} added: {task}")

        db.session.commit()  # Save all tasks
        current_app.logger.info("All tasks saved successfully.")

        flash('Report and tasks created successfully!')
        return redirect(url_for('main.reports'))

    # Log form validation errors
    if form.errors:
        current_app.logger.warning(f"Form validation errors: {form.errors}")

    return render_template('report_form.html', form=form, report=None)


@bp.route('/report/delete/<int:report_id>', methods=['POST'])
def delete_report(report_id):
    report = Report.query.get_or_404(report_id)
    db.session.delete(report)
    db.session.commit()
    flash('Report deleted successfully!')
    return redirect(url_for('main.reports'))

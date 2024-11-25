from flask import Blueprint, render_template, redirect, url_for, flash, current_app
from app.models import Plane, Report, Task
from app.forms import ReportForm
from app import db

bp = Blueprint('main', __name__)

@bp.route('/report/edit/<int:report_id>', methods=['GET', 'POST'])
def edit_report(report_id):
    report = Report.query.get_or_404(report_id)
    form = ReportForm(obj=report)

    if form.validate_on_submit():
        report.plane_id = form.plane.data
        report.date = form.date.data
        db.session.commit()

        Task.query.filter_by(report_id=report.id).delete()

        for index, task_form in enumerate(form.tasks.data):
            task = Task(
                lfd_nr=index + 1,
                description=task_form['description'],
                fix_description=task_form['fix_description'],
                reference=task_form['reference'],
                date=form.date.data,
                executor=task_form['executor'],
                report_id=report.id
            )
            db.session.add(task)

        db.session.commit()
        flash('Report and tasks updated successfully!')
        return redirect(url_for('main.reports'))

    return render_template('report_form.html', form=form, report=report)

@bp.route('/plane/new', methods=['GET', 'POST'])
def new_plane():
    form = PlaneForm()
    if form.validate_on_submit():
        plane = Plane(name=form.name.data, model=form.model.data, manufacturer=form.manufacturer.data)
        db.session.add(plane)
        db.session.commit()
        flash('Plane added successfully!')
        return redirect(url_for('main.planes'))
    return render_template('plane_form.html', form=form)


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
    return render_template('plane_form.html', form=form, plane=plane)

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
    if form.validate_on_submit():
        report = Report(plane_id=form.plane.data, date=form.date.data)
        db.session.add(report)
        db.session.commit()
        flash('Report created successfully!')
        return redirect(url_for('main.reports'))
    return render_template('report_form.html', form=form)


@bp.route('/report/delete/<int:report_id>', methods=['POST'])
def delete_report(report_id):
    report = Report.query.get_or_404(report_id)
    db.session.delete(report)
    db.session.commit()
    flash('Report deleted successfully!')
    return redirect(url_for('main.reports'))

from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, DateField, TextAreaField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    task_description = TextAreaField('Art der Beanstandung / Durchzuführende Arbeiten', validators=[DataRequired()])
    fix_description = TextAreaField('Art der Behebung / Durchgeführte Arbeiten', validators=[DataRequired()])
    reference = StringField('Bezug / Seriennummer')
    executor = StringField('Ausführender', validators=[DataRequired()])

    class Meta:
        csrf = False  # Disable CSRF for this form

class ReportForm(FlaskForm):
    plane = SelectField('Plane', coerce=int, validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    tasks = FieldList(FormField(TaskForm), min_entries=1)
    submit = SubmitField('Save')

    def __init__(self, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        # Populate the SelectField with planes from the database
        from app.models import Plane  # Import here to avoid circular imports
        self.plane.choices = [(plane.id, f"{plane.name} ({plane.model})") for plane in Plane.query.all()]


class PlaneForm(FlaskForm):
    name = StringField('Plane Name', validators=[DataRequired()])
    model = StringField('Model', validators=[DataRequired()])
    manufacturer = StringField('Manufacturer', validators=[DataRequired()])
    submit = SubmitField('Save')
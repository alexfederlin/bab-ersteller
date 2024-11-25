from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, DateField, FieldList, FormField, SubmitField
from wtforms.validators import DataRequired

class TaskForm(FlaskForm):
    description = TextAreaField('Art der Beanstandung / Durchzuführende Arbeiten', validators=[DataRequired()])
    fix_description = TextAreaField('Art der Behebung / Durchgeführte Arbeiten', validators=[DataRequired()])
    reference = StringField('Bezug / Seriennummer')
    executor = StringField('Ausführender', validators=[DataRequired()])

class ReportForm(FlaskForm):
    plane = SelectField('Plane', coerce=int, validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    tasks = FieldList(FormField(TaskForm), min_entries=1)
    submit = SubmitField('Save')

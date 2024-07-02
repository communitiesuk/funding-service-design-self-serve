from flask_wtf import FlaskForm
from wtforms import StringField, URLField, DateTimeField, HiddenField
from wtforms.validators import DataRequired, Length

class RoundForm(FlaskForm):
    round_id = HiddenField('Round ID', validators=[DataRequired()])
    fund_id = HiddenField('Fund ID', validators=[DataRequired()])
    title_en = StringField('Title', validators=[DataRequired()])
    short_name = StringField('Short Name', validators=[DataRequired(), Length(max=6)])
    opens = DateTimeField('Opens')
    deadline = DateTimeField('Deadline')
    assessment_start = DateTimeField('Assessment Start')
    reminder_date = DateTimeField('Reminder Date')
    assessment_deadline = DateTimeField('Assessment Deadline')
    prospectus_link = URLField('Prospectus', validators=[DataRequired()])
    privacy_notice_link = URLField('Privacy Notice', validators=[DataRequired()])

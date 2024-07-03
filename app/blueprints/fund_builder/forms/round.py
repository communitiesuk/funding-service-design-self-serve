from flask_wtf import FlaskForm
from wtforms import DateTimeField
from wtforms import HiddenField
from wtforms import StringField
from wtforms import URLField
from wtforms.validators import DataRequired
from wtforms.validators import Length


class RoundForm(FlaskForm):
    round_id = HiddenField("Round ID")
    fund_id = HiddenField("Fund ID")
    title_en = StringField("Title", validators=[DataRequired()])
    short_name = StringField("Short Name", validators=[DataRequired(), Length(max=6)])
    opens = DateTimeField("Opens")
    deadline = DateTimeField("Deadline")
    assessment_start = DateTimeField("Assessment Start")
    reminder_date = DateTimeField("Reminder Date")
    assessment_deadline = DateTimeField("Assessment Deadline")
    prospectus_link = URLField("Prospectus", validators=[DataRequired()])
    privacy_notice_link = URLField("Privacy Notice", validators=[DataRequired()])

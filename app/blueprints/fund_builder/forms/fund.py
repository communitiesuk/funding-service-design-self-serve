

from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length

class FundForm(FlaskForm):
    fund_id = HiddenField('Fund ID', validators=[DataRequired()])
    name_en = StringField('Name', validators=[DataRequired()])
    title_en = StringField('Title', validators=[DataRequired()])
    short_name = StringField('Short Name', validators=[DataRequired(), Length(max=6)])
    description_en = StringField('Description', validators=[DataRequired()])
    welsh_available = BooleanField('Welsh Available')
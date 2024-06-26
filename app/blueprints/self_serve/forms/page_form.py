
from wtforms import StringField, SelectMultipleField, HiddenField, BooleanField
from wtforms.validators import InputRequired
from flask_wtf import FlaskForm


class PageForm(FlaskForm):

    def validate_pages(form, field):
        pass

    id = StringField(
        label="Page ID",
        validators=[InputRequired(message="Supply a unique ID")],
    )
    builder_display_name = StringField(label="Display Name in this tool", validators=[InputRequired(message="Supply a name for this page in this tool")])
    form_display_name = StringField(label="Page Name", validators=[InputRequired(message="Supply a name for this page")])
    selected_components = SelectMultipleField(validate_choice=False) #choices=[], validators=[validate_pages])
    show_in_builder=BooleanField(label="Display in Build Form tool", default=True)

    def as_dict(self):
        return {field_name: field.data for field_name, field in self._fields.items()}

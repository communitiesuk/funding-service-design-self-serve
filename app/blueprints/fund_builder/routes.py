from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import url_for

from app.blueprints.fund_builder.forms.fund import FundForm

build_fund_bp = Blueprint(
    "build_fund_bp",
    __name__,
    url_prefix="/",
    template_folder="templates",
)


@build_fund_bp.route("/fund", methods=["GET", "POST"])
def fund():
    form = FundForm()
    if form.validate_on_submit():
        # TODO save fund
        flash(f"Saved fund {form.name_en.data}")
        return redirect(url_for("self_serve_bp.index"))

    return render_template("fund.html", form=form)

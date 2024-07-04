from datetime import datetime

from flask import Blueprint
from flask import flash
from flask import redirect
from flask import render_template
from flask import request
from flask import url_for

from app.blueprints.fund_builder.forms.fund import FundForm
from app.blueprints.fund_builder.forms.round import RoundForm
from app.db.models.fund import Fund
from app.db.models.round import Round
from app.db.queries.fund import add_fund
from app.db.queries.fund import get_all_funds
from app.db.queries.fund import get_fund_by_id
from app.db.queries.round import add_round
from app.db.queries.round import get_round_by_id

build_fund_bp = Blueprint(
    "build_fund_bp",
    __name__,
    url_prefix="/",
    template_folder="templates",
)


def all_funds_as_govuk_select_items(all_funds: list) -> list:
    return [{"text": f"{f.short_name} - {f.name_json['en']}", "value": str(f.fund_id)} for f in all_funds]


@build_fund_bp.route("/fund/view", methods=["GET", "POST"])
def view_fund():
    params = {"all_funds": all_funds_as_govuk_select_items(get_all_funds())}
    if request.method == "POST":
        fund_id = request.form.get("fund_id")
        fund = get_fund_by_id(fund_id)
        params["fund"] = fund

    return render_template("view_fund_config.html", **params)


@build_fund_bp.route("/fund/round/<round_id>/application_config")
def view_app_config(round_id):
    round = get_round_by_id(round_id)
    fund = get_fund_by_id(round.fund_id)
    return render_template("view_application_config.html", round=round, fund=fund)


@build_fund_bp.route("/fund", methods=["GET", "POST"])
def fund():
    form: FundForm = FundForm()
    if form.validate_on_submit():
        add_fund(
            Fund(
                name_json={"en": form.name_en.data},
                title_json={"en": form.title_en.data},
                description_json={"en": form.description_en.data},
                welsh_available=form.welsh_available.data,
                short_name=form.short_name.data,
                audit_info={"user": "dummy_user", "timestamp": datetime.now().isoformat(), "action": "create"},
            )
        )
        flash(f"Saved fund {form.name_en.data}")
        return redirect(url_for("self_serve_bp.index"))

    return render_template("fund.html", form=form)


@build_fund_bp.route("/round", methods=["GET", "POST"])
def round():
    all_funds = get_all_funds()
    form: RoundForm = RoundForm()
    if form.validate_on_submit():
        add_round(
            Round(
                fund_id=form.fund_id.data,
                audit_info={"user": "dummy_user", "timestamp": datetime.now().isoformat(), "action": "create"},
                title_json={"en": form.title_en.data},
                short_name=form.short_name.data,
                opens=form.opens.data,
                deadline=form.deadline.data,
                assessment_start=form.assessment_start.data,
                reminder_date=form.reminder_date.data,
                assessment_deadline=form.assessment_deadline.data,
                prospectus_link=form.prospectus_link.data,
                privacy_notice_link=form.privacy_notice_link.data,
            )
        )

        flash(f"Saved round {form.title_en.data}")
        return redirect(url_for("self_serve_bp.index"))

    return render_template(
        "round.html",
        form=form,
        all_funds=all_funds_as_govuk_select_items(all_funds),
    )

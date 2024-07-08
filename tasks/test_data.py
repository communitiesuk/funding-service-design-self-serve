from datetime import datetime
from uuid import uuid4

from app.db.models import Component
from app.db.models import ComponentType
from app.db.models import Criteria
from app.db.models import Form
from app.db.models import Fund
from app.db.models import Page
from app.db.models import Round
from app.db.models import Section
from app.db.models import Subcriteria
from app.db.models import Theme


def init_data():
    f: Fund = Fund(
        fund_id=uuid4(),
        name_json={"en": "Salmon Fishing Fund"},
        title_json={"en": "funding to improve access to salmon fishing"},
        description_json={
            "en": "A £10m fund to improve access to salmong fishing facilities across the devolved nations."
        },
        welsh_available=False,
        short_name="SFF",
    )

    r: Round = Round(
        round_id=uuid4(),
        fund_id=f.fund_id,
        audit_info={"user": "dummy_user", "timestamp": datetime.now().isoformat(), "action": "create"},
        title_json={"en": "round the first"},
        short_name="R1",
        opens=datetime.now(),
        deadline=datetime.now(),
        assessment_start=datetime.now(),
        reminder_date=datetime.now(),
        assessment_deadline=datetime.now(),
        prospectus_link="http://www.google.com",
        privacy_notice_link="http://www.google.com",
    )
    r2: Round = Round(
        round_id=uuid4(),
        fund_id=f.fund_id,
        audit_info={"user": "dummy_user", "timestamp": datetime.now().isoformat(), "action": "create"},
        title_json={"en": "round the second"},
        short_name="R2",
        opens=datetime.now(),
        deadline=datetime.now(),
        assessment_start=datetime.now(),
        reminder_date=datetime.now(),
        assessment_deadline=datetime.now(),
        prospectus_link="http://www.google.com",
        privacy_notice_link="http://www.google.com",
    )

    s1: Section = Section(
        section_id=uuid4(), index=1, round_id=r.round_id, name_in_apply={"en": "Organisation Information"}
    )
    f1: Form = Form(
        form_id=uuid4(),
        section_id=s1.section_id,
        name_in_apply={"en": "About your organisation"},
        section_index=1,
        runner_publish_name="about-your-org",
    )
    f2: Form = Form(
        form_id=uuid4(),
        section_id=s1.section_id,
        name_in_apply={"en": "Contact Details"},
        section_index=2,
        runner_publish_name="contact-details",
    )
    p1: Page = Page(
        page_id=uuid4(),
        form_id=f1.form_id,
        display_path="organisation-name",
        name_in_apply={"en": "Organisation Name"},
        form_index=1,
    )
    p2: Page = Page(
        page_id=uuid4(),
        display_path="organisation-address",
        form_id=f1.form_id,
        name_in_apply={"en": "Organisation Address"},
        form_index=3,
    )
    p3: Page = Page(
        page_id=uuid4(),
        form_id=f2.form_id,
        display_path="lead-contact-details",
        name_in_apply={"en": "Lead Contact Details"},
        form_index=1,
    )
    p4: Page = Page(
        page_id=uuid4(),
        form_id=f2.form_id,
        display_path="organisation-alternative-names",
        name_in_apply={"en": "Alternative names of your organisation"},
        form_index=2,
    )
    cri1: Criteria = Criteria(criteria_id=uuid4(), index=1, round_id=r.round_id, name="Unscored", weighting=0.0)
    sc1: Subcriteria = Subcriteria(
        subcriteria_id=uuid4(), criteria_index=1, criteria_id=cri1.criteria_id, name="Organisation Information"
    )
    t1: Theme = Theme(
        theme_id=uuid4(), subcriteria_id=sc1.subcriteria_id, name="General Information", subcriteria_index=1
    )
    t2: Theme = Theme(theme_id=uuid4(), subcriteria_id=sc1.subcriteria_id, name="Contact Details", subcriteria_index=1)
    c4: Component = Component(
        component_id=uuid4(),
        page_id=p3.page_id,
        title="Main Contact Name",
        type=ComponentType.TEXT_FIELD,
        page_index=1,
        theme_id=t2.theme_id,
        theme_index=1,
        options={"hideTitle": False, "classes": ""},
    )
    c5: Component = Component(
        component_id=uuid4(),
        page_id=p3.page_id,
        title="Main Contact Email",
        type=ComponentType.EMAIL_ADDRESS_FIELD,
        page_index=2,
        theme_id=t2.theme_id,
        theme_index=4,
        options={"hideTitle": False, "classes": ""},
    )
    c6: Component = Component(
        component_id=uuid4(),
        page_id=p3.page_id,
        title="Main Contact Address",
        type=ComponentType.UK_ADDRESS_FIELD,
        page_index=3,
        theme_id=t2.theme_id,
        theme_index=3,
        options={"hideTitle": False, "classes": ""},
    )
    c1: Component = Component(
        component_id=uuid4(),
        page_id=p1.page_id,
        title="What is your organisation's name?",
        hint_text="This must match the regsitered legal organisation name",
        type=ComponentType.TEXT_FIELD,
        page_index=1,
        theme_id=t1.theme_id,
        theme_index=1,
        options={"hideTitle": False, "classes": ""},
    )
    c3: Component = Component(
        component_id=uuid4(),
        page_id=p1.page_id,
        title="Does your organisation use any other names?",
        type=ComponentType.YES_NO_FIELD,
        page_index=2,
        theme_id=t1.theme_id,
        theme_index=2,
        options={"hideTitle": False, "classes": ""},
        conditions=[
            {
                "name": "organisation_other_names_no",
                "value": "false",  # this must be lowercaes or the navigation doesn't work
                "operator": "is",
                "destination_page_path": "CONTINUE",
            },
            {
                "name": "organisation_other_names_yes",
                "value": "true",  # this must be lowercaes or the navigation doesn't work
                "operator": "is",
                "destination_page_path": "organisation-alternative-names",
            },
        ],
    )
    c2: Component = Component(
        component_id=uuid4(),
        page_id=p2.page_id,
        title="What is your organisation's address?",
        hint_text="This must match the regsitered organisation address",
        type=ComponentType.UK_ADDRESS_FIELD,
        page_index=1,
        theme_id=t1.theme_id,
        theme_index=5,
        options={"hideTitle": False, "classes": ""},
    )
    c7: Component = Component(
        component_id=uuid4(),
        page_id=p4.page_id,
        title="Alternative Name 1",
        type=ComponentType.TEXT_FIELD,
        page_index=1,
        theme_id=t1.theme_id,
        theme_index=2,
        options={"hideTitle": False, "classes": ""},
    )
    return {
        "funds": [f],
        "rounds": [r, r2],
        "sections": [s1],
        "forms": [f1, f2],
        "pages": [p1, p2, p3],
        "components": [c1, c2, c3, c4, c5, c6],
        "criteria": [cri1],
        "subcriteria": [sc1],
        "themes": [t1, t2],
    }


def insert_test_data(db):
    test_data = init_data()
    db.session.bulk_save_objects(test_data["funds"])
    db.session.commit()
    db.session.bulk_save_objects(test_data["rounds"])
    db.session.commit()
    db.session.bulk_save_objects(test_data["sections"])
    db.session.commit()
    db.session.bulk_save_objects(test_data["forms"])
    db.session.commit()
    db.session.bulk_save_objects(test_data["pages"])
    db.session.commit()
    db.session.bulk_save_objects(test_data["criteria"])
    db.session.commit()
    db.session.bulk_save_objects(test_data["subcriteria"])
    db.session.commit()
    db.session.bulk_save_objects(test_data["themes"])
    db.session.commit()
    db.session.bulk_save_objects(test_data["components"])
    db.session.commit()

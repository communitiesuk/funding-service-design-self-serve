import ast
import json
import shutil
from datetime import date
from pathlib import Path

import pytest

from app.config_generator.scripts.generate_fund_round_config import (
    generate_config_for_round,
)
from app.config_generator.scripts.generate_fund_round_form_jsons import (
    generate_form_jsons_for_round,
)
from app.config_generator.scripts.generate_fund_round_html import (
    generate_all_round_html,
)
from app.config_generator.scripts.helpers import validate_json

output_base_path = Path("app") / "config_generator" / "output"


def test_generate_config_for_round_valid_input(seed_dynamic_data, monkeypatch):
    # Setup: Prepare valid input parameters
    fund_id = seed_dynamic_data["funds"][0].fund_id
    fund_short_name = seed_dynamic_data["funds"][0].short_name
    round_id = seed_dynamic_data["rounds"][0].round_id
    org_id = seed_dynamic_data["organisations"][0].organisation_id
    round_short_name = seed_dynamic_data["rounds"][0].short_name
    mock_round_base_paths = {round_short_name: 99}

    # Use monkeypatch to temporarily replace ROUND_BASE_PATHS
    import app.config_generator.scripts.generate_fund_round_config as generate_fund_round_config

    monkeypatch.setattr(generate_fund_round_config, "ROUND_BASE_PATHS", mock_round_base_paths)
    # Execute: Call the function with valid inputs
    result = generate_config_for_round(round_id)
    # Simply writes the files to the output directory so no result is given directly
    assert result is None
    # Assert: Check if the directory structure and files are created as expected
    expected_files = [
        {
            "path": output_base_path
            / round_short_name
            / "fund_store"
            / f"fund_config_{date.today().strftime('%d-%m-%Y')}.py",
            "expected_output": {
                "id": str(fund_id),
                "short_name": fund_short_name,
                "welsh_available": False,
                "owner_organisation_name": f"Ministry of Testing - {str(org_id)[:5]}",
                "owner_organisation_shortname": f"MoT-{str(org_id)[:5]}",
                "owner_organisation_logo_uri": "http://www.google.com",
                "name_json": {"en": "Unit Test Fund 1"},
                "title_json": {"en": "funding to improve testing"},
                "description_json": {"en": "A £10m fund to improve testing across the devolved nations."},
            },
        },
        {
            "path": output_base_path
            / round_short_name
            / "fund_store"
            / f"round_config_{date.today().strftime('%d-%m-%Y')}.py",
            "expected_output": {
                "id": str(round_id),
                "fund_id": str(fund_id),
                "short_name": round_short_name,
                "application_reminder_sent": False,
                "prospectus": "http://www.google.com",
                "privacy_notice": "http://www.google.com",
                "reference_contact_page_over_email": False,
                "contact_email": None,
                "contact_phone": None,
                "contact_textphone": None,
                "support_times": None,
                "support_days": None,
                "instructions_json": None,
                "feedback_link": None,
                "project_name_field_id": None,
                "application_guidance_json": None,
                "guidance_url": None,
                "all_uploaded_documents_section_available": None,
                "application_fields_download_available": None,
                "display_logo_on_pdf_exports": None,
                "mark_as_complete_enabled": None,
                "is_expression_of_interest": None,
                "eoi_decision_schema": None,
                "feedback_survey_config": {
                    "has_feedback_survey": None,
                    "has_section_feedback": None,
                    "is_feedback_survey_optional": None,
                    "is_section_feedback_optional": None,
                },
                "eligibility_config": {"has_eligibility": None},
                "title_json": {"en": "round the first"},
                "contact_us_banner_json": {"en": "", "cy": ""},
            },
        },
        {
            "path": output_base_path
            / round_short_name
            / "fund_store"
            / f"sections_config_{date.today().strftime('%d-%m-%Y')}.py",
            "expected_output": [
                {
                    "section_name": {"en": "1. Organisation Information", "cy": ""},
                    "tree_path": "99.1",
                    "requires_feedback": None,
                },
                {
                    "section_name": {"en": "1.1 About your organisation", "cy": ""},
                    "tree_path": "99.1.1",
                    "form_name_json": {"en": "about-your-org", "cy": ""},
                },
            ],
        },
    ]
    try:
        for expected_file in expected_files:
            path = expected_file["path"]
            assert path.exists(), f"Expected file {path} does not exist."

            with open(expected_file["path"], "r") as file:
                content = file.read()
                # Safely evaluate the Python literal structure
                # only evaluates literals and not arbitrary code
                data = ast.literal_eval(content)
                # remove keys that can't be accurately compared
                if isinstance(data, dict):
                    keys_to_remove = ["reminder_date", "assessment_start", "assessment_deadline", "deadline", "opens"]
                    data = {k: v for k, v in data.items() if k not in keys_to_remove}

                assert data == expected_file["expected_output"]
    finally:
        # Cleanup step to remove the directory
        directory_path = output_base_path / round_short_name
        if directory_path.exists():
            shutil.rmtree(directory_path)


def test_generate_config_for_round_invalid_input(seed_dynamic_data):
    # Setup: Prepare invalid input parameters
    round_id = None
    # Execute and Assert: Ensure the function raises an exception for invalid inputs
    with pytest.raises(ValueError):
        generate_config_for_round(round_id)


def test_generate_form_jsons_for_round_valid_input(seed_dynamic_data):
    # Setup: Prepare valid input parameters
    round_id = seed_dynamic_data["rounds"][0].round_id
    round_short_name = seed_dynamic_data["rounds"][0].short_name
    form_publish_name = seed_dynamic_data["forms"][0].runner_publish_name

    # Execute: Call the function with valid inputs
    generate_form_jsons_for_round(round_id)
    # Assert: Check if the directory structure and files are created as expected
    expected_files = [
        {
            "path": output_base_path / round_short_name / "form_runner" / f"{form_publish_name}.json",
            "expected_output": '{"metadata": {}, "startPage": "/intro-about-your-organisation", "backLinkText": "Go back to application overview", "pages": [{"path": "/organisation-name", "title": "Organisation Name", "components": [{"options": {"hideTitle": false, "classes": ""}, "type": "TextField", "title": "What is your organisation\'s name?", "hint": "This must match the regsitered legal organisation name", "schema": {}, "name": "organisation_name"}, {"options": {"hideTitle": false, "classes": ""}, "type": "RadiosField", "title": "How is your organisation classified?", "hint": "", "schema": {}, "name": "organisation_classification", "list": "classifications_list"}], "next": [{"path": "/summary"}], "options": {}}, {"path": "/intro-about-your-organisation", "title": "About your organisation", "components": [{"name": "start-page-content", "options": {}, "type": "Html", "content": "<p class=\\"govuk-body\\">None</p><p class=\\"govuk-body\\">We will ask you about:</p> <ul><li>Organisation Name</li></ul>", "schema": {}}], "next": [{"path": "/organisation-name"}], "options": {}, "controller": "./pages/start.js"}, {"path": "/summary", "title": "Check your answers", "components": [], "next": [], "section": "uLwBuz", "controller": "./pages/summary.js"}], "lists": [{"type": "string", "items": [{"text": "Charity", "value": "charity"}, {"text": "Public Limited Company", "value": "plc"}], "name": "classifications_list"}], "conditions": [], "fees": [], "sections": [], "outputs": [{"name": "update-form", "title": "Update form in application store", "type": "savePerPage", "outputConfiguration": {"savePerPageUrl": true}}], "skipSummary": false, "name": "About your organisation"}',  # noqa: E501
        }
    ]
    try:
        for expected_file in expected_files:
            path = expected_file["path"]
            assert path.exists(), f"Expected file {path} does not exist."

        with open(expected_file["path"], "r") as file:
            data = json.load(file)
            for page in data["pages"]:
                for component in page["components"]:
                    component.pop("metadata", None)
            expected = json.loads(expected_file["expected_output"])
            assert data == expected
    finally:
        # Cleanup step to remove the directory
        directory_path = output_base_path / round_short_name
        if directory_path.exists():
            shutil.rmtree(directory_path)


def test_generate_form_jsons_for_round_invalid_input(seed_dynamic_data):
    # Setup: Prepare invalid input parameters
    round_id = None
    # Execute and Assert: Ensure the function raises an exception for invalid inputs
    with pytest.raises(ValueError):
        generate_form_jsons_for_round(round_id)


def test_generate_fund_round_html(seed_dynamic_data):
    # Setup: Prepare valid input parameters
    round_id = seed_dynamic_data["rounds"][0].round_id
    round_short_name = seed_dynamic_data["rounds"][0].short_name
    # Execute: Call the function with valid inputs
    generate_all_round_html(round_id)
    # Assert: Check if the directory structure and files are created as expected
    expected_files = [
        {
            "path": output_base_path / round_short_name / "html" / "full_application.html",
            "expected_output": '<div class="govuk-!-margin-bottom-8">\n  <h2 class="govuk-heading-m ">\n    Table of contents\n  </h2>\n  <ol class="govuk-list govuk-list--number">\n    <li>\n      <a class="govuk-link" href="#organisation-information">\n        Organisation Information\n      </a>\n    </li>\n  </ol>\n  <hr class="govuk-section-break govuk-section-break--l govuk-section-break--visible" />\n  <h2 class="govuk-heading-l" id="organisation-information">\n    1. Organisation Information\n  </h2>\n  <h3 class="govuk-heading-m">\n    1.1. About your organisation\n  </h3>\n  <h4 class="govuk-heading-s">\n    1.1.1. Organisation Name\n  </h4>\n  <p class="govuk-body">\n    What is your organisation\'s name?\n  </p>\n  <p class="govuk-body">\n    This must match the regsitered legal organisation name\n  </p>\n  <p class="govuk-body">\n    How is your organisation classified?\n  </p>\n  <ul class="govuk-list govuk-list--bullet">\n    <li class="">\n      Charity\n    </li>\n    <li class="">\n      Public Limited Company\n    </li>\n  </ul>\n</div>',  # noqa: E501
        }
    ]
    try:
        for expected_file in expected_files:
            path = expected_file["path"]
            assert path.exists(), f"Expected file {path} does not exist."

        with open(expected_file["path"], "r") as file:
            data = file.read()
            assert data == expected_file["expected_output"]
    finally:
        # Cleanup step to remove the directory
        directory_path = output_base_path / round_short_name
        if directory_path.exists():
            shutil.rmtree(directory_path)


def test_generate_fund_round_html_invalid_input(seed_dynamic_data):
    # Setup: Prepare invalid input parameters
    round_id = None
    # Execute and Assert: Ensure the function raises an exception for invalid inputs
    with pytest.raises(ValueError):
        generate_all_round_html(round_id)


test_json_schema = {
    "type": "object",
    "properties": {"name": {"type": "string"}, "age": {"type": "number"}},
    "required": ["name", "age"],
}


def test_valid_data_validate_json():
    # Data that matches the schema
    data = {"name": "John Doe", "age": 30}
    result = validate_json(data, test_json_schema)
    assert result, "The data should be valid according to the schema"


@pytest.mark.parametrize(
    "data",
    [
        ({"age": 30}),  # Missing 'name'
        ({"name": 123}),  # 'name' should be a string
        ({"name": ""}),  # 'name' is empty
        ({}),  # Empty object
        ({"name": "John Doe", "extra_field": "not allowed"}),  # Extra field not defined in schema
        # Add more invalid cases as needed
    ],
)
def test_invalid_data_validate_json(data):
    result = validate_json(data, test_json_schema)
    assert not result, "The data should be invalid according to the schema"

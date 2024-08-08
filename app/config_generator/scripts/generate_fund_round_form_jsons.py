import json

from app.app import app
from app.config_generator.generate_form import build_form_json
from app.config_generator.scripts.helpers import write_config
from app.db.queries.round import get_round_by_id


def generate_form_jsons_for_round(round_id):
    """
    Generates JSON configurations for all forms associated with a given funding round.

    This function iterates through all sections of a specified funding round, and for each form
    within those sections, it generates a JSON configuration. These configurations are then written
    to files named after the forms, organized by the round's short name.

    Args:
        round_id (str): The unique identifier for the funding round.

    The generated files are named after the form names and are stored in a directory
    corresponding to the round's short name.
    """
    if not round_id:
        raise ValueError("Round ID is required to generate form JSONs.")
    forms_for_round = []
    round = get_round_by_id(round_id)
    app.logger.info(f"Generating form JSONs for round {round_id}.")
    for section in round.sections:
        for form in section.forms:
            result = build_form_json(form)
            form_json = json.dumps(result, indent=4)
            forms_for_round.append({"form_name": form.runner_publish_name, "json_str": form_json})
    for form in forms_for_round:
        write_config(form["json_str"], form["form_name"], round.short_name, "form_json")

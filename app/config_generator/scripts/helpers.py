import os
from dataclasses import asdict
from dataclasses import is_dataclass
from datetime import date

from app.blueprints.self_serve.routes import human_to_kebab_case
from app.blueprints.self_serve.routes import human_to_snake_case


def convert_to_dict(obj):
    if is_dataclass(obj):
        return asdict(obj)
    elif isinstance(obj, list):
        return [asdict(item) if is_dataclass(item) else item for item in obj]
    else:
        return obj


def write_config(config, filename, round_short_name, config_type):
    # Determine the base output directory
    base_output_dir = f"app/config_generator/output/{round_short_name}/"

    if config_type == "form_json":
        output_dir = os.path.join(base_output_dir, "form_runner/")
        content_to_write = config
        file_path = os.path.join(output_dir, f"{human_to_kebab_case(filename)}.json")
    elif config_type == "python_file":
        output_dir = os.path.join(base_output_dir, "fund_store/")
        config_dict = convert_to_dict(config)  # Convert config to dict for non-JSON types
        content_to_write = str(config_dict)
        file_path = os.path.join(output_dir, f"{human_to_snake_case(filename)}_{date.today().strftime('%d-%m-%Y')}.py")
    elif config_type == "html":
        output_dir = os.path.join(base_output_dir, "html/")
        content_to_write = config
        file_path = os.path.join(output_dir, f"{filename}.html")

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Write the content to the file
    with open(file_path, "w") as f:
        if config_type == "form_json":
            f.write(content_to_write)  # Write JSON string directly
        elif config_type == "python_file":
            print(content_to_write, file=f)  # Print the dictionary for non-JSON types
        elif config_type == "html":
            f.write(content_to_write)

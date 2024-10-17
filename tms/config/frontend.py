import os
import json

def load_config():
    # Define the project root directory
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

    # Construct the absolute path to the config file
    config_path = os.path.join(project_root, 'frontend', 'config', 'config.json')
    print(config_path)
    # Load the configuration from the JSON file
    try:
        with open(config_path, 'r', encoding='utf-8') as config_file:
            return json.load(config_file)
    except FileNotFoundError:
        print(f"Configuration file not found at: {config_path}")
    except json.JSONDecodeError:
        print("Error decoding JSON from the configuration file.")

    return None


if __name__ == "__main__":
    config_data = load_config()
    if config_data is not None:
        print(config_data)

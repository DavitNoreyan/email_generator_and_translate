from typing import Any, Dict

from generator import EmailGenerator
from settings.validators import validate_application_configs
from translator.translate_file import Translator
from utils import ArgParser


def generate_email(arguments):
    print("Starting emails generator...")
    application_configs = validate_application_configs(arguments)
    email_generator = EmailGenerator(application_configs)
    email_generator.setup()
    email_generator.generate_emails()
    print("Email(s) generated. ")


def translate_file(arguments):
    print("Starting file(s) translation...")
    file_translator = Translator(path=arguments.get(f"source"), target=arguments.get("lang"))
    file_translator.translate_text()
    print("File(s) translation finished.")


def main():
    arg_parser = ArgParser()
    arguments: Dict[str, Any] = arg_parser.get_args()
    if arguments["action"] == "generate":
        generate_email(arguments)
    else:
        translate_file(arguments)


if __name__ == "__main__":
    main()

from generator.body_generators.attachements_handler import EXTENSIONS_CONTENT_TYPE_MAPPING
from settings.validators.body_custom_validators import check_directory_contains_file_with_extension, \
    check_directory_contains_files_with_extension

COMMON_REQUIRED_FIELDS = ["charset", "content_transfer_encoding"]
COMMON_OPTIONAL_FIELDS = ["language"]
GENERATE_HTML_FIELDS = ["html_sentence_words_max_count", "html_tags_count"]
READ_OR_GENERATE_HTML_FIELDS = GENERATE_HTML_FIELDS + ["html_text_folder"]
GENERATE_PLAIN_FIELDS = ["plain_length"]
READ_OR_GENERATE_PLAIN_FIELDS = GENERATE_PLAIN_FIELDS + ["plain_text_folder"]
ATTACHMENT_EXTENSION_LIST = list(EXTENSIONS_CONTENT_TYPE_MAPPING.keys())
IMAGE_EXTENSION_LIST = ['jpeg', 'jpg', 'png', 'gif', 'tiff', 'tiff', 'psd', 'pdf', 'esp', 'al', 'indd',
                        'cr2', 'crw', 'nef', 'pef']
TYPE_SUB_TYPE_REQUIREMENTS_MAPPING = {
    "text": {
        "plain": {
            "required": COMMON_REQUIRED_FIELDS,
            "optional": COMMON_OPTIONAL_FIELDS + ["text_length", "folder_path"],
            "custom_validator": [(check_directory_contains_file_with_extension, "folder_path", "txt")]
        },
        "html": {
            "required": COMMON_REQUIRED_FIELDS,
            "optional": COMMON_OPTIONAL_FIELDS + GENERATE_HTML_FIELDS + ["file_path", "folder_path"],
            "custom_validator": [(check_directory_contains_file_with_extension, "folder_path", "html")]

        }
    },
    "multipart": {
        "alternative": {
            "required": COMMON_REQUIRED_FIELDS,
            "optional": COMMON_OPTIONAL_FIELDS + READ_OR_GENERATE_PLAIN_FIELDS + READ_OR_GENERATE_HTML_FIELDS,
            "custom_validator": [(check_directory_contains_file_with_extension, "plain_text_folder", "txt"),
                                 (check_directory_contains_file_with_extension, "html_text_folder", "html")]
        },
        'related': {
            "required": COMMON_REQUIRED_FIELDS,
            "optional": COMMON_OPTIONAL_FIELDS + READ_OR_GENERATE_PLAIN_FIELDS + READ_OR_GENERATE_HTML_FIELDS + [
                "image_folder"],
            "custom_validator": [(check_directory_contains_file_with_extension, "plain_text_folder", "txt"),
                                 (check_directory_contains_file_with_extension, "html_text_folder", "html"),
                                 (check_directory_contains_files_with_extension, "image_folder", IMAGE_EXTENSION_LIST)]

        },
        "mixed": {
            "required": COMMON_REQUIRED_FIELDS,
            "optional": COMMON_OPTIONAL_FIELDS + READ_OR_GENERATE_PLAIN_FIELDS + READ_OR_GENERATE_HTML_FIELDS + [
                "image_folder", "attachments_folder"],
            "custom_validator": [(check_directory_contains_file_with_extension, "plain_text_folder", "txt"),
                                 (check_directory_contains_file_with_extension, "html_text_folder", "html"),
                                 (check_directory_contains_files_with_extension, "image_folder", IMAGE_EXTENSION_LIST),
                                 (check_directory_contains_files_with_extension, "attachments_folder",
                                  ATTACHMENT_EXTENSION_LIST)]
        },
        "report": {
            "required": ["charset", "content_transfer_encoding", "content_type", "message_charset"],
            "optional": ["language", "report_type", "plain_length", "plain_text_folder", "html_text_folder",
                         "image_folder", "body_type",
                         "attachments_folder", "html_sentence_words_max_count", "html_tags_count", "external_file_path",
                         "max_symbols_count", "partial_files_folder", "request_link", "request_method",
                         "request_headers", "request_body", "request_params", "request_part"],
            "custom_validator": [(check_directory_contains_file_with_extension, "plain_folder", "txt"),
                                 (check_directory_contains_file_with_extension, "html_folder", "html"),
                                 (check_directory_contains_files_with_extension, "image_folder", IMAGE_EXTENSION_LIST),
                                 (check_directory_contains_files_with_extension, "attachments_folder",
                                  ATTACHMENT_EXTENSION_LIST)]
        }

    }
}

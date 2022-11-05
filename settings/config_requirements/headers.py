# todo change strs to dicts , each dict shoul containt configuration property name ,
# todo or names and function which generating the header

email_address_configs = {
    "optional_arguments": ["with_display_name", "email_local_name_length", "email_service_name_length",
                           "domain_length", "email_service_list"],
    "required_arguments": ["count", "language", "charset"],
    "fields_providing_via_file": {
        "required_arguments": ["email_addresses"],
        "optional_arguments": ["display_names"]
    }
}

msg_id_configs = {
    "optional_arguments": ["idstring", "domain"],
    "required_arguments": [],
}
multiple_msg_id_configs = {**msg_id_configs, "optional_arguments": [*msg_id_configs["optional_arguments"], "count"]}
text_header_configs = {
    "optional_arguments": [],
    "required_arguments": ["language", "length"],
}
date_header_configs = {
    "optional_arguments": ["year",
                           "month",
                           "day",
                           "hour",
                           "second",
                           "ms"
                           ],
    "required_arguments": [],
}
SUPPORTED_HEADERS = {
    # "Apparently-To": {
    #     "optional_arguments": [],
    #     "required_arguments": [],
    # },
    "bcc": {**email_address_configs, "header_name": "Bcc"},
    "cc": {**email_address_configs, "header_name": "Cc"},
    "comments": {**text_header_configs, "header_name": "Comments"},
    "date": {**date_header_configs, "header_name": "Date"},
    "errors-to": {**email_address_configs, "header_name": "Errors-To"},
    "from": {**email_address_configs, "header_name": "From"},
    "message-id": {**msg_id_configs, "header_name": "Message-Id"},
    "in-reply-to": {**multiple_msg_id_configs, "header_name": "In-Reply-To"},
    "mime-version": {
        "optional_arguments": ["version", "subversion"],
        "required_arguments": [],
        "header_name": "Mime-Version"
    },
    "newsgroups": {
        "optional_arguments": ["count", "domain_length", "subdomain_length",
                               "news_groups"],
        "required_arguments": [],
        "header_name": "Newsgroups"
    },
    "organization": {**text_header_configs, "header_name": "Organization"},
    "priority": {
        "optional_arguments": ["value"],
        "required_arguments": [],
        "header_name": "Priority"
    },
    "received": {
        "optional_arguments": ["receiving_type", "from_domain", "with_ip", "domain", "smtp_protocol", "receiving_year",
                               "receiving_month", "receiving_day", "receiving_hour", "receiving_minute",
                               "receiving_second",
                               ],
        "required_arguments": [],
        "header_name": "Received"
    },
    "references": {**msg_id_configs, "header_name": "References"},
    "reply-to": {**email_address_configs, "header_name": "Reply-To"},
    "sender": {**email_address_configs, "header_name": "Sender"},
    "subject": {**text_header_configs, "header_name": "Subject"},
    "to": {**email_address_configs, "header_name": "To"},
}

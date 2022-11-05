from .email_address_header_generator import generate_email_address_header
from .email_date_generator import generate_date_header
from .header_with_random_text_generator import header_with_random_text_generator
from .mime_version_generator import generate_mime
from .msg_id_generator import bulk_msg_id_generator, generate_message_id
from .news_gropus_generator import generate_news_groups
from .priority_header_generator import generate_priority_header
from .received_header_generator import generate_received_header

# Below described header-generator mapping for all supported headers
# In each generator arguments will not be checked because all arguments coming checked and cleaned
# from the defaults parsing process

# TODO check outlook documentations for X-headers , check again Apparently-to header

HEADERS_GENERATORS_MAPPER = {
    # "Apparently-To": ,
    "Bcc": generate_email_address_header,
    "Cc": generate_email_address_header,
    "Comments": header_with_random_text_generator,
    "Date": generate_date_header,
    "Errors-To": generate_email_address_header,
    "From": generate_email_address_header,
    "Message-Id": generate_message_id,
    "In-Reply-To": bulk_msg_id_generator,
    "Mime-Version": generate_mime,
    "Newsgroups": generate_news_groups,
    "Organization": header_with_random_text_generator,
    "Priority": generate_priority_header,
    "Received": generate_received_header,
    "References": generate_message_id,
    "Reply-To": generate_email_address_header,
    "Sender": generate_email_address_header,
    "Subject": header_with_random_text_generator,
    "To": generate_email_address_header,
    # "X-headers": ,
    # "X-Confirm-Reading-To": ,
    # "X-Distribution": ,
    # "X-Errors-To": ,
    # "X-Mailer": ,
    # "X-Priority": ,
    # "X-Sender": ,
    # "X-UIDL":
}

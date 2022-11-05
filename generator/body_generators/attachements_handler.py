# read and add attaching files to email
from email.mime.application import MIMEApplication
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from logging import getLogger
from os.path import exists, splitext, basename
from typing import Union, List

logger = getLogger("info_logger")

DEFAULT_CONTENT_TYPE = "application/octet-stream"
EXTENSIONS_CONTENT_TYPE_MAPPING = {
    "css": "text/css",
    "csv": "text/csv ",
    "htm": "text/html",
    "html": "text/html",
    "asc": "text/plain",
    "c": "text/plain",
    "diff": "text/plain",
    "log": "text/plain",
    "patch": "text/plain",
    "pot": "text/plain",
    "text": "text/plain",
    "txt": "text/plain",
    "gif": "image/gif",
    "jpeg": "image/jpeg",
    "jpg": "image/jpeg",
    "jpe": "image/jpeg",
    "png": "image/png",
    "tif": "image/tiff",
    "tiff": "image/tiff",
    "mpeg": "video/mpeg",
    "mpg": "video/mpeg",
    "mpe": "video/mpeg",
    "mp4": "video/mp4",
    "qt": "video/quicktime",
    "mov": "video/quicktime",
    "wmv": "video/x-ms-wmv",
    "avi": "video/x-msvideo",
    "doc": "application/msword",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "dotx": "application/vnd.openxmlformats-officedocument.wordprocessingml.template",
    "docm": "application/vnd.ms-word.document.macroEnabled.12 ",
    "dotm": "application/vnd.ms-word.template.macroEnabled.12",
    "xls": "application/vnd.ms-excel",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "xltx": "application/vnd.openxmlformats-officedocument.spreadsheetml.template",
    "xlsm": "application/vnd.ms-excel.sheet.macroEnabled.12",
    "xltm": "application/vnd.ms-excel.template.macroEnabled.12",
    "xlam": "application/vnd.ms-excel.addin.macroEnabled.12",
    "xlsb": "application/vnd.ms-excel.sheet.binary.macroEnabled.12",
    "ppt": "application/vnd.ms-powerpoint",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
    "potx": "application/vnd.openxmlformats-officedocument.presentationml.template",
    "ppsx": "application/vnd.openxmlformats-officedocument.presentationml.slideshow ",
    "ppam": "application/vnd.ms-powerpoint.addin.macroEnabled.12",
    "pptm": "application/vnd.ms-powerpoint.presentation.macroEnabled.12",
    "ppsm": "application/vnd.ms-powerpoint.slideshow.macroEnabled.12",
    "potm": "application/vnd.ms-powerpoint.template.macroEnabled.12",
    "sldm": "application/vnd.ms-powerpoint.slide.macroEnabled.12",
    "pps": "application/vnd.openxmlformats-officedocument.presentationml.slide",
    "one": "application/msonenote",
    "thmx": "application/vnd.ms-officetheme",
    "key": "application/vnd.apple.keynote",
    "pdf": "application/pdf",
}


def create_attachment(attachment_path: str) -> \
        Union[MIMEBase, MIMEApplication, MIMEText, MIMEImage, MIMEText, MIMEAudio, None]:
    # todo write docs
    if not exists(attachment_path):
        return None
    filename, file_extension = splitext(attachment_path)
    content_type = EXTENSIONS_CONTENT_TYPE_MAPPING.get(file_extension[1:], DEFAULT_CONTENT_TYPE)
    [main_content_type, sub_content_type] = content_type.split("/")

    with open(attachment_path, "rb") as att_file:
        file_data = att_file.read()

    if main_content_type == "text":
        attachment = MIMEText(_text=str(file_data), _subtype=sub_content_type)
    elif main_content_type == "image":
        attachment = MIMEImage(_imagedata=file_data, _subtype=sub_content_type)
    elif main_content_type == "video":
        attachment = MIMEBase(_maintype=main_content_type, _subtype=sub_content_type)
        attachment.set_payload(file_data)
    else:
        attachment = MIMEApplication(_data=file_data, _subtype=sub_content_type)
    attachment.add_header('Content-Disposition', f"attachment; filename={basename(attachment_path)}")
    return attachment


def create_attachments(attachment_paths: List[str]) -> \
        List[Union[MIMEBase, MIMEApplication, MIMEText, MIMEImage, MIMEAudio]]:
    created_attachments = []
    for att_path in attachment_paths:
        created_attachment = create_attachment(att_path)
        if created_attachment:
            created_attachments.append(created_attachment)
    return created_attachments

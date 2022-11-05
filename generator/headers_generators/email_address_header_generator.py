from email.header import Header
from email.utils import formataddr
from random import choice
from typing import Optional, List

from generator.utils import random_email_address_generator, random_f_name_s_name_generator, change_charset_encoding


# There are email address and user_name + email_address generators


def email_with_display_name_generator(language: str, charset: str, email_local_name_length: int,
                                      email_service_name_length: Optional[int] = None,
                                      domain_length: Optional[int] = None,
                                      email_service_list: Optional[List[str]] = None) -> str:
    """
    Generating email address with display name.
    Example FirstName LastName <address@email.com>
    :param email_service_list:if got this argument email service name and domain will not be generated,
    it will be chosen from the got list randomly
    :param domain_length: generating domain length ( chars count )
    :param email_service_name_length:  generating email service name length ( chars count )
    :param email_local_name_length: generating user name length ( chars count )
    :param language: will be used in user firstname and lastname generating process
    :param charset: will be used for address formatting according to RFC standards
    :return: formatted email with display name and email address
    """
    a = random_f_name_s_name_generator(language, 10, 10)
    return formataddr((a,
                       random_email_address_generator(email_local_name_length=email_local_name_length,
                                                      email_service_name_length=email_service_name_length,
                                                      domain_length=domain_length,
                                                      email_service_list=email_service_list)), charset=charset)


def email_address_generator(email_local_name_length: Optional[int] = None,
                            email_service_name_length: Optional[int] = None,
                            domain_length: Optional[int] = None,
                            email_service_list: Optional[List[str]] = None) -> str:
    """
    Returning random generated email address.
    :return: formatted email according rfc standards
    """
    return formataddr((None, random_email_address_generator(email_local_name_length=email_local_name_length,
                                                            email_service_name_length=email_service_name_length,
                                                            domain_length=domain_length,
                                                            email_service_list=email_service_list)), charset="ascii")


def email_address_list_generator(count: int, charset: str, lang: Optional[str] = None,
                                 with_display_name: bool = False, email_local_name_length: Optional[int] = None,
                                 email_service_name_length: Optional[int] = None,
                                 domain_length: Optional[int] = None,
                                 email_service_list: Optional[List[str]] = None) -> str:
    """
    Generating multiple email address with or without display name.
    Generated email addresses will be concatenated with comma according RFC standards.
        :param email_service_list:if got this argument email service name and domain will not be generated,
    it will be chosen from the got list randomly
    :param domain_length: generating domain length ( chars count )
    :param email_service_name_length:  generating email service name length ( chars count )
    :param email_local_name_length: generating user name length ( chars count )
    :param count: generating email address count
    :param charset: will be used in email address formatting process
    :param lang: will be used in display name generating process
    :param with_display_name: if True generating email will be with display name,
    otherwise only email addresses will be generated
    :return: comma seperated email addresses
    """
    generated_emails = []
    for _ in range(count):
        if with_display_name:
            generated_emails.append(email_with_display_name_generator(language=lang, charset=charset,
                                                                      email_local_name_length=email_local_name_length,
                                                                      email_service_name_length=email_service_name_length,
                                                                      domain_length=domain_length,
                                                                      email_service_list=email_service_list))
        else:
            generated_emails.append(email_address_generator())
    return " , ".join(generated_emails)


def create_content_from_file_data(charset: str, email_addresses: List[str], display_names: List[str],
                                  count: int) -> str:
    #     todo write docs
    if count:
        generated_emails = []
        for _ in range(count):
            display_name = None if not display_names else choice(display_names)
            generated_emails.append(formataddr((display_name, choice(email_addresses)), charset=charset))
        return " , ".join(generated_emails)
    display_name = None if not display_names else choice(display_names)
    return formataddr((display_name, choice(email_addresses)), charset)


def generate_email_address_header(charset: str, header_name: str, with_display_name: bool = False,
                                  language: Optional[str] = None,
                                  count: Optional[int] = None, email_local_name_length: Optional[int] = None,
                                  email_service_name_length: Optional[int] = None,
                                  domain_length: Optional[int] = None,
                                  email_service_list: Optional[List[str]] = None,
                                  display_names: Optional[List[str]] = None,
                                  email_addresses: Optional[List[str]] = None
                                  ) -> Header:
    """
    Generating email address(es) , creating and email.headers.Header instance with generated value.
    :param email_addresses: got in case if reading values from json
    :param display_names: got in case if reading values from json
    :param email_service_list:if got this argument email service name and domain will not be generated,
    it will be chosen from the got list randomly
    :param domain_length: generating domain length ( chars count )
    :param email_service_name_length:  generating email service name length ( chars count )
    :param email_local_name_length: generating user name length ( chars count )
    :param charset: will be used in email address generating process
    :param header_name: will set up as header_name property for email.headers.Header instance
    :param with_display_name:  if True generating email will be with display name,
    otherwise only email addresses will be generated
    :param language: will be used in display name generating process
    :param count: generating email address count
    :return: email.headers.Header instance with generated value and got header_name
    """
    change_charset_encoding(charset, "q")
    if email_addresses:
        content = create_content_from_file_data(charset, email_addresses, display_names, count)
    else:
        if not count:
            if with_display_name:
                content = email_with_display_name_generator(language=language, charset=charset,
                                                            email_local_name_length=email_local_name_length,
                                                            email_service_name_length=email_service_name_length,
                                                            domain_length=domain_length,
                                                            email_service_list=email_service_list)
            else:
                content = email_address_generator()
        else:
            content = email_address_list_generator(count=count, charset=charset, lang=language,
                                                   with_display_name=with_display_name,
                                                   email_local_name_length=email_local_name_length,
                                                   email_service_name_length=email_service_name_length,
                                                   domain_length=domain_length,
                                                   email_service_list=email_service_list)
    return Header(s=content, header_name=header_name)

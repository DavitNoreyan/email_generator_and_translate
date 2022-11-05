# Table of Content

* [System Requirements](#system-requirements)
* [Installation](#installation)
* [How To Run](#how-to-run)
* [Configuring generating email's headers](*configuring-gen-params)
* [Configuring generating email's headers](#Configuring-generating-email's-headers)
  ​

# System Requirements:

### Run parameters

- ```--log_handler``` - run specific class tests -- Supported values ```file_handler```, ```console```
  -- Default value is ```file_handler```
  -- Parameter is optional
- ```action``` - generate email or translate specified text file(s)
  -- Supported values ```generate```, ```tranlsate```
  -- Parameter is required

```sh
python3 run.py --log_handler console
python3 main.py generate
```  

or

```sh
python3 main.py translate
```  

- ```--log_handler``` - run specific class tests \
  Supported values ```file_handler```, ```console``` \
  Default value is ```file_handler``` \
  Parameter is ```optional```

```sh
python3 main.py generate --log_handler console
```

- ```--body_cfg```
  use in email generating case \
  Supported value ```json file path``` \
  Parameter is ```optional```

```sh
python3 main.py generate --body_cfg \my\file\path.json
```

- ```--headers_cfg```
  Use in email generating case \
  Supported value ```json file path``` \
  Parameter is ```optional```

```sh
python3 main.py generate --headers_cfg \my\file\path.json
```

- ```--app_cfg```
  Use in email generating case \
  Supported value ```json file path``` \
  Parameter is ```optional```

```sh
python3 main.py generate --app_cfg \my\file\path.json
```

- ```--lang```
  Use in email translating case \
  Supported value ```language code``` \
  Parameter is ```optional``` \
  Default value is ```en```

```sh
python3 main.py tranlate --lang ru
```

- ```--source```
  Use in email translating case \
  Supported value ```txt file path or directory with txt files``` \
  Parameter is ```required```

```sh
python3 main.py source --app_cfg \my\file\path.txt
```

or

```sh
python3 main.py source --app_cfg \my\folder\with\txts\path
```

# Email Generator configuration

## Email headers

Open `settings/configs/headers.json` file
\
Add the header which should be used in email generating process\
You can specify your own json file for describing the properties and requirements.

Supported headers and its required and optional arguments:

#### Bcc, Cc, Errors-To, From, Reply-To, Sender, Subject, To

Required arguments:

* count
* language
* charset
* value_from ( if values should be read from file )

Optional arguments:

* with_display_name
* email_local_name_length
* email_service_name_length
* domain_length
* email_service_list

If reading from file:

Required arguments:

* email_addresses

Optional arguments:

* display_names

#### Message-Id, In-Reply-To ( can be multiple ides ) , References

Optional arguments:

* domain
* idstring
* count ( for multiple ides )

#### Comments, Organization, Subject

Required arguments:

* language
* length

#### Date

Optional arguments:

* year
* month
* day
* hour
* second

#### Mime-Version

Optional arguments:

* version
* subversion

#### Newsgroups

Optional arguments:

* count
* domain_length
* subdomain_length
* news_groups

#### Priority

Optional arguments:

* value

#### Received

Optional arguments:

* receiving_type
* from_domain
* with_ip
* domain
* smtp_protocol
* receiving_year
* receiving_month
* receiving_day
* receiving_hour
* receiving_minute
* receiving_second

## Email body

Open `settings/configs/body.json` file,\
Configure the MIME structure, save file and run the generator \
If you have another json file you can provide the file's path via CLI argument

The json file should contain 3 main properties:

* type
* sub_type
* configs

type and sub_type is email's main type and subtype which should be generated. \
In configs property charset, content transfer encoding , language etc...should be specified \
Each type and subtype may have its specific configurations \
All types subtypes and its possible configs are described below.

Supported types and its subtypes are:

* text
    * plain
    * html
* multipart
    * alternative
    * related
    * mixed
    * report

charset and content_transfer_encoding are required for any type and sub_type\
the supported values for these configs are described below

* charset
    * utf-8
    * utf-16
    * utf-16le
    * utf-16be
    * ascii
    * windows-1250
    * windows-1251
    * windows-1252
    * iso-8859-1
    * iso-8859-2
    * iso-8859-5
* content_transfer_encoding
    * quoted-printable
    * base64
    * 7bit
    * 8bit

***If charset and content_transfer_encoding are not compatible to each other the appropriate exception should be
raised.***

**1. plain/text**

In case of plain text either appropriate configurations for generating the content or folder should be specified for
reading the content\
In case of email's **text generation** `language` and `text_length` should be specified.\
Example:

```json
{
  "type": "text",
  "sub_type": "plain",
  "configs": {
    "charset": "utf-8",
    "content_transfer_encoding": "quoted-printable",
    "language": "en",
    "text_length": 500
  }
}
```

In case of reading the text from the file, `folder_path` should be specified which contains txt files.

```json
{
  "type": "text",
  "sub_type": "plain",
  "configs": {
    "charset": "utf-8",
    "content_transfer_encoding": "7bit",
    "folder_path": "\directory\which\contains\txt\files"
  }
}
```

*If there are multiple txt files multiple emails should be generated.*

**2. html/text**

For html text as for plain there are 2 cases, generating the content and reading it from the file.\
In case of email's **text generation** `language`, `html_sentence_words_max_count` and `html_tags_count` should be
specified.\
Example:

```json
{
  "type": "text",
  "sub_type": "html",
  "configs": {
    "charset": "utf-8",
    "content_transfer_encoding": "7bit",
    "language": "en",
    "html_sentence_words_max_count": 20,
    "html_tags_count": 50
  }
}
```

In case of reading the text from the file, `folder_path` should be specified which contains html files.

```json
{
  "type": "text",
  "sub_type": "html",
  "configs": {
    "charset": "utf-8",
    "content_transfer_encoding": "7bit",
    "folder_path": "\directory\which\contains\html\files"
  }
}
```

*If there are multiple html files multiple emails should be generated.*

**3. multipart/alternative**

In case if email's **text should be generated** `language` , `plain_length`, `html_sentence_words_max_count`
and `html_tags_count` should be specified.\
Example:

```json
{
  "type": "multipart",
  "sub_type": "alternative",
  "configs": {
    "charset": "utf-8",
    "content_transfer_encoding": "7bit",
    "language": "fr",
    "plain_length": 100,
    "html_sentence_words_max_count": 50,
    "html_tags_count": 1
  }
}
```

If text should be read from file `html_text_folder` and `plain_text_folder` should be specified.\
Example:

```json
{
  "type": "multipart",
  "sub_type": "alternative",
  "configs": {
    "charset": "utf-8",
    "content_transfer_encoding": "7bit",
    "html_text_folder": "\directory\which\contains\html\files",
    "plain_text_folder": "\directory\which\contains\txt\files"
  }
}
```

**4. multipart/related**

Multipart related can be generated in multiple ways depending on requirements:

1. read html content with inner img tags ( images should be found and attached to email automatically )
2. html should be generated ( should be specified `image_folder` )
3. multipart/related should contain multipart/alternative body using as plain/text content provided txt file(s)
4. multipart/related should contain multipart/alternative body which plain/text part should be generated

In case of html `html_text_folder` should be provided, which contains html files with either img tags or without.\
*Image source in the html file(s) should be image's absolute path, otherwise it should be ignored.*
Examples:

with generating plain part

```json
{
  "type": "multipart",
  "sub_type": "related",
  "configs": {
    "charset": "utf-8",
    "content_transfer_encoding": "7bit",
    "language": "fr",
    "plain_length": 100,
    "html_text_folder": "\directory\which\contains\html\files"
  }
}
```

with reading plain part

```json
{
  "type": "multipart",
  "sub_type": "related",
  "configs": {
    "charset": "utf-8",
    "content_transfer_encoding": "7bit",
    "html_text_folder": "\directory\which\contains\html\files",
    "plain_text_folder": "\directory\which\contains\txt\files"
  }
}
```

In case of html generation you should provide `image_folder` which contains the images. \
Examples:

with generating plain part

```json
{
  "type": "multipart",
  "sub_type": "related",
  "configs": {
    "charset": "utf-8",
    "content_transfer_encoding": "7bit",
    "language": "fr",
    "plain_text_folder": "\directory\which\contains\txt\files",
    "html_sentence_words_max_count": 50,
    "html_tags_count": 10,
    "image_folder": "\directory\which\contains\image\files"
  }
}
```

with reading plain part

```json
{
  "type": "multipart",
  "sub_type": "related",
  "configs": {
    "charset": "utf-8",
    "content_transfer_encoding": "7bit",
    "language": "fr",
    "plain_length": 100,
    "html_sentence_words_max_count": 50,
    "html_tags_count": 10,
    "image_folder": "\directory\which\contains\image\files"
  }
}
```

**5. multipart/mixed**

All cases described above can be present here , only `attachments_folder` property should be added here.\
Example:

Open `settings/configs/body.json` file, configure the MIME structure, save file and run the generator.

```json
{
  "type": "multipart",
  "sub_type": "mixed",
  "configs": {
    "charset": "utf-8",
    "content_transfer_encoding": "7bit",
    "language": "fr",
    "plain_length": 100,
    "html_sentence_words_max_count": 50,
    "html_tags_count": 10,
    "image_folder": "\directory\which\contains\image\files",
    "attachments_folder": "\directory\which\contains\attachments"
  }
}
```

**6. multipart/report**

content-types:

1. message / delivery-status
2. message / disposition-notification-to
3. message / external-body
4. message / http
5. message / partial
6. message / rfc822

generated as part of multipart/report.\
In particular, the message/delivery-status or message/disposition-notification-to should be a mimetext, alternative or
related.

to generate message/delivery-status, you need to set the following configurations. \
Examples:

```json
{
  "type": "multipart",
  "sub_type": "report",
  "configs": {
    "report_type": "delivery-status",
    "image_paths": [],
    "charset": "utf-8",
    "message_charset": "ascii",
    "content_transfer_encoding": "quoted-printable",
    "language": "en",
    "html_sentence_words_max_count": 20,
    "html_tags_count": 20,
    "plain_length": 50,
    "body_type": "multipart/related",
    "content_type": "message/delivery-status",
    "action": "failed",
    "plain_text_folder": "\directory\which\contains\txt\files",
    "html_text_folder": "\directory\which\contains\html\files",
    "image_folder": "\directory\which\contains\image\files"
  }
}
```

to generate message/disposition-notification-to, you need to set the following configurations.\
Examples:

```json
{
  "type": "multipart",
  "sub_type": "report",
  "configs": {
    "report_type": "disposition-notification-to",
    "image_paths": [],
    "charset": "utf-8",
    "message_charset": "ascii",
    "content_transfer_encoding": "quoted-printable",
    "language": "en",
    "html_sentence_words_max_count": 20,
    "html_tags_count": 20,
    "plain_length": 50,
    "body_type": "multipart/related",
    "content_type": "message/disposition-notification-to",
    "action": "failed",
    "plain_text_folder": "\directory\which\contains\txt\files",
    "html_text_folder": "\directory\which\contains\html\files",
    "image_folder": "\directory\which\contains\image\files"
  }
}
```

to generate message/external-body, you need to set the following configurations.\
Examples:

```json
{
  "type": "multipart",
  "sub_type": "report",
  "configs": {
    "image_paths": [],
    "charset": "utf-8",
    "message_charset": "ascii",
    "content_transfer_encoding": "quoted-printable",
    "content_type": "message/external-body",
    "action": "failed",
    "partial_files_folder": "\directory\which\contains\txt\files"
  }
}
```

to generate message/http, you need to set the following configurations.\
Examples:

```json
{
  "type": "multipart",
  "sub_type": "report",
  "configs": {
    "charset": "utf-8",
    "content_type": "message/http",
    "message_charset": "ascii",
    "content_transfer_encoding": "quoted-printable",
    "language": "en",
    "request_link": "http://google.com",
    "request_headers": {
      "header": "value"
    },
    "request_method": "post",
    "request_body": {
      "key": "val"
    },
    "request_params": {
      "param": "value"
    },
    "request_part": "request"
  }
}
```

to generate message/partial, you need to set the following configurations.\
Examples:

```json
{
  "type": "multipart",
  "sub_type": "report",
  "configs": {
    "image_paths": [],
    "charset": "utf-8",
    "message_charset": "ascii",
    "content_transfer_encoding": "quoted-printable",
    "content_type": "message/partial",
    "action": "failed",
    "max_symbols_count": 400,
    "partial_files_folder": "\directory\which\contains\txt\files"
  }
}
```

to generate message/rfc822, you need to set the following configurations.\
Examples:

```json
{
  "type": "multipart",
  "sub_type": "report",
  "configs": {
    "image_paths": [],
    "charset": "utf-8",
    "message_charset": "ascii",
    "content_transfer_encoding": "quoted-printable",
    "language": "en",
    "plain_length": 50,
    "content_type": "message/rfc822",
    "plain_text_folder": "\directory\which\contains\txt\files"
  }
}
```


import argparse
from typing import Optional, Any, Dict


class ArgParser:

    def __init__(self):
        """
            Initializing args, which will used for storing handled arguments.
        """
        self.args: Optional[argparse.Namespace] = None

    def parse_cmd_arguments(self) -> None:
        """
            Parsing arguments and saving the parsed data into self.args.
        :return: None
        """
        parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        parser.add_argument("action", choices=["generate", "translate"],
                            help="Use this arguments for choose action , translate file or generate email."),
        parser.add_argument("--log_handler", default="file_handler", choices=["file_handler", "console"],
                            help="Use this arguments for configuring logs - should be displayed in cli ( console ) "
                                 "or write into log file ( file_handler ) ")
        parser.add_argument("--body_cfg",
                            help="Use this arguments for configuring body configuration json file path.")
        parser.add_argument("--headers_cfg",
                            help="Use this arguments for configuring headers configuration json file path.")
        parser.add_argument("--app_cfg",
                            help="Use this arguments for configuring application main configuration json file path.")
        parser.add_argument("--lang", default="en",
                            choices=['af', 'sq', 'am', 'ar', 'hy', 'az', 'eu', 'be', 'bn', 'bs', 'bg', 'ca', 'ceb',
                                     'ny', 'zh', 'zh-cn', 'zh-tw', 'co', 'hr', 'cs', 'da', 'nl', 'en', 'eo', 'et', 'tl',
                                     'fi', 'fr', 'fy', 'gl', 'ka', 'de', 'el', 'gu', 'ht', 'ha', 'haw', 'iw', 'hi',
                                     'hmn', 'hu', 'is', 'ig', 'id', 'ga', 'it', 'ja', 'jw', 'kn', 'kk', 'km', 'ko',
                                     'ku', 'ky', 'lo', 'la', 'lv', 'lt', 'lb', 'mk', 'mg', 'ms', 'ml', 'mt', 'mi', 'mr',
                                     'mn', 'my', 'ne', 'no', 'ps', 'fa', 'pl', 'pt', 'pa', 'ro', 'ru', 'sm', 'gd', 'sr',
                                     'st', 'sn', 'sd', 'si', 'sk', 'sl', 'so', 'es', 'su', 'sw', 'sv', 'tg', 'ta', 'te',
                                     'th', 'tr', 'uk', 'ur', 'uz', 'vi', 'cy', 'xh', 'yi', 'yo', 'zu', 'fil', 'he'],
                            help="Use this arguments for configuring target language for translation.")
        parser.add_argument("--source",
                            help="Use this arguments for configuring translating file or directory path.")
        self.args = parser.parse_args()

    def get_args(self) -> Dict[str, Any]:
        """
            Calling the self.parse_cmd_arguments method , which processing arguments and saving data into self.args.
        :return: Dict with parsed arguments.
        """
        if self.args is None:
            self.parse_cmd_arguments()
        return vars(self.args)

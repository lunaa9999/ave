import re


class Utils:
    @staticmethod
    def remove_special_characters(text):
        unwanted_chars = r'[\/\\:*?"<>|].'
        return re.sub(unwanted_chars, " ", text)

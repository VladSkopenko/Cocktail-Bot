from string import punctuation


def clean_text(text: str):
    return text.translate(str.maketrans("", "", punctuation))

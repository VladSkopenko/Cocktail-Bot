import re

from src.common.patterns_for_command import ABOUT

text1 = "Как работать с  ботом "
text2 = "Расскажи мне о себе"


def test_patterns_for_command():
    if re.match(ABOUT, text1):
        print("Соответствует")
    else:
        print("Не соответствует")

    if re.match(ABOUT, text2):
        print("Соответствует")
    else:
        print("Не соответствует")

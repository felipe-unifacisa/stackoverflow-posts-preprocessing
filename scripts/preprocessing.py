import re

def preprocess_text(text):
    # Remove leading and trailing whitespace
    text.strip()

    # Convert all words to lowercase
    text = text.lower()

    # Remove all tags except tags that could imply information, such as code tags and tags that represent emphasis
    text = re.sub(r"<(?!code|\/code)(?!b|\/b)(?!i|\/i)(?!strong|\/strong)[^>]*>", "", text)

    # Replace new line, tab and carriage return with space
    text = re.sub(r"\n|\t|\r", " ", text)

    # Remove extra spaces
    text = re.sub(r" {2,}", " ", text)

    return text
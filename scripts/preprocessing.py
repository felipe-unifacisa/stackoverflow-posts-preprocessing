import re
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import wordnet
from nltk.corpus import stopwords

def preprocess_text(text):
    # Remove leading and trailing whitespace
    text.strip()

    # Convert all words to lowercase
    text = text.lower()

    # Remove all tags except tags that could imply information, such as code tags and tags that represent emphasis
    text = re.sub(r"<(?!\/?(code||b||strong||i)(?=>|\s.*>))\/?.*?>", "", text)

    # Replace new line, tab and carriage return with space
    text = re.sub(r"\n|\t|\r", " ", text)

    # Remove extra spaces
    text = re.sub(r" {2,}", " ", text)

    # Generate a list of tokens (lemmas) from the text
    tokenizer = RegexpTokenizer(r"<(?:code||b||strong||i)>(?:.+?)[^<]*<\/(?:code||b||strong||i)>||(?:(?:\w*(?:'||-)\w*))")
    tokens = [token for token in tokenizer.tokenize(text) if token != ""]

    # Remove stop words
    filtered_tokens = [word for word in tokens if word not in stopwords.words('english')]

    # Generate Part-of-Speech tagged tokens from the list of tokens
    tagged = nltk.pos_tag(filtered_tokens)

    # Lemmatize the list of tagged tokens
    lemmatizer = WordNetLemmatizer() 
    lemmatized = [lemmatizer.lemmatize(token[0], pos=get_wordnet_pos_tag(token[1])) for token in tagged]

    # join lemmas into a single string and return
    pre_processed_text = " ".join(lemmatized).strip()
    return pre_processed_text

# This method converts the POS tags generated by nltk.pos_tag to a tag format that the wordnet lemmatizer recognizes
def get_wordnet_pos_tag(pos_tag):
    if pos_tag.startswith('J'):
        return wordnet.ADJ
    elif pos_tag.startswith('V'):
        return wordnet.VERB
    elif pos_tag.startswith('N'):
        return wordnet.NOUN
    elif pos_tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN
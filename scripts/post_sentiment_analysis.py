from nltk.sentiment.vader import SentimentIntensityAnalyzer
from timeit import default_timer as timer
import xmltodict

# Returns a string representing the compound score interval
def get_rating(compound_score):
    if compound_score >= 0.5:
        return 'positive'
    elif compound_score  > -0.5 and compound_score < 0.5:
        return 'neutral'
    elif compound_score <= -0.5:
        return 'negative'

# Uses NLTK's VADER sentiment analysis function on the body of all questions of a given file
def sentiment_analysis(input_path, year, filtertag1 = None, filtertag2 = None):
    print(f"Starting sentiment analysis for {year} posts. This might take a while...")
    start = timer()
    interval = timer()
    processed_questions = 0

    sia = SentimentIntensityAnalyzer()

    year_scores = {
            filtertag1: {'positive': [], 'neutral': [], 'negative': []}, 
            filtertag2: {'positive': [], 'neutral': [], 'negative': []}
    }

    with open(input_path, encoding="utf8") as questions_and_answers:
        for line in questions_and_answers:
            if line.strip().startswith("<row"):
                post_dict = xmltodict.parse(line, xml_attribs=True)
                if post_dict['row']['@PostTypeId'] == '1':
                    if f"<{filtertag1}>" in post_dict['row']['@Tags']:
                        score = sia.polarity_scores(post_dict['row']['@Body'])
                        year_scores[filtertag1][get_rating(score['compound'])].append((post_dict['row']['@Id'], score))

                    elif f"<{filtertag2}>" in post_dict['row']['@Tags']:
                        score = sia.polarity_scores(post_dict['row']['@Body'])
                        year_scores[filtertag1][get_rating(score['compound'])].append((post_dict['row']['@Id'], score))

                processed_questions += 1
                if timer() - interval > 300:
                    print(f"# of processed posts: {processed_questions}")
                    interval = timer()

    print(f"Sentiment Analysis for {year} posts finished in {round(timer() - start, 2)} seconds.")

    return year_scores
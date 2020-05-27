import nltk
from nltk.probability import FreqDist
import json
from timeit import default_timer as timer
import re


def generate_freqdist(input_json_path, filtertag1 = None, filtertag2 = None):
    freq_per_year = {}
    current_year = ""
    year_wordbag = {filtertag1: "", filtertag2: ""}

    print(f"Starting generating frequency distribution data. This might take a while...")
    start = timer()

    with open(input_json_path, encoding="utf8") as questions_and_answers:
        for line in questions_and_answers:
            if line.strip().startswith("{"):
                question = json.loads(line.replace(',\n', ''))

                year = question['creationDate'][0:4]

                if year != current_year:
                    if current_year != '':
                        freq_per_year[current_year] = {filtertag1: FreqDist(), filtertag2: FreqDist()}

                    for word in nltk.tokenize.word_tokenize(year_wordbag[filtertag1]):
                        freq_per_year[current_year][filtertag1][word] += 1
                    
                    for word in nltk.tokenize.word_tokenize(year_wordbag[filtertag2]):
                        freq_per_year[current_year][filtertag2][word] += 1

                    year_wordbag[filtertag1] = ""
                    year_wordbag[filtertag2] = ""
                    current_year = year
                
                if f"<{filtertag1}>" in question['tags']:
                    year_wordbag[filtertag1] = year_wordbag[filtertag1] + " " + re.sub(r"(<code>.*<\/code>)", "", question['title'])
                    year_wordbag[filtertag1] = year_wordbag[filtertag1] + " " + re.sub(r"(<code>.*<\/code>)", "", question['body'])
                    for answer in question['answers']:
                        year_wordbag[filtertag1] = year_wordbag[filtertag1] + " " + re.sub(r"(<code>.*<\/code>)", "", answer['body'])

                if f"<{filtertag2}>" in question['tags']:
                    year_wordbag[filtertag2] = year_wordbag[filtertag2] + " " + re.sub(r"(<code>.*<\/code>)", "", question['title'])
                    year_wordbag[filtertag2] = year_wordbag[filtertag2] + " " + re.sub(r"(<code>.*<\/code>)", "", question['body'])
                    for answer in question['answers']:
                        year_wordbag[filtertag2]= year_wordbag[filtertag2] + " " + re.sub(r"(<code>.*<\/code>)", "", answer['body'])

            elif line.strip().startswith("]"):
                freq_per_year[current_year] = {filtertag1: FreqDist(), filtertag2: FreqDist()}

                for word in nltk.tokenize.word_tokenize(year_wordbag[filtertag1]):
                    freq_per_year[current_year][filtertag1][word] += 1

                freq_per_year[current_year][filtertag1] = sorted(freq_per_year[current_year][filtertag1].items(), key=lambda x: x[1], reverse=True)
                
                for word in nltk.tokenize.word_tokenize(year_wordbag[filtertag2]):
                    freq_per_year[current_year][filtertag2][word] += 1

                freq_per_year[current_year][filtertag2] = sorted(freq_per_year[current_year][filtertag2].items(), key=lambda x: x[1], reverse=True)

    print(f"Frequency distribution generation finished in {round(timer() - start, 2)} seconds.")

    return freq_per_year
                    
                

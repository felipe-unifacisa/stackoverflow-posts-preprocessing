import json
from timeit import default_timer as timer

# Represents the Q&A statistics for a given technology.
class Stats:
    def __init__(self):
        self.num_questions = 0
        self.num_answers = 0
        self.num_questions_with_code = 0
        self.unanswered_questions = 0
        self.answer_count = {}
        self.score_count = {}

# Takes a pre-processed Q&A JSON file and generates the Q&A statistics for the chosen question tags.
# Due to the file size, it has to be accessed line by line.
def generate_stats(input_json_path, filtertag1 = None, filtertag2 = None):
    stats_per_year = {}

    print(f"Starting generating Q&A stats. This might take a while...")
    start = timer()

    with open(input_json_path, encoding="utf8") as questions_and_answers:
        for line in questions_and_answers:
            if line.strip().startswith("{"):
                question = json.loads(line.replace(',\n', ''))

                year = question['creationDate'][0:4]

                if year not in stats_per_year.keys():
                    stats_per_year[year] = { filtertag1: Stats(), filtertag2: Stats()}                   

                if f"<{filtertag1}>" in question['tags']:
                    calculate_tag_stats(stats_per_year[year][filtertag1], question) 

                if f"<{filtertag2}>" in question['tags']:
                    calculate_tag_stats(stats_per_year[year][filtertag2], question)

    print(f"Stats generation finished in {round(timer() - start, 2)} seconds.")

    return stats_per_year

# Takes a Stats object reference and increments its values based on a question's data.
def calculate_tag_stats(filtertag_stats, question):
    filtertag_stats.num_questions += 1
    
    if "<code>" in question['body']:
        filtertag_stats.num_questions_with_code += 1

    q_answers = len(question['answers'])
    if(q_answers > 0):
        filtertag_stats.num_answers += q_answers
        try: 
            filtertag_stats.answer_count[q_answers] += 1
        except KeyError:
            filtertag_stats.answer_count[q_answers] = 0
            filtertag_stats.answer_count[q_answers] += 1

    else:
        filtertag_stats.unanswered_questions += 1
                            
    try: 
        filtertag_stats.score_count[question['score']] += 1
    except KeyError:
        filtertag_stats.score_count[question['score']] = 0
        filtertag_stats.score_count[question['score']] += 1

    for answer in question['answers']:
        try: 
            filtertag_stats.score_count[answer['score']] += 1
        except KeyError:
            filtertag_stats.score_count[answer['score']] = 0
            filtertag_stats.score_count[answer['score']] += 1    
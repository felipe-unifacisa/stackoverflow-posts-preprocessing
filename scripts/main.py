from xml_to_json import process_posts
from preprocessing import preprocess_text
from post_stats import generate_stats
from post_freqdist import generate_freqdist
from post_splitter import split_posts
from post_splitter_nineteen import split_posts_nineteen
from post_sentiment_analysis import sentiment_analysis
import json
import multiprocessing

def save_freqdist_to_file(input_path, output_path):
    freq_per_year = generate_freqdist(input_path, filtertag1="c#", filtertag2="java")

    with open(output_path, "w") as output_file:
        json.dump(list(freq_per_year.values())[0], output_file)

def save_sentiment_analysis_to_file(input_path, output_path, year):
    sentiment_analysis_result = sentiment_analysis(input_path, year, filtertag1="c#", filtertag2="java")

    with open(output_path, "w") as output_file:
        json.dump(sentiment_analysis_result, output_file)

def save_post_stats_to_file(input_path, output_path):
    stats_per_year = generate_stats(input_path, filtertag1="c#", filtertag2="java")
    
    data = {
        "c#": list(stats_per_year.values())[0]["c#"].__dict__,
        "java": list(stats_per_year.values())[0]["java"].__dict__
    }

    with open(output_path, "w") as output_file:
        json.dump(data, output_file)

def main():
    # Example usage: Saving sentiment analysis results to a json file
     
    input_paths = {
        '2015': "Your/Posts Data/Path/Posts2015.xml",
        '2016': "Your/Posts Data/Path/Posts2016.xml",
        '2017': "Your/Posts Data/Path/Posts2017.xml",
        '2018': "Your/Posts Data/Path/Posts2018.xml",
        '2019': "Your/Posts Data/Path/Posts2019.xml"
    }

    output_paths = {
        '2015': "Your/Output Data/Path/SentimentAnalysis2015.json",
        '2016': "Your/Output Data/Path/SentimentAnalysis2016.json",
        '2017': "Your/Output Data/Path/SentimentAnalysis2017.json",
        '2018': "Your/Output Data/Path/SentimentAnalysis2018.json",
        '2019': "Your/Output Data/Path/SentimentAnalysis2019.json"
    }

    sentiment_analysis2015 = multiprocessing.Process(target=save_sentiment_analysis_to_file, args=(input_paths['2015'], output_paths['2015'], '2015'))
    sentiment_analysis2016 = multiprocessing.Process(target=save_sentiment_analysis_to_file, args=(input_paths['2016'], output_paths['2016'], '2016'))
    sentiment_analysis2017 = multiprocessing.Process(target=save_sentiment_analysis_to_file, args=(input_paths['2017'], output_paths['2017'], '2017'))
    sentiment_analysis2018 = multiprocessing.Process(target=save_sentiment_analysis_to_file, args=(input_paths['2018'], output_paths['2018'], '2018'))
    sentiment_analysis2019 = multiprocessing.Process(target=save_sentiment_analysis_to_file, args=(input_paths['2019'], output_paths['2019'], '2019'))

    sentiment_analysis2015.start()
    sentiment_analysis2016.start()
    sentiment_analysis2017.start()
    sentiment_analysis2018.start()
    sentiment_analysis2019.start()

    sentiment_analysis2015.join()
    sentiment_analysis2016.join()
    sentiment_analysis2017.join()
    sentiment_analysis2018.join()
    sentiment_analysis2019.join()

    print('end')

if __name__=="__main__": 
    main()
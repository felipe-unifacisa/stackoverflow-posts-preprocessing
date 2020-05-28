# stackoverflow-posts-preprocessing
Scripts for pre-processing Stack Overflow Posts.xml from https://archive.org/details/stackexchange

# Installing Dependencies
The scripts depend on **nltk** for NLP tools and **xmltodict** to process the xml files. To install the dependencies, run the command:
```
pip install nltk xmltodict
```

After NLTK is installed, the nltk sub-packages must be downloaded. Start python on the terminal and run:
```python
>>> import nltk
>>> nltk.download()
```
A window should open with the available packages. Install the following packages:

- wordnet
- words
- punkt
- stopwords
- vader-lexicon
- averaged-perceptron-tagger
- maxent-ne-chunker

# File Splitting
Because the Stack Overflow Posts.xml file holds over 70GB of data, it's advised to export only the posts you desire to analyze before running any sort of post-processing. The `post_splitter.py` script does that, extracting posts with a creation date matching the desired years, and saving all posts of each year to an individual xml file.

# Pre-Processing
The `xml_to_json.py` script is responsible for taking the xml files, generating a dictionary containing all the questions with the answers for each question as an array property of the question object, and saving it to a JSON file. This is done because JSON is a better file format than XML to load as a python object. For the sake of optimization, the `preprocessing.py` script is called when the dictionary is being generated, so the posts title and body can be pre-processed while the dictionary is being generated.

# Processing
The following scripts are used for processing the posts:

- `post_stats.py` - receives a pre-processed posts file and returns an object with statistical data.
- `post_freqdist.py` - receives a pre-processed posts file and returns an object with frequency distribution data.
- `post_sentiment_analysis.py` - receives a pre-processed posts file and returns an object with sentiment analysis data.

It is advised to make use of python multiprocessing to process all posts files simultaneously, and to save the processing results to a json file. The `main.py` script has an example.

import json
import xmltodict
from pathlib import Path
from timeit import default_timer as timer


# This function takes a Posts.xml file from the StackExchange data dump (https://archive.org/details/stackexchange) and generates a json file
# containing a list of all the questions that match the given filter tatgs and a list of answers as a new property for each question. 
# Each question and answer's title (if available) and body go through a preprocessor passed as a parameter to the function.

def process_posts(posts_xml_path, output_json_path, preprocessor, year = 2008, filtertag1 = None, filtertag2 = None):
    start = timer()
    interval = timer()
    questions = {}
    processed_lines = 0
    with open(posts_xml_path, encoding="utf8") as post_xml:
        print(f"Starting Pre-processing Posts.xml file for year {year}. This might take a while...")
        
        for line in post_xml:
            # in the xml file, each post is a <row> tag with the properties as xml attributes
            if line.strip().startswith("<row"):
                post_dict = xmltodict.parse(line, xml_attribs=True)

                post = {
                    'postId': post_dict['row']['@Id'],
                    'postTypeId': post_dict['row']['@PostTypeId'],                    
                    'creationDate': post_dict['row']['@CreationDate'],
                    'score': post_dict['row']['@Score'] if '@Score' in post_dict['row'] else "",
                    'commentCount': post_dict['row']['@CommentCount'] if '@CommentCount' in post_dict['row'] else ""
                }
                # post is a question and has one of the chosen technology tags in its tag list
                if post_dict['row']['@PostTypeId'] == '1' and (f"<{filtertag1}>" in post_dict['row']['@Tags'] or f"<{filtertag2}>" in post_dict['row']['@Tags']):
                    post['title'] = preprocessor(post_dict['row']['@Title']) if '@Title' in post_dict['row'] else ""
                    post['body'] = preprocessor(post_dict['row']['@Body'])
                    post['tags'] = post_dict['row']['@Tags'] if '@Tags' in post_dict['row'] else ""
                    post['acceptedAnswerId'] = post_dict['row']['@AcceptedAnswerId'] if '@AcceptedAnswerId' in post_dict['row'] else ""
                    post['answerCount'] = post_dict['row']['@AnswerCount'] if '@AnswerCount' in post_dict['row'] else ""
                    post['favoriteCount'] = post_dict['row']['@FavoriteCount'] if '@FavoriteCount' in post_dict['row'] else ""
                    post['viewCount'] = post_dict['row']['@ViewCount'] if '@ViewCount' in post_dict['row'] else ""
                    post['answers'] = []
                    questions[post['postId']] = post
                # post is an answer
                elif post_dict['row']['@PostTypeId'] == "2":
                    post['parentId'] = post_dict['row']['@ParentId'] if '@ParentId' in post_dict['row'] else ""                    
                    if post['parentId'] in list(questions.keys()):
                        post['body'] = preprocessor(post_dict['row']['@Body'])
                        questions.get(post['parentId'])['answers'].append(post)

                processed_lines = processed_lines + 1

                if timer() - interval > 300:
                    print(f"# of processed posts for year {year}: {processed_lines}")
                    interval = timer()

    print(f"Pre-processing finished in {round(timer() - start, 2)} seconds.")

    # Write the list of questions with answers to the JSON output file
    with open(output_json_path, "w") as output_file:
        print("Generating questions and answers JSON file...")
        output_file.write("[\n")
        for question in list(questions.values()):
            json.dump(question, output_file)
            questions.pop(question['postId'])
            if len(questions) > 0:
                output_file.write(",\n")
        output_file.write("\n]")

    print(f"{output_json_path} file created.")

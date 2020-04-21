import json
import xmltodict
from pathlib import Path

# This function takes a Posts.xml file from the StackExchange data dump (https://archive.org/details/stackexchange) and generates a json file
# containing a list of all the questions and a list of answers as a new property for each question. Each question and answer's title (if available)
# and body go through a preprocessor passed as a parameter to the function.

def process_posts(posts_xml_path, output_json_path, preprocessor):

    questions = []
    answers = []

    with open(posts_xml_path, encoding="utf8") as post_xml:
        for line in post_xml:
            # in the xml file, each post is a <row> tag with the properties as xml attributes
            if line.strip().startswith("<row"):
                post_dict = xmltodict.parse(line, xml_attribs=True)
                post = {
                    'postId': post_dict['row']['@Id'],
                    'postTypeId': post_dict['row']['@PostTypeId'],
                    'body': preprocessor(post_dict['row']['@Body']),
                    'creationDate': post_dict['row']['@CreationDate'],
                    'score': post_dict['row']['@Score'] if '@Score' in post_dict['row'] else "",
                    'commentCount': post_dict['row']['@CommentCount'] if '@CommentCount' in post_dict['row'] else ""
                }
                if post_dict['row']['@PostTypeId'] == '1':  # post is a question
                    post['title'] = preprocessor(post_dict['row']['@Title']) if '@Title' in post_dict['row'] else ""
                    post['tags'] = post_dict['row']['@Tags'] if '@Tags' in post_dict['row'] else ""
                    post['acceptedAnswerId'] = post_dict['row']['@AcceptedAnswerId'] if '@AcceptedAnswerId' in post_dict['row'] else ""
                    post['answerCount'] = post_dict['row']['@AnswerCount'] if '@AnswerCount' in post_dict['row'] else ""
                    post['favoriteCount'] = post_dict['row']['@FavoriteCount'] if '@FavoriteCount' in post_dict['row'] else ""
                    post['viewCount'] = post_dict['row']['@ViewCount'] if '@ViewCount' in post_dict['row'] else ""
                    questions.append(post)
                elif post_dict['row']['@PostTypeId'] == "2":  # post is an answer
                    post['parentId'] = post_dict['row']['@ParentId'] if '@ParentId' in post_dict['row'] else ""
                    answers.append(post)
                print(f"{post['postId']}")

    # Create a list of answers for each question
    for question in questions:
        print(f"Answers left: {len(answers)}. Getting answers for question Id {question['postId']}...")
        question['answers'] = []
        for answer in answers[:]:
            if question['postId'] == answer['parentId']:
                question['answers'].append(answer)
                answers.remove(answer)

    # Write the list of questions with answers to the JSON output file
    with open(output_json_path, "w") as output_file:
        print("Generating questions and answers JSON file...")
        output_file.write("[\n")
        for question in questions[:]:
            json.dump(question, output_file)
            questions.remove(question)
            if len(questions) > 0:
                output_file.write(",\n")
        output_file.write("\n]")

    print(f"{output_json_path} file created.")

import json
import xmltodict
from pathlib import Path
from timeit import default_timer as timer

# Splits posts in different files by their year, for supporting multiprocessing
def split_posts(posts_xml_path, output_xml_paths, filtertag1 = None, filtertag2 = None):
    print(f"Starting file splitting by year...")
    start = timer()
    interval = timer()
    processed_lines = 0
    question_ids = {'2015': [], '2016': [], '2017': [], '2018': []}
    with open(posts_xml_path, encoding="utf8") as post_xml:
        with open(output_xml_paths['2015'], "w", encoding="utf-8") as posts_2015_xml:
            with open(output_xml_paths['2016'], "w", encoding="utf-8") as posts_2016_xml:
                with open(output_xml_paths['2017'], "w", encoding="utf-8") as posts_2017_xml:
                    with open(output_xml_paths['2018'], "w", encoding="utf-8") as posts_2018_xml:
                        for line in post_xml:
                            # in the xml file, each post is a <row> tag with the properties as xml attributes
                            if line.strip().startswith("<row"):
                                post_dict = xmltodict.parse(line, xml_attribs=True)
                                year = post_dict['row']['@CreationDate'][0:4]
                                post_type = post_dict['row']['@PostTypeId']
                                valid_line = False

                                if year in output_xml_paths.keys():
                                    if post_type == "1" and (f"<{filtertag1}>" in post_dict['row']['@Tags'] or f"<{filtertag2}>" in post_dict['row']['@Tags']):
                                        question_ids[year].append(post_dict['row']['@Id'])
                                        valid_line = True

                                    elif post_type == "2" and post_dict['row']['@ParentId'] in question_ids[year]:
                                        valid_line = True

                                if valid_line:
                                    if year == '2015':
                                        posts_2015_xml.write(line)
                                    elif year == '2016':
                                        posts_2016_xml.write(line)
                                    elif year == '2017':
                                        posts_2017_xml.write(line)
                                    elif year == '2018':
                                        posts_2018_xml.write(line)
                                    
                                processed_lines = processed_lines + 1

                                if timer() - interval > 300:
                                    print(f"# of processed posts: {processed_lines}")
                                    interval = timer()

    print(f"File splitting by year finished in {round(timer() - start, 2)} seconds.")
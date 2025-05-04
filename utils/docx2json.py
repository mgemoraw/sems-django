from os import write
import os
from docx2python import docx2python
import re
import json
import sys 


def create_working_directory(docx_path):
    pass


def extract_questions(docx_path):
    questions = []

    # set working folder
    folder = input("Enter file folder: ")
    if not os.path.exists(folder):
        os.makedirs(folder)
        print(f"Folder '{folder}' created successfully.")
    else:
        print(f"Folder '{folder}' already exists.")

    # read docx document
    document = docx2python(docx_path)
    # print(dir(document))
    # save images to current directory
    with docx2python(docx_path) as docx_content:
        # os.makedirs(f'{folder}/images/')
        docx_content.save_images(f"./{folder}/images/")

    # get document body
    # print(document.body[2])
    module_name = None
    course_name = None
    department = None
    course_code = None
    university = None 
    faculty = None
    exam_year = None
    qno = 0
    # print(document.body[0][0][0])
    # print(document.body[1][0][0])
    # print(document.body[2][0][0])
    # print(dir(document))
    # print(document.)

    print("processing conversion....")
    for section in document.body:
        # print("----section---")
        for page in section:
            # print('-----page----')
            for paragraphs in page:
                question = {}
                options = []

                # print("--------paragraph------")
                # print(paragraphs)
                for line in paragraphs:
                    # print(line)
                    line = line.strip()
                    try:
                        if 'answer key' in line.strip().lower():
                            break

                        if not line or len(line.strip()) < 2 :
                            continue

                        # check if the line is a numbered bullet
                        if re.match(r'^\d+[.)]', line):
                            # print("question:", line)
                            pos = re.search(r'^\d+[.)]', line)
                            end_pos = pos.end()
                            # print(pos)
                            question = {'qno': qno+1, 'department': department, 'module': module_name, 'course': course_name, 'content': line.strip()[end_pos:], 'options': [], 'image': None, 'answer': None}
                            # # options = []
                            questions.append(question)
                            qno += 1
                            # continue

                        elif re.match(r'^[A-Za-z][.)]', line):
                            # if questions[qno-1].get('options') is None:
                            #     questions[qno-1]['options'] = []
                            image_name = None
                            if ('image' in line):
                                pos1 = line.find('/')
                                pos2 = line.find('.')
                                image_name = line[pos1+1:pos2+2]

                            pos = re.search(r'^[A-Za-z][.)]', line)
                            end_pos = pos.end()
                            option_label = line[0]
                            option_content = line[end_pos:].strip()

                            option = {'label': option_label, 'content': option_content, 'image': image_name}
                            questions[qno-1]['options'].append(option)
                            
                            # continue

                        elif "[IMAGE" in line.upper():
                            # question['image'].append(line)
                            pos1 = line.find('/')
                            pos2 = line.find('.')
                            image_name = line[pos1+1:pos2+2]
                            questions[qno-1]['image'] = image_name
                            # print(f"Image placeholder: {line}")
                            # continue

                        elif line.lower().startswith('answer'):
                            pos = line.find(':')
                            # answer = line[pos+1]
                            answer = line.strip().split(':')
                            if (len(answer) > 1):
                                questions[qno-1]['answer'] = answer[1]
                                # print(line)
                        
                        # Extract metadata (e.g., course name, module name)
                        elif line.lower().startswith('course name'):
                            course_name = line.split(':', 1)[1].strip()
                            # questions[qno-1]['course'] = course_name
                            # print(f"Course Name: {course_name}")

                        elif line.lower().startswith('module name'):
                            module_name = line.split(':', 1)[1].strip()
                            # questions[qno-1]['module'] = module_name
                            # print(f"Module Name: {module_name}")
                        elif line.lower().startswith('department'):
                            department = line.split(':', 1)[1].strip()
                            # print(f"Department: {department}")
                            # questions[qno-1]['department'] = department

                        elif line.lower().startswith('course code'):
                            if (len(line.split(':', 1)) > 0):
                                course_code = line.split(':', 1)[1].strip()

                            # print(f"Course Code: {course_code}")
                            # questions[qno-1]['course_code'] = course_code
                            
                        elif line.lower().startswith('university'):
                            pass
                            # university = line.split(':', 1)[1].strip()
                            # print(f"University: {university}")

                        elif line.lower().startswith('faculty'):
                            faculty = line
                            # faculty = line.split(':', 1)[1].strip()
                            # print(f"Faculty: {faculty}")
                        elif line.lower().startswith('exam year'):
                            pass
                            # exam_year = line.split(':', 1)[1].strip()
                            # print(f"Exam Year: {exam_year}")
                    
                        else:
                            print("TEXT, {}".format(qno), line)
                            
                    except Exception as e:
                        print(e)
                        raise e
  
    # saving questions.json
    with open(os.path.join(folder, 'questions.json'), 'w') as file:
        print("Dumping data to json format...")
        json.dump(questions, file)

  

def extract_bullets(docx_path):
    # Extract text from the .docx file
    doc_content = docx2python(docx_path)

    # print(doc_content.text.split())
    # for line in doc_content.body:
    #    if re.match(r"^\d+\)", line):
    #        print(line)
    # print(doc_content.body)
    
    for name, image in doc_content.images.items():
        with open(name, 'wb') as image_destination:
            image_destination.write(image)


    # Flatten text from the extracted structure
    text = "\n".join(["\n".join(paragraph) for section in doc_content.body for table in section for row in table for paragraph in row])

    
    # Define regex patterns for numbered and lettered bullets
    numbered_bullet_pattern = r"^\d+\)"   # Matches "1)", "2)", etc.
    lettered_bullet_pattern = r"^[A-Z]\)"  # Matches "A)", "B)", etc.

    numbered_bullets = []
    lettered_bullets = []

    # Iterate through each line and classify bullets
    for line in text.split("\n"):
        line = line.strip()  # Remove unnecessary spaces
        if re.match(numbered_bullet_pattern, line):
            numbered_bullets.append(line)
        elif re.match(lettered_bullet_pattern, line):
            lettered_bullets.append(line)

    return numbered_bullets, lettered_bullets


if __name__=='__main__':
    # docx_path = "sample.docx"

    if len(sys.argv) != 2:
        print("You have to enter name of docx file ")
        sys.exit(0)
    else:
        docx_path = f"./{sys.argv[1]}.docx"

        # call extract questions function
        extract_questions(docx_path=docx_path)

        print("json file saved to {}.json".format(sys.argv[1]))


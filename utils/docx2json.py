from os import write
from docx2python import docx2python
import re
import json

def extract_questions(docx_path):
    questions = {}

    # read docx document
    document = docx2python(docx_path)
    print(dir(document))
    # save images to current directory
    with docx2python(docx_path) as docx_content:
        docx_content.save_images("./")

    # get document body
    # print(document.body[2])
    for section in document.body:
        for page in section:
            for paragraphs in page:
                for line in paragraphs:
                    if not line:
                        continue

                    # check if the line is a numbered bullet
                    if re.match(r'^\d+\)', line):
                        print("Question:", line)
                    
                    elif re.match(r'^[A-Za-z]\)', line):
                        print("Choice:", line)
                    elif "[IMAGE" in line.upper():
                        print("Image placeholder", line)

                    elif isinstance(line, list) and line and isinstance(paragraphs[0],list):
                        table = []
                        row_text = [' '.join(cell).strip() for cell in row if isinstance(cell, list)]
                        print("Table: ", row_text)
                    else:
                        print("Text: ", line)
                
    # extract tables
    print("--------Tables------")
    print(hasattr(document, 'tables'))

    # for table in document.table:
        # print("Table: ")
        # for row in table:
        #     row_text = [' '.join(cell).strip() for cell in row]
        #     print("\tRow: ", row_text)


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
    docx_path = "sample.docx"


    # call extract questions function
    extract_questions(docx_path=docx_path)


    # Example usage
    # document = docx2python('sample.docx')

    docx_file = "sample.docx"  # Replace with your actual .docx file path
    # numbered, lettered = extract_bullets(docx_file)

    # print("Numbered Bullets:", numbered)
    # print("Lettered Bullets:", lettered)



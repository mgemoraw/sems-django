from os import write
from docx2python import docx2python
import re

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

# Example usage
# document = docx2python('sample.docx')

docx_file = "sample.docx"  # Replace with your actual .docx file path
numbered, lettered = extract_bullets(docx_file)

print("Numbered Bullets:", numbered)
print("Lettered Bullets:", lettered)

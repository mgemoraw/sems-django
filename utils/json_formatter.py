"""
this script changes previous .json qustion format to a more suitable json string format
>>> previous format 
{
    "question": str,
    "A": str,
    "B": str,
    "C": str,
    "D": str,
    "E": str,
    "F": str,
    "answer": str,
    "image": str,
    "course": str,
    "module": str,
}
>>> latest format
{
    "id": number,
    "department_idfk": number,
    "department_name": str,
    "course_code": str,
    "course_name": str,
    "content": str,
    "options": [
        {"label": str, "content": str, "image": str},
        {"label": str, "content": str, "image": str},
        {"label": str, "content": str, "image": str},
        {"label": str, "content": str, "image": str},
        {"label": str, "content": str, "image": str},
        {"label": str, "content": str, "image": str},
    ]
    "answer": str,
    "image": str,
}
"""

from pydantic import BaseModel
from typing import Optional
import json
import os
import sys 
# from config import BASE_DIR


class PreviousQuestion(BaseModel):
    question:str
    A: str
    B: str
    C: str
    D: str
    E: str
    F: str
    answer: str
    image: str
    course: str
    module: str 

    class Config:
        from_attributes = True


class AnswerOption(BaseModel):
    label: str | None = None
    image: str | None = None
    content: str | None = None


class LatestQuestion(BaseModel):
    department_id: Optional[int] = None
    course_code: Optional[str] = None
    department_name: Optional[str] = None
    course_name: Optional[str] = None
    content: Optional[str] = None
    image: Optional[str] = None
    options: list[AnswerOption] = None
    answer: str = None
    year:int = 2025

class Department(BaseModel):
    id: int
    name: str


def convert(file_path, department: Department):
    if file_path is None:
        raise Exception("Input Files Error!")
    
    # open storage list for questions
    questions = []
    
    with open(file_path, 'r', encoding="utf-8") as file:
        jfile = json.loads(file.read())
        

        # convert file
        for q in jfile:
            # assign options
            options = [
                AnswerOption(label='A', content=q.get('A'), image=None).model_dump(), 
                AnswerOption(label='B', content=q.get('B'), image=None).model_dump(),
                AnswerOption(label='C', content=q.get('C'), image=None).model_dump(),
                AnswerOption(label='D', content=q.get('D'), image=None).model_dump(),
                AnswerOption(label='E', content=q.get('E'), image=None).model_dump(),
                AnswerOption(label='F', content=q.get('F'), image=None).model_dump(),
            ]

            # create question object
            question = LatestQuestion(
                department_id = department.id,
                department_name = department.name,
                course_name = q.get("course").encode("utf-8"),
                course_code = None,
                content = q.get("question").encode("utf-8"),
                options = options,
                image=q.get("image").encode("utf-8"),
                answer=q.get("answer").encode("utf-8"),
                year=2025
            )

            # add question as json dictionary to the storage list
            questions.append(question.model_dump())


    # save questions as a json file
    save_to = file_path.split("/")[-1]
    write_to_json(questions, save_to)


    # return list of questions ready to be wrritten to json file format
    return (questions)


def write_to_json(file:list, save_to:str):

    with open(save_to, "w") as json_file:
        json.dump(file, json_file, indent=4) 

    print(f"File saved to {save_to}")



if __name__ == "__main__":
    
    if len(sys.argv) != 2:
        print("You have to enter name of docx file ")
        sys.exit(0)
    else:
        file_path = f"./{sys.argv[1]}.json"

        # call extract questions function
        # extract_questions(docx_path=docx_path)

        # print("json file saved to {}.json".format(sys.argv[1]))


        # set working folder
        folder = input("Enter ouptput folder: ")
        if not os.path.exists(folder):
            os.makedirs(folder)
            print(f"Folder '{folder}' created successfully.")
        else:
            print(f"Folder '{folder}' already exists.")
        
        # json_files = os.listdir(BASE_DIR / "assets")


        # input departent name
        dep_name = input("Enter Department Name: ")
        department = Department(id=0, name=dep_name)

        save_to = f"{folder}/questions.json"
        file_path = f'tadele-data-2025/{sys.argv[1]}.json'

        questions = convert(file_path, department=department)
        write_to_json(questions, save_to)

        # departments = [
        #     {"id": 1, "name": "Civil Engineering"},
        #     {"id": 2, "name": "Water Resources and Irrigation Engineering"},
        #     {"id": 3, "name": "Mechanical Engineering"},
        #     {"id": 4, "name": "Electrical Engineering"},
        #     {"id": 5, "name": "Industrial Engineering"},
        #     {"id": 6, "name": "Automotive Engineering"},
        #     {"id": 7, "name": "Hydraulic Engineering"},
        # ]


        # for file in json_files:
        #     if file.endswith(".json"):
        #         # set department name and id 
        #         department = Department(id=0, name="Hydrawulic and Water Resources Engineering")
        
        #         file_path = "assets/HydraulicEngineering.json"
        #         save_to = os.path.join("./", file_path.split("/")[1])

        #         questions = convert(os.path.join(BASE_DIR, file_path), department=department)
        #         write_to_json(questions, save_to)

import os
import json 

question_path = "ce/questions.json"
answers_path = "ce/answers.txt"

def map_answers(questions, answers):
    json_file =None
    a_file = None 
    with open(questions, 'r', encoding='utf-8') as jfile:
        json_file = json.load(jfile)

    with open(answers, 'r', encoding='utf-8') as afile:
        a_file = afile.readlines()

    # for q, a in zip(json_file, a_file):
        # print(q.get('qno'), '<--->', a)

    counter = 0
    for q in json_file:  
        if q.get('content') != '' :
            # print(q.get('qno'), '<--->', a_file[counter])
            # print(q.get('qno'))
            answer = a_file[counter].split()
            if len(answer) > 1:
                q['answer'] = answer[1]
            counter += 1
    # print(counter)   
    with open('ce/chemical_engineering.json', 'w', encoding='utf-8') as file:
        json.dump(json_file, file)  



map_answers(question_path, answers_path)
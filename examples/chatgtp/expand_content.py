import os
import openai
import sys
import json
import re

sys.path.insert(0, '.')
from pydt3 import DEVONthink3

dtp = DEVONthink3()
def get_api_key():
    result = dtp.search("name==__openai_api_key__")
    if result:
        api_key = result[0].plain_text
    else:
        response = dtp.display_dialog("Please enter your OpenAI API key", "")
        api_key = response["textReturned"]
        dtp.create_record_with({
            "name": "__openai_api_key__",
            "type": "txt",
            "plain text": api_key,
        })
    
    return api_key

    
def expand_content(content) -> str:
    system = '''You are a skillful writer. Replace the angle brackets you see with the content you generated. Outputs should follow the hints in angle brackets. \n 
    
    eg.
    
    User: "Today I watched a famous British movie <<Movie Name>>. Its's written by <<Author>>. It's about <<Plot>>. I like it very much.
    
    AI: {"Movie Name": "The Godfather.", "Author": "Mario Puzo", "Plot": "a mafia family"}
    "'''

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": system,},
            {"role": "user", "content": content,},
            {"role": "assistant", "content": "Okay, I'll gie the answer in json format.",},

        ]
    )
    print(completion.choices)
    response = completion.choices[0]['message']['content']
    results = json.loads(response)
    print("=======", results)
    for key in results:
        content = re.sub(f'<<{key}>>', f'=={results[key]}==', content, count=1)
    return content

def expand_current_record():
    retry_count = 3
    record = dtp.think_windows[0].content_record

    for _ in range(retry_count):
        try:
            record.plain_text = expand_content(record.plain_text)
            break
        except json.decoder.JSONDecodeError as e:
            print(e)
            print("retrying...")
            continue
    
if __name__ == '__main__':
    openai.api_key = get_api_key()
    expand_current_record()
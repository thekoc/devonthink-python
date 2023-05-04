import openai
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

def generate_tags(content) -> list[str]:
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Generate the tags for the following content. Tags should be concise and accurate and no more than 10. output the tags directly seperateted by ',':\n {content}"},
        ]
    )
    response = completion.choices[0]['message']['content']
    print(response)
    return [tag.strip() for tag in response.split(",")]


def add_tags_to_selected_records():
    records = dtp.selected_records
    for recod in records:
        tags = generate_tags(recod.plain_text)
        recod.tags = tags
    
    
if __name__ == '__main__':
    openai.api_key = get_api_key()
    add_tags_to_selected_records()
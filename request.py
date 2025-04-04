import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

authorization_token =  os.getenv('AUTHORIZATION_TOKEN')

selected_model = 'qwen-2.5'

models = {
    'qwen-2.5': 'qwen/qwen2.5-vl-3b-instruct:free',
    'deepseek-r1': 'deepseek/deepseek-r1-zero:free',
    'llama-3.2': 'meta-llama/llama-3.2-1b-instruct:free',
    'gemini-2.5': 'google/gemini-2.5-pro-exp-03-25:free',
}

def get_response(json_response):

    response = ''

    if selected_model in ['qwen-2.5', 'deepseek-r1', 'llama-3.2', 'gemini-2.5']:

        choices = json_response['choices']
        if type(choices) != list or len(choices) == 0:
            response += 'No Response Available'
            return
        first_choice = choices[0]['message']
        for k, v in first_choice.items():
            if k == 'role' or v == None:
                continue
            response += f'\n\n______ {k} ______\n\n'
            response += v
        return response
    
    else:
        json_data = json.dumps(json_response, indent=2)
        print(json_data)
        return ''


def request_model(query):

    response = requests.post(
        url='https://openrouter.ai/api/v1/chat/completions',
        headers={
            'Authorization': f'Bearer {authorization_token}',
            'Content-Type': 'application/json',
        },
        data=json.dumps({
            'model': models[selected_model],
            'messages': [
                {
                    'role': 'user',
                    'content': [
                        {
                            'type': 'text',
                            'text': query
                        },
                    ],
                }
            ],
        })
    )

    print('>>>> Status Code:', response.status_code)
    print(get_response(response.json()))


if __name__ == '__main__':
    
    while True:

        query = input(f'\n\n({selected_model})>>> ').strip()

        if len(query) == 0:
            print('the prompt you provided is empty........')
            continue

        if query[0] == ':':

            if query == ':q':
                break        

            elif query == ':cm':
            
                model_names = list(models.keys())
                for i, v in enumerate(model_names, start=1):
                    print(f'{i}) {v}')
                new_model = input('Enter model number: ')
                try:
                    new_model = int(new_model)
                    if 1 <= new_model <= len(model_names):
                        selected_model = model_names[new_model - 1]
                    else:
                        print('Invalid model number')
                except:
                    print('Invalid model number')
            
            else:

                print('\nInvalid command........')
        
        else:

            try:
                print('fetching ....')
                request_model(query)
            except:
                print('Got error in fetching or formatting response.........')
            

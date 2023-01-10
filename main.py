import os
import openai as ai

ai.organization = 'org-2J6BFEzhs2n3BzlyPa2caWQE'
ai.api_key = os.environ.get('API_KEY')

def query_ai(prompt):
    print('Prompt:',prompt)
    completions = ai.Completion.create(
        engine='text-davinci-003',
        prompt=prompt,
        max_tokens=128,
        n=1,
        stop=None,
        temperature=0.5
    )
    message = completions.choices[0].text
    print('Message: ',message)
    return message


if __name__ == '__main__':
    query_ai('How long would it take to get to Mars?')
    print('It Works!')




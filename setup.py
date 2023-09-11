from __future__ import print_function, unicode_literals
import os
from PyInquirer import style_from_dict, Token, prompt, Separator
from prompt_toolkit.terminal.win32_output import NoConsoleScreenBufferError
from pyfiglet import Figlet

f = Figlet(font='slant')
print(f.renderText('SpaceInvader 2.0'))

print("Welcome to the SpaceInvader 2.0 setup wizard.")
print("Installing dependencies...")
os.system("pip install -r requirements.txt")

style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Pointer: '#673ab7 bold',
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})

questions = [
    {
        'type': 'list',
        'message': 'Select a Scanner',
        'name': 'scanner',
        'choices': [
            {
                'name': 'Qubo Scanner'
            },
            {
                'name': 'Masscan'
            },
        ],
    },
    {
        'type': 'checkbox',
        'message': 'Setup',
        'name': 'features',
        'choices': [
            Separator('Optional Features'),
            {
                'name': 'Discord Bot',
            },
            {
                'name': 'Web UI'
            },
            {
                'name': 'MPI (recommended)',
                'checked': True
            },
            {
                'name': 'Celery',
            }
        ],
        'validate': lambda answer: 'Pls select at least one option.'
        if len(answer) == 0 else True
    },
    {
        'type': 'input',
        'name': 'discord_token',
        'message': 'Enter your Discord Bot Token',
        'when': lambda answers: 'Discord Bot' in answers['features'],
        'validate': lambda answer: 'Pls enter a token.'
        if len(answer) == 0 else True
    },
    {
        'type': 'input',
        'name': 'web_port',
        'message': 'Enter the port you want to host the Web UI on',
        'when': lambda answers: 'Web UI' in answers['features'],
        'default': '8080',
        'validate': lambda answer: 'Pls enter a valid port number.'
        if len(answer) == 0 and answer.isnumeric() else True
    },
    {
        'type': 'input',
        'name': 'rabbitmq_url',
        'message': 'Enter your RabbitMQ URL (celery)',
        'when': lambda answers: 'Celery' in answers['features'],
        'default': 'amqp://guest:guest@localhost:5672/',
    },
    {
        'type': 'input',
        'name': 'mongo_url',
        'message': 'Enter your MongoDB URL',
        'validate': lambda answer: 'Pls enter a URL.'
        if len(answer) == 0 else True
    },
    {
        'type': 'input',
        'name': 'mongo_port',
        'message': 'Enter your MongoDB Port',
        'default': '27017',
        'validate': lambda answer: 'Pls enter a valid port number.'
        if len(answer) == 0 and answer.isnumeric() else True
    },
    {
        'type': 'input',
        'name': 'mongo_db',
        'message': 'Enter your MongoDB Database Name',
        'default': 'spaceinvader',
        'validate': lambda answer: 'Pls enter a database name.'
        if len(answer) == 0 else True
    },
    {
        'type': 'input',
        'name': 'mongo_collection',
        'message': 'Enter your MongoDB Collection Name',
        'default': 'spaceinvader',
        'validate': lambda answer: 'Pls enter a collection name.'
        if len(answer) == 0 else True
    },
    {
        'type': 'input',
        'name': 'mongo_user',
        'message': 'Enter your MongoDB Username',
        'default': 'root',
        'validate': lambda answer: 'Pls enter a username.'
        if len(answer) == 0 else True
    },
    {
        'type': 'password',
        'name': 'mongo_pass',
        'message': 'Enter your MongoDB Password',
        'validate': lambda answer: 'Pls enter a password.'
        if len(answer) == 0 else True
    },
]

try:
    answers = prompt(questions, style=style)
    with open("config.json", "w") as f:
        f.write(str(answers).replace("'", '"'))
except NoConsoleScreenBufferError:
    print("Pls run in cmd or powershell to configure.")
    exit()

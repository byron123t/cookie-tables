from sensitive.objects import openai_key
import openai, json, os, difflib, random, argparse
from time import sleep


class OpenAIChatSession:
    def __init__(self):
        openai.api_key = openai_key
            
    def handle_response(self, user_prompt):
        while True:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                    {'role': 'system', 'content': 'The user will provide a list of attributes for a cookie (name, value). You must respond to the user with either "YES" or "NO". Reply "YES" if the cookie contains personal information. This means the cookie is used for tracking with a unique ID (uid, id, uuid, session_id, GA) which are typically long random strings, contains location information, contains IP address, or contains other PII.'},
                    {'role': 'user', 'content': user_prompt}
                ])
                if response['choices'][0]['finish_reason'] == 'stop':
                    message = response['choices'][0]['message']['content']
                return message
            except openai.error.RateLimitError:
                sleep(5)

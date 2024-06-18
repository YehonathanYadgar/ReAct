
from tools import useWikipedia
import re
import prompts
import main 
from openai import OpenAI
import os
import dotenv
from dotenv import load_dotenv

load_dotenv()

# Create an instance of the OpenAI class
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# function that takes text and returns the function name, and argument thats after the word action
def action_extracter(text):
    action_regex = re.compile(r'^Action: (\w+): (.*)$')
    response_lines = text.split("\n")
    for line in response_lines:
        match = action_regex.search(line)
        if match:
            action = match.group(1)
            action_arg = match.group(2)
            break  

        else:
            print("no actions needed")

    if action and action_arg:
        return action,action_arg
    else:
        print("No matching action found.")

# takes openai conversasion format, and model name and return the output
def generate_text_with_conversation(messages, model = "gpt-4"):
    response = openai_client.chat.completions.create(
        model=model,
        messages=messages
        )
    return response.choices[0].message.content

# list of aviable functions:
available_actions = {
    "useWikipedia": useWikipedia
}

user_prompt = "whats the quran"

messages = [
    {"role": "system", "content": prompts.system_prompt},
    {"role": "user", "content": user_prompt},
]

turn_count = 1
max_turns = 5

while turn_count < max_turns:
    print (f"Loop: {turn_count}")
    print("----------------------")
    turn_count += 1

    response = generate_text_with_conversation(messages, model="gpt-4")

    print(response)

    try:
        function_name,function_param = action_extracter(response)
    except:
         print('finished')    

    if function_name:
            if function_name not in available_actions:
                raise Exception(f"Unknown action: {function_name}: {function_param}")
            print(f" -- running {function_name} {function_param}")
            action_function = available_actions[function_name]
            #call the function
            result = action_function(function_param)
            function_result_message = f"Action_Response: {result}"
            messages.append({"role": "user", "content": function_result_message})
            print(function_result_message)
            function_name = None
            function_param = None
    else:
         break
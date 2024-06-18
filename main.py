
from tools import useWikipedia
import re
import prompts


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

'''
def agent(question):
        
    for i in range(2):
        initial_response = llm.complete(prompts.system_prompt + " " + question)

        # making the initial reponse easyer to deal with
        initial_response = str(initial_response)
        if '*' in initial_response:
            print("removed\n")
            initial_response = initial_response.replace('**' , '')
        print(initial_response)    
            
        # extracting function name and arg
        function_name , function_arg = action_extracter(initial_response)
        function_name = function_name.replace(" ", "")

        # executing extracted functions
        if function_name and function_arg != None:
            function_to_call = globals()[function_name]
            observation  = function_to_call(function_arg)
            print(f"\nObservasion: {observation}")

        initial_response = f
        QUESTION: {question}\n
        system prompt: {prompts.system_prompt}\n
        initial response: {initial_response}
        Observasion: {observation}
                
        initial_response = llm.complete(initial_response)

agent("who are the celts?")

'''





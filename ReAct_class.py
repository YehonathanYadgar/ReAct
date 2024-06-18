import re
import os
from openai import OpenAI
from dotenv import load_dotenv
from tools import useWikipedia
import prompts

load_dotenv()

class ReAct:
    def __init__(self, model):
        self.model = model
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.messages = []
        self.available_actions = {
            "useWikipedia": useWikipedia
        }

    def generate_text_with_conversation(self, messages):
        response = self.openai_client.chat.completions.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message.content
        

    def action_extractor(self, text):
        action_regex = re.compile(r'^Action: (\w+): (.*)$')
        response_lines = text.split("\n")
        for line in response_lines:
            match = action_regex.search(line)
            if match:
                return match.group(1), match.group(2)
        print("No matching action found.")
        return None, None


    def run_session(self, user_prompt):
        function_name = None
        function_param = None

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

            response = self.generate_text_with_conversation(messages)

            print(response)

            try:
                function_name,function_param = self.action_extractor(response)
            except:
                print('finished')    

            if function_name:
                    if function_name not in self.available_actions:
                        raise Exception(f"Unknown action: {function_name}: {function_param}")
                    print(f" -- running {function_name} {function_param}")
                    action_function = self.available_actions[function_name]
                    #call the function
                    result = action_function(function_param)
                    function_result_message = f"Action_Response: {result}"
                    messages.append({"role": "user", "content": function_result_message})
                    print(function_result_message)
                    function_name = None
                    function_param = None
            else:
                break
# Example usage with specifying the model:
session = ReAct(model="gpt-3.5-turbo")
session.run_session("What's the Quran?")

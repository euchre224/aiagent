import os
import sys
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from functions.call_function import *
from prompts import system_prompt

def main():
    print("Hello from aiagent!")

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("There isn't an API key, unfortunately.")

    client = genai.Client(api_key=api_key)
    modeltext= "gemini-2.5-flash"
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    # contentstext = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    # contentstext = args.user_prompt


    MAX_ITERATIONS = 20

    for _ in range(MAX_ITERATIONS):
        response = client.models.generate_content(model=modeltext, contents=messages, config=types.GenerateContentConfig(tools=[available_functions], system_instruction=system_prompt, temperature=0))
        if response.candidates != None:
            for i in response.candidates:
                messages.append(i.content)

        if _ == MAX_ITERATIONS:
            print("No final response produced.")
            sys.exit(1)

        if response.usage_metadata == None:
            raise RuntimeError("client.models.generate_content.usage_metadata is None.")
        p_tokens = response.usage_metadata.prompt_token_count
        r_tokens = response.usage_metadata.candidates_token_count
        if args.verbose:
            print(f"User prompt: {args.user_prompt}\nPrompt tokens: {p_tokens}\nResponse tokens: {r_tokens}")
        
        function_results = []

        if not response.function_calls == None:
            for function_call in response.function_calls:
                print(f"Calling function: {function_call.name}({function_call.args})")
                function_call_result = call_function(function_call)
                if function_call_result.parts == None:
                    raise Exception("Nothing in the call_function.parts list.")
                
                if len(function_call_result.parts[0].function_response.response) == 0:
                    raise Exception("No function here, boss.")
                
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                
                function_results.append(function_call_result.parts[0])
                
            messages.append(types.Content(role="user", parts=function_results))

        else:
            print(response.text)
            break
        


if __name__ == "__main__":
    main()

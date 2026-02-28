import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
# from functions.call_function import available_functions
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
    contentstext = messages
    response = client.models.generate_content(model=modeltext, contents=contentstext, config=types.GenerateContentConfig(system_instruction=system_prompt, temperature=0))
    if response.usage_metadata == None:
        raise RuntimeError("client.models.generate_content.usage_metadata is None.")
    p_tokens = response.usage_metadata.prompt_token_count
    r_tokens = response.usage_metadata.candidates_token_count
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\nPrompt tokens: {p_tokens}\nResponse tokens: {r_tokens}")
    print(response.text)
    


if __name__ == "__main__":
    main()

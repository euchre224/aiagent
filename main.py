import os
from dotenv import load_dotenv
from google import genai
import argparse



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
    args = parser.parse_args()
    contentstext = args.user_prompt
    # contentstext = "Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum."
    response = client.models.generate_content(model=modeltext, contents=contentstext)
    if response.usage_metadata == None:
        raise RuntimeError("client.models.generate_content.usage_metadata is None.")
    p_tokens = response.usage_metadata.prompt_token_count
    r_tokens = response.usage_metadata.candidates_token_count
    print(f"Prompt tokens: {p_tokens}\nResponse tokens: {r_tokens}")
    print(response.text)
    


if __name__ == "__main__":
    main()

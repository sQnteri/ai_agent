import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    load_dotenv()
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
    except Exception:
        raise RuntimeError("No API key found")
    client = genai.Client(api_key=api_key)

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for i in range(20):

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt),
            )

        if response.usage_metadata is not None:
            if args.verbose == True:
                print(f"User prompt: {args.user_prompt}\nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
        else:
            raise RunTimeError("No metadata, likely failed API request")
        
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
        
        functions = response.function_calls
        function_results = []
        if functions:
            for function in functions:
                function_call_result = call_function(function)
                if not function_call_result.parts:
                    raise Exception('Parts is empty')
                if not function_call_result.parts[0].function_response:
                    raise Exception("No function response")
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("No function")
                function_results.append(function_call_result.parts[0])
                messages.append(types.Content(role="user", parts=function_results))
                if args.verbose == True:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
        else:
            print(response.text)
            break
    
    else:
        print("Maximum attempts reached wihout success.")
        sys.exit(1)
        


if __name__ == "__main__":
    main()

import os
import sys
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts import system_prompt
from call_function import available_functions, call_function

def main():
    """
    Orchestrates the AI Agent loop: takes user input, calls the LLM,
    handles tool/function exectution, and returns the final answer
    
    """
    
    load_dotenv()
    try:
        api_key = os.environ.get("GEMINI_API_KEY")
    except Exception:
        raise RuntimeError("No API key found")
    client = genai.Client(api_key=api_key)

    # Setup command line arguments for quick testing/debugging
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # Initialize message history with the user's input
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    
     # Reasoning Loop: Limits the agent to 20 turns to prevent infinite loops (and high costs)
    for i in range(20):

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt),
            )
        # Track token usage if verbose mode is on (useful for cost monitoring)
        if response.usage_metadata is not None:
            if args.verbose == True:
                print(f"User prompt: {args.user_prompt}\nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}")
        else:
            raise RunTimeError("No metadata, likely failed API request")
        
        # Add the Assistant's response to the message history to maintain context       
        if response.candidates:
            for candidate in response.candidates:
                messages.append(candidate.content)
        
        functions = response.function_calls
        function_results = []
        
        # Check if the AI wants to call a function (Tool Use)
        if functions:
            for function in functions:
                function_call_result = call_function(function)
                
                # Validation: Ensure the tool returned a valid response before proceeding
                if not function_call_result.parts:
                    raise Exception('Parts is empty')
                if not function_call_result.parts[0].function_response:
                    raise Exception("No function response")
                if not function_call_result.parts[0].function_response.response:
                    raise Exception("No function")
                function_results.append(function_call_result.parts[0])
                if args.verbose == True:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                    
            # Feed the function results back to the AI as a 'user' role so it can interpret them
            messages.append(types.Content(role="user", parts=function_results))
            
        else:
            # If no functions were called, the AI has its final answer
            print(response.text)
            break
    
    else:
        # This triggers only if the for-loop completes 20 iterations without a 'break'
        print("Maximum attempts reached wihout success.")
        sys.exit(1)
        


if __name__ == "__main__":
    main()

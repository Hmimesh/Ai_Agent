import os
from dotenv import load_dotenv
from google import genai
import argparse
from google.genai import types
from prompts import system_prompt
from functions.call_function import available_function, call_function




def get_api_key() -> str:
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key == None:
        raise RuntimeError("GEMINI_API_KEY is not set")
    return api_key

parser = argparse.ArgumentParser(description="AI_Agent")
parser.add_argument("user_prompt", type=str, help="User prompt")
parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
args = parser.parse_args()



def generate_response(client, messages):
    return client.models.generate_content(
        model='gemini-2.5-flash',
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_function], system_instruction=system_prompt
        ),
    )



def main():
    
    MAX_ITERATION = 20

    
    client = genai.Client(api_key=get_api_key())
    
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    

    for i in range(MAX_ITERATION):

        function_results = []
        response = generate_response(client, messages)

        for candidate in response.candidates:
            messages.append(candidate.content)


        if args.verbose == True:
            print(f"User prompt: {args.user_prompt}")
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")


        if response.function_calls:
            for function_call in response.function_calls:
                function_call_result = call_function(function_call)
                if not function_call_result.parts:
                    raise Exception("Must have parts")
                if function_call_result.parts[0].function_response is None:
                    raise Exception("First part cannot be None type")
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("Result cannot be None type")
                
                function_results.append(function_call_result.parts[0])
                if args.verbose == True:
                    print(f"-> {function_call_result.parts[0].function_response.response}")


        else:
            print(response.text)
            break
        
        messages.append(types.Content(role="user", parts=function_results))
    else:
        print("couldnt find a last response")
        exit(1)


if __name__ == "__main__":
    main()

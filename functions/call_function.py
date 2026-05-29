from google.genai import types
from functions.get_files_info import schema_get_files_info, get_files_info
from functions.run_python_file import schema_run_python_file, run_python_file
from functions.write_in_file import schema_write_file, write_file
from functions.get_file_contents import schema_get_files_content, get_file_contents
from collections.abc import Callable

available_function = types.Tool(
    function_declarations=[schema_get_files_info, schema_get_files_content, schema_run_python_file, schema_write_file],
)

def call_function(
        function_call: types.FunctionCall, verbose: bool = False
) -> types.Content:
    function_name = function_call.name or ""
    if verbose:
        print(f"Calling function: {function_name}({function_call.args})")
    else:
        print(f" - Calling function: {function_name}")
    
    function_map: dict[str, Callable[..., str]] = {
        "get_file_content": get_file_contents,
        "get_files_info": get_files_info,
        "write_file": write_file,
        "run_python_file": run_python_file,
    }
    
    

    if function_name not in function_map:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    args = dict(function_call.args) if function_call.args else {}
    args["working_directory"] = "./calculator"

    function_to_call = function_map[function_name]

    try:
        function_result = function_to_call(**args)
    except Exception as e:
        function_result = f"Error while running {function_name}: {e}"

    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": function_result},
            )
        ],
    )


    
   
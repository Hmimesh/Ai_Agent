import os
from google.genai import types
#This func is for the agent to write in files in the scope of the agent

def write_file(working_directory, file_path, content):
    
    abs_working_directory = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(abs_working_directory, file_path))
    valid_target_file = os.path.commonpath([abs_working_directory, target_file]) == abs_working_directory
    if not valid_target_file:
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    if os.path.isdir(target_file):
        return f'Error cannot write to "{file_path}" as it is a directory'
    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    
    try:
        with open(target_file, "w") as f:
            f.write(content)
        return f'Successfully wrote to"{file_path}" ({len(content)} characters written'
    except Exception as e:
        return f"Error: {e}"



schema_write_file = types.FunctionDeclaration(
     name="write_file",
     description="write into file",
     parameters=types.Schema(
          required=["file_path", "content"],
          type=types.Type.OBJECT,
          properties={
               "file_path": types.Schema(
                    type=types.Type.STRING,
                    description="Directory path to list files from, relative to working directory (default is the working directory itself)",
               ),
               "content": types.Schema(
                   type=types.Type.STRING,
                   description="The content to fill into the file.",
               ),
          },
     ),
)
    
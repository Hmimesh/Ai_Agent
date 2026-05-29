import os
from google.genai import types


# This func is for getting the files in scope for the agent to work with
def get_files_info(working_directory, directory="."):
    working_directory_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_directory_abs, directory))
    valid_target_dir = os.path.commonpath([working_directory_abs, target_dir]) == working_directory_abs
    # catch in string for Agent to act upon
    if not valid_target_dir: 
        return (f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
    if not os.path.isdir(target_dir):
            return (f"Error: '{directory}' is not a directory")
    #getting file info and putting in string
    try:
        files = os.listdir(target_dir)
        result = []
        for file in files:
            file_path = os.path.join(target_dir, file)
            is_dir = os.path.isdir(file_path)
            size = os.path.getsize(file_path)
            line = f'- {file}: file_size={size} bytes, is_dir={is_dir}'
            result.append(line)
    except Exception as e:
        return f"Error: {e}"
    return "\n".join(result)


schema_get_files_info = types.FunctionDeclaration(
     name="get_files_info",
     description="List files in a specified directory relative to the working directory, providing file size and directory status",
     parameters=types.Schema(
          type=types.Type.OBJECT,
          properties={
               "directory": types.Schema(
                    type=types.Type.STRING,
                    description="Directory path to list files from, relative to working directory (default is the working directory itself)",
               ),
          },
     ),
)

import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    abs_working_directory = os.path.abspath(working_directory)
    target_file = os.path.normpath(os.path.join(abs_working_directory, file_path))
    valid_target_file = os.path.commonpath([abs_working_directory, target_file]) == abs_working_directory
    if not valid_target_file:
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_file):
        return f'Error:"{file_path}" does not exist or is not a regular file'
    if not target_file.endswith(".py"):
        return f'Error "{file_path}" is not a Python file'
    
    command = ["python", target_file]
    
    if args:
        command.extend(args)
    try:
        result = subprocess.run(command, cwd=abs_working_directory ,timeout=30,capture_output=True, text=True)
        output_code = result.returncode
        string_list = [] 
        if output_code != 0:
            string_list.append(f'Process exited with code {output_code}')
        stdout = str(result.stdout)
        stderr = str(result.stderr)
        if not stdout and not stderr:
            string_list.append(f'Process no output produced')
        else:
            string_list.append(f'STDOUT:\n{stdout}\n STDERR:\n{stderr}')
            words = "\n".join(string_list)
            return words
    except Exception as e:
        return f'Error: executing python file: {e}'
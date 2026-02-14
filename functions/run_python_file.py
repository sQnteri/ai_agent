import os
import subprocess
from google.genai import types

def run_python_file(working_directory, file_path, args=None):
    working_dir_abs = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_path = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs

    if not valid_target_path:
        return f'   Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    if not os.path.isfile(target_path):
        return f'   Error: "{file_path}" does not exist or is not a regular file'
    if not file_path.endswith('.py'):
        return f'   Error: "{file_path}" is not a Python file'

    command = ["python", target_path]
    if args:
        command.extend(args)

    try: 
        process = subprocess.run(args=command, capture_output=True, text=True, timeout=30)

        output_string = ""

        if process.returncode != 0:
            output_string += f'Process exited with code {process.returncode}'
        if not process.stdout and not process.stderr:
            output_string += 'No output produced'
        else:
            output_string += f'STDOUT: {process.stdout}\nSTDERR: {process.stderr}'

        return output_string
    
    except Exception as e:
        return f'Error: executing Python file: {e}'


schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description=f"Runs a python file in a specified path relative to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="File path for the file to run, relative to the working directory",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="List of arguments for the python program",
                items=types.Schema(
                    type=types.Type.STRING,
                    description="Individual arguments in the args list"
                )
            ), 
        },
        required=["file_path"]
    ),
)
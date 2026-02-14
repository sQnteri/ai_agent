import os
from google.genai import types

def write_file(working_directory, file_path, content):
    working_dir_abs = os.path.abspath(working_directory)
    target_path = os.path.normpath(os.path.join(working_dir_abs, file_path))
    valid_target_path = os.path.commonpath([working_dir_abs, target_path]) == working_dir_abs

    if os.path.isdir(target_path):
        return f'   Cannot write to "{file_path}" as it is a directory'
    if not valid_target_path:
        return f'   Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

    dir_name = os.path.dirname(target_path)

    try:
        os.makedirs(dir_name, exist_ok=True)
        with open(target_path, "w") as f:
            f.write(content)
            return f'Succesfully wrote to "{file_path}" ({len(content)} characters written)'
            
    except Exception as e:
        return f'   Error: {e}'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Overwrites the contents of a file in a specified path relative to the working directory. If the path or file doesn't exist yet, creates it first",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path to the file to write to, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content you want to write to the file",
            ),
        },
        required=["file_path", "content"]
    ),
)
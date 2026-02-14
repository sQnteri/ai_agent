import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
    
    if not os.path.isdir(target_dir):
        return f'   Error: "{directory}" is not a directory'
    if not valid_target_dir:
        return f'   Error: Cannot list "{directory}" as it is outside the permitted working directory'

    dir_string =""
    try:
        for item in os.scandir(target_dir):
            t = item.is_dir() 
            s = item.stat().st_size
            dir_string += f"   - {item.name}: file_size={s} bytes, is_dir={t}\n"
    except Exception:
        return "   Error: couldn't scan directory"
    
    return dir_string


schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


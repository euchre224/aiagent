import os
from config import MAX_CHARS

def get_file_content(working_directory, file_path):
    try:
        # print("lol")
        working_dir_abs = os.path.abspath(working_directory)
        # print(working_dir_abs)
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # print(target_file)

        # Will be True or False
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        # print(valid_target_file)
        if valid_target_file == False:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        file_path_isfile = os.path.isfile(target_file)
        # print(file_path_isfile)
        if file_path_isfile == False:
            return f'Error: File not found or is not a regular file: "{file_path}"'
        # print("lmao")
        with open(target_file, "r") as f:
            file_content_string = f.read(MAX_CHARS + 1)
        
        if len(file_content_string) > MAX_CHARS:
            # print(len(file_content_string[0:(MAX_CHARS)]))
            content = file_content_string[0:(MAX_CHARS)] + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
        else: 
            content = file_content_string
        return content 
    except:
        return "Error: Function get_file_content failed to execute."
    
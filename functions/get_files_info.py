import os
from google.genai import types

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

def get_files_info(working_directory, directory="."):
    try:
        # print("lol")
        working_dir_abs = os.path.abspath(working_directory)
        # print(working_dir_abs)
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory))
        # print(target_dir)

        # Will be True or False
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs
        # print(valid_target_dir)
        if valid_target_dir == False:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        directory_isdir = os.path.isdir(target_dir)
        # print(directory_isdir)
        if directory_isdir == False:
            return f'Error: "{directory}" is not a directory'
        
        target_dir_files = os.listdir(target_dir)
        # print(target_dir_files)
        filelist = []
        for file in target_dir_files:
            filepath = target_dir + "/" + file
            filesize = os.path.getsize(filepath)
            # print(filesize)
            fileisdir = os.path.isdir(filepath)
            # print(fileisdir)
            filestring = f"- {file}: file_size={filesize} bytes, is_dir={fileisdir}"
            # print(filestring)
            filelist.append(filestring)
            # print(filelist)
        # print(filelist)
        strfilelist = "\n".join(filelist)
        if directory == ".":
            startstring = "Result for current directory:"
        else:
            startstring = f"Result for '{directory}' directory:"
        total_output = f"{startstring}\n{strfilelist}"
        return total_output
    except:
        # print("Error: The function started, but failed to complete.")
        return "Error: Function get_files_info failed to execute."

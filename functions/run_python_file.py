import os
from google.genai import types
import subprocess

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Runs a specified python file and outputs a string.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        required=["file_path"],
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Stated file to open and run.",
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                description="Optional. List of extra information added. This is optional.",
                items=types.Schema(
                        type=types.Type.STRING,
                        description="The individual items inside the args list.",)
            ),
        },
    ),
)

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        # print(working_dir_abs)

        divider = working_dir_abs[0]

        
        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # print(target_file)

        
        # Will be True or False
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        # print(valid_target_file)
        if valid_target_file == False:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        
        file_path_isfile = os.path.isfile(target_file)
        # print(file_path_isfile)
        if file_path_isfile == False:
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if not file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", target_file]
        
        if not args == None:
            command.extend(args)

        Process_Ob = subprocess.run(command, stdout=None, stderr=None, capture_output=True, timeout=30, text=True)

        outputlist = []

        if Process_Ob.returncode != 0:
            outputlist.append(f"Process exited with code {Process_Ob.returncode}.")
        
        if (Process_Ob.stdout == "") and (Process_Ob.stderr ==""):
            outputlist.append("No output produced")
        if Process_Ob.stdout != "":
            outputlist.append(f"STDOUT: {Process_Ob.stdout}")
        if Process_Ob.stderr != "":
            outputlist.append(f"STDERR: {Process_Ob.stderr}")

        if outputlist != []:
            output = "\n".join(outputlist)
        else:
            output = ""
        
        return output

    except Exception as e:
        return f"Error: executing Python file: {e}"
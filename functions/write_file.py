import os

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory)
        # print(working_dir_abs)

        divider = working_dir_abs[0]

        # if file_path[0] == divider:
        #     file_path = file_path[1:]

        target_file = os.path.normpath(os.path.join(working_dir_abs, file_path))
        # print(target_file)

        
        # Will be True or False
        valid_target_file = os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        # print(valid_target_file)
        if valid_target_file == False:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        


        last_divider = file_path.rfind(divider)

        newdirs = ""
        if not last_divider == -1:
            newdirs = file_path[0:last_divider]

        totaldirs = os.path.normpath(os.path.join(working_dir_abs, newdirs))
        os.makedirs(totaldirs, exist_ok=True) 
        
        
        file_path_isdir = os.path.isdir(target_file)
        # print(file_path_isdir)
        if file_path_isdir == True:
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        # print("lmao")

        
        
        with open(target_file, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except:
        return "Error: Function write_file failed to execute."
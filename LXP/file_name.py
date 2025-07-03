import os

# Define the directory path
directory = r'D:\nubeera\LXP'

# Walk through the directory and its subdirectories
for root, dirs, files in os.walk(directory):
    for file in files:
        if 'module' in file.lower():
            # Full path of the file
            old_file_path = os.path.join(root, file)
            
            # Ask the user for confirmation to rename the file
            print(f"Found file: {old_file_path}")
            response = input("Do you want to rename 'module' to 'course' in the filename? (y/n): ").strip().lower()

            if response == 'y':
                # Create the new file name by replacing 'module' with 'course'
                new_file_name = file.replace('module', 'course')
                new_file_path = os.path.join(root, new_file_name)

                # Rename the file
                os.rename(old_file_path, new_file_path)
                print(f"File renamed to: {new_file_path}")
            elif response == 'n':
                print("File not renamed.")
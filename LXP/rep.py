import os

# Set the directory path
directory = r"D:\nubeera\LXP\templates\staff\runningactivity"

# Define replacements as a dictionary
replacements = {
    "Subject": "Playlist",
    "subject": "playlist",
    "Chapter": "Video",
    "chapter": "video",
    "Activity": "RunningActivity",
    "activity": "runningactivity"
}

# Walk through each file in the directory
for filename in os.listdir(directory):
    if filename.endswith(".html"):
        file_path = os.path.join(directory, filename)
        
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        # Perform replacements
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        # Write the updated content back to the file
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(content)

print("Replacement completed.")

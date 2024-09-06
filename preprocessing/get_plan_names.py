import os

def extract_plan_title_from_file(filepath):

    with open(filepath, 'r') as file:
        for line in file:
            if 'Plan Title=' in line:
                # Extract the text to the right of the equals sign
                plan_title = line.split('=')[1].strip()
                # remove extension from plan_title
                plan_title = os.path.splitext(plan_title)[0]
                break  # Stop after the first match is found
        return plan_title

def extract_plan_titles_from_dir(directory):
    plan_titles = {}

    # Iterate through all files in the directory
    for filename in os.listdir(directory):
        # Skip files that end with .hdr and files that do not match the '*.p*' pattern
        if filename.endswith(".hdr") or not any(filename.endswith(ext) for ext in [f".p{str(i).zfill(2)}" for i in range(100)]):
            continue
        
        plan_titles[filename] = extract_plan_title_from_file(filename)
               
    return plan_titles

def main():
    # Set the directory containing the .p* files
    directory = r"C:\ATD\Hydraulic Models\Bennett_Test"  # Change this to your directory

    # Extract Plan Titles
    plan_titles = extract_plan_titles_from_dir(directory)

    # Print the results
    for filename, title in plan_titles.items():
        print(f"{filename}: {title}")

if __name__ == "__main__":
    main()

# copies the titles over from a metadata sheet containing all the titles to the target sheet or sheets
# only copies titles for OBJs, this is used for book pages and possibly compound objects
# ideally the target csv is all the filesets and attachments for that collection
# the "source_csv" is the one with the proper titles
# So far this has only been done for beacon, but it needs to be done for all of the remaining collections
# before they are imported
import csv
import sys
import os

def read_titles_from_csv(filename):
    titles = {}
    with open(filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            titles[row['source_identifier'].split('_OBJ')[0]] = row['title']
    return titles

def update_titles_in_csv(source_filename, target_filename):
    titles = read_titles_from_csv(source_filename)
    updated_rows = []

    with open(target_filename, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        for row in reader:
            source_id = row['source_identifier'].split('_OBJ')[0]
            if source_id in titles and row['title'] == "OBJ":
                row['title'] = titles[source_id]
            updated_rows.append(row)

    new_target_filename = target_filename.replace('.csv', '_titles_added.csv')
    with open(new_target_filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(updated_rows)

def process_directory(source_filename, target_directory):
    for filename in os.listdir(target_directory):
        if filename.endswith(".csv"):
            target_filepath = os.path.join(target_directory, filename)
            update_titles_in_csv(source_filename, target_filepath)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python titlecopy.py <source_csv> <target_csv_or_directory>")
        sys.exit(1)

    source_csv = sys.argv[1]
    target_path = sys.argv[2]

    if os.path.isdir(target_path):
        process_directory(source_csv, target_path)
    else:
        update_titles_in_csv(source_csv, target_path)

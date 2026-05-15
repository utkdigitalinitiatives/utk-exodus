import csv
import sys
import tqdm

if len(sys.argv) != 3:
  print("Usage: python script.py <full_collection_sheet> <output_sheet>")
  sys.exit(1)

unified_sheet = sys.argv[1]
output_sheet = sys.argv[2]

# Read all data and separate into parents and children
all_data = []
with open(unified_sheet, 'r') as file:
  reader = csv.DictReader(file)
  all_data = list(reader)

# Filter parents (model='Book') and children (model='Attachment')
parents = [row for row in all_data if row.get('model') == 'Book'] #  CHANGE THIS WHEN DIFFERENT MODEL
children_data = [row for row in all_data if row.get('model') == 'Attachment']

# Write enriched parents to output
fieldnames = ['source_identifier', 'model', 'parents', 'primary_identifier', 'title', 'children']

with open(output_sheet, 'w', newline='') as outfile:
  writer = csv.DictWriter(outfile, fieldnames=fieldnames)
  writer.writeheader()
  
  for parent_row in tqdm.tqdm(parents):
    parent_id = parent_row.get('source_identifier')
    
    matching_children = []
    for child_row in children_data:
      if child_row.get('parents') == parent_id:
        matching_children.append(child_row.get('source_identifier'))
    
    parent_row['children'] = ' | '.join(matching_children)
    writer.writerow({field: parent_row.get(field, '') for field in fieldnames})
import csv
import sys

class FixMetadata:
    def __init__(self, titles, remove_columns=False):
        self.titles = titles
        self.remove_columns = remove_columns

    def update_metadata(self, csv_filename):
        keywords = self.titles
        remove_columns = self.remove_columns
        keywords_list = [keyword.lower() for keyword in keywords.split(',')]
        with open(csv_filename, mode='r', newline='') as infile:
            reader = csv.DictReader(infile)
            rows = list(reader)

        attachment_rows = [row for row in rows if row['model'].lower() == 'attachment']
        fileset_rows = [row for row in rows if row['model'].lower() == 'fileset']

        if len(attachment_rows) + len(fileset_rows) != len(rows):
            print("unexpected model in sheet")
            sys.exit(1)

        attachment_rows.sort(key=lambda row: ('obj' in row['title'].lower() or 'preserve' in row['title'].lower(), row['title'].lower()))
        fileset_rows.sort(key=lambda row: ('obj' in row['title'].lower() or 'preserve' in row['title'].lower(), row['title'].lower()))
        rows = attachment_rows + fileset_rows

        for row in rows:
            if row['title'].lower() == 'ocr':
                row['rdf_type'] = 'http://pcdm.org/use#ExtractedText'
            elif row['title'].lower() == 'hocr':
                row['rdf_type'] = 'http://pcdm.org/file-format-types#HTML'

        with open(csv_filename, mode='w', newline='') as outfile:
            fieldnames = reader.fieldnames
            if remove_columns:
                # Here are the columns that will not get removed when using the remove columns option
                fieldnames = ['source_identifier', 'title', 'model', 'visibility']
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                if any(keyword in row['title'].lower() for keyword in keywords_list):
                    row['visibility'] = 'restricted'
                if remove_columns:
                    row = {key: row[key] for key in fieldnames}
                writer.writerow(row)

if __name__ == "__main__":
    print("use this space to test metadata fixes if needed")
#!/usr/bin/env python3
"""
Usage:
  python3 header_finding.py <path_to_csv_or_folder>

Use this to write it to a file:
  python3 header_finding.py <path_to_csv_or_folder> > <path_to_filename>

Example usage:
  python3 header_finding.py all_full_sheets > data.csv

Arguments:
  path_to_csv_or_folder: Path to either a single CSV file or a directory containing CSV files
Output:
  Prints a csv of the collections data

"""
import csv
import sys
from pathlib import Path

def count_non_blank_cells(csv_path): # counts the non blank cells of each header in a given csv
  counts = {}
  
  with open(csv_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)

    headers = next(reader)

    for header in headers:
      counts[header] = 0

    for row in reader:
      for i, cell in enumerate(row):
        if i < len(headers) and cell.strip():  # checks if cell is not blank
          counts[headers[i]] += 1
  
  return counts


def print_results_as_csv(counts, filename): # outputting the csv
  writer = csv.writer(sys.stdout)
  headers = ['collection'] + list(counts.keys())
  writer.writerow(headers)

  counts_row = [filename] + list(counts.values())
  writer.writerow(counts_row)


def process_csv_file(csv_path): # for a single csv
  counts = count_non_blank_cells(csv_path)
  return (csv_path.stem, counts)


def print_multiple_results_as_csv(results): # for a folder of csvs
  if not results:
    return
  
  # gets all the unique headers from all the files, use the order from the first one
  all_headers = []
  seen_headers = set()
  for _, counts in results:
    for header in counts.keys():
      if header not in seen_headers:
        all_headers.append(header)
        seen_headers.add(header)

  writer = csv.writer(sys.stdout)

  writer.writerow(['collection'] + all_headers)

  for filename, counts in results:
    counts_row = [filename] + [counts.get(header, 0) for header in all_headers]
    writer.writerow(counts_row)


def main():
  if len(sys.argv) != 2:
    print("Usage: python header_finding.py <path_to_csv_or_folder>", file=sys.stderr)
    sys.exit(1)
    
  path = Path(sys.argv[1])
  
  if not path.exists():
    print(f"Error: Path '{path}' not found", file=sys.stderr)
    sys.exit(1)
  
  try:
    if path.is_file(): # for just a single file
      counts = count_non_blank_cells(path)
      print_results_as_csv(counts, path.stem)
    elif path.is_dir(): # for a folder of files 
      csv_files = sorted(path.glob('*.csv'))
      if not csv_files:
        print(f"Error: No CSV files found in '{path}'", file=sys.stderr)
        sys.exit(1)
      results = []
      for csv_file in csv_files:
        try:
          filename, counts = process_csv_file(csv_file)
          results.append((filename, counts))
        except Exception as e:
          print(f"Warning: Error processing {csv_file.name}: {e}", file=sys.stderr)
      if results:
        print_multiple_results_as_csv(results)
      else:
        print("Error: No CSV files could be processed", file=sys.stderr)
        sys.exit(1)
    else:
      print(f"Error: '{path}' is not a file or directory", file=sys.stderr)
      sys.exit(1)

  except Exception as e:
    print(f"Error: {e}", file=sys.stderr)
    sys.exit(1)

if __name__ == "__main__":
  main()
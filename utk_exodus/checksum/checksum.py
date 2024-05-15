import hashlib
from csv import DictWriter, DictReader
import os
import requests
from tqdm import tqdm


class HashSheet:
    def __init__(self, path, output):
        self.path = path
        self.output = output
        self.all_files = self.walk_sheets(path)

    @staticmethod
    def walk_sheets(path):
        all_files = []
        for path, directories, files in os.walk(path):
            for filename in files:
                with open(f"{path}/{filename}", "r") as f:
                    reader = DictReader(f)
                    for row in reader:
                        all_files.append(row["remote_files"])
        return all_files

    def checksum(self):
        files_with_checksums = []
        for file in tqdm(self.all_files):
            response = requests.get(file, stream=True)
            response.raise_for_status()
            sha1 = hashlib.sha1()
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    sha1.update(chunk)
            files_with_checksums.append({"url": file, "checksum": sha1.hexdigest()})
        return files_with_checksums

    def write(self):
        with open(self.output, "w") as csvfile:
            writer = DictWriter(csvfile, fieldnames=["url", "checksum"])
            writer.writeheader()
            writer.writerows(self.checksum())
        return


if __name__ == "__main__":
    path = "delete/bad_imports"
    output = "delete/sample_checksums.csv"
    checksum = HashSheet(path, output)
    checksum.write()

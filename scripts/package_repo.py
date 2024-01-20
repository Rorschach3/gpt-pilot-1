import os
import shutil
import zipfile
from tempfile import TemporaryDirectory
from subprocess import check_call

# Only these top-level items will be included in the package
INCLUDE = [
    "pilot",
    "Dockerfile",
    "docker-compose.yml",
    "LICENSE",
    "README.md",
    "requirements.txt",
    "setup.py"
]

def main():
    # Change working directory to the root of the repository
    if not os.path.exists("pilot"):
        print("This script must be run from the root of the repository")
        return

    with TemporaryDirectory() as tmp_dir:
        # Create a repository archive
        temp_archive_path = os.path.join(tmp_dir, "repository.zip")
        check_call(["git", "archive", "-o", temp_archive_path, "main"])
        check_call(["unzip", "-qq", "-x", temp_archive_path], cwd=tmp_dir)

        # Remove all items from the archive that aren't explictly whitelisted
        for item in os.listdir(tmp_dir):
            if item not in INCLUDE:
                path = os.path.join(tmp_dir, item)
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    shutil.rmtree(path)

        archive_path = os.path.abspath(os.path.join("..", "gpt-pilot-packaged.zip"))
        if os.path.exists(archive_path):
            os.remove(archive_path)

        with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for dpath, dirs, files in os.walk(tmp_dir):
                for file in files:
                    full_path = os.path.join(dpath, file)
                    if full_path != temp_archive_path:
                        rel_path = os.path.relpath(full_path, tmp_dir)
                        print(rel_path)
                        zip_file.write(full_path, rel_path)

        print("\nCreated", archive_path)


if __name__ == "__main__":
    main()

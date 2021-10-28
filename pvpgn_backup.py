import os
import zipfile
import datetime as dt
import logging


def backup():
    archive_path = dt.datetime.utcnow().strftime("C:/char_backup/%Y/%m/%d/")
    archive_file = dt.datetime.utcnow().strftime("ESR_char_backup_%H%M.zip")
    if not os.path.exists(archive_path):
        logging.info("Creating new directory: "+archive_path)
        os.makedirs(archive_path)
    backup_archive = zipfile.ZipFile(archive_path+archive_file, 'w')
    for folder, subfolders, files in os.walk("C:/pvpgn/release/var"):
        for file in files:
            if not '.log' in file:
                backup_archive.write(
                    os.path.join(folder, file),
                    os.path.relpath(os.path.join(folder, file), 'C:/pvpgn/release/var'),
                    compress_type=zipfile.ZIP_DEFLATED)
    backup_archive.close()
    return archive_path+archive_file


if __name__ == "__main__":
    backup()

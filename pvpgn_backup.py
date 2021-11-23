import os
import zipfile
import datetime as dt
import logging

logging.basicConfig(filename='/home/d2esr/char_backup/backup.log', encoding='utf-8', level=logging.DEBUG)

def backup():
    archive_path = dt.datetime.utcnow().strftime("/home/d2esr/char_backup/%Y/%m/%d/")
    archive_file = dt.datetime.utcnow().strftime("ESR_char_backup_%H%M.zip")
    if not os.path.exists(archive_path):
        logging.info("Creating new directory: "+archive_path)
        os.makedirs(archive_path)
    backup_archive = zipfile.ZipFile(archive_path+archive_file, 'w')
    for folder, subfolders, files in os.walk("/home/d2esr/pvpgn/release/var"):
        for file in files:
            if not '.log' in file:
                backup_archive.write(
                    os.path.join(folder, file),
                    os.path.relpath(os.path.join(folder, file), '/home/d2esr/pvpgn/release/var'),
                    compress_type=zipfile.ZIP_DEFLATED)
    backup_archive.close()
    return archive_path+archive_file


if __name__ == "__main__":
    fil = backup()
    logging.info("Wrote "+fil)

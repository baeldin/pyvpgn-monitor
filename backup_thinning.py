import os
import logging
import datetime as dt
import glob

logging.basicConfig(filename='/home/d2esr/char_backup/backup.log', encoding='utf-8', level=logging.DEBUG)

def backup_thinning_to_hourly():
    thin_date = dt.date.today() - dt.timedelta(days=4)
    count = 0
    for hh in range(24):
        for mm in [10, 20, 30, 40, 50]:
            backup_file_path = "/home/d2esr/char_backup/{:s}/ESR_char_backup_{:02d}{:02d}.zip".format(
                thin_date.strftime("%Y/%m/%d"), hh, mm)
            if os.path.exists(backup_file_path):
                os.remove(backup_file_path)
                count += 1
    return count


def backup_thinning_to_3hourly():
    thin_date = dt.date.today() - dt.timedelta(days=10)
    count = 0
    for hh in range(24):
        if hh%3 > 0:
            backup_file_path = "/home/d2esr/char_backup/{:s}/ESR_char_backup_{:02d}00.zip".format(
                thin_date.strftime("%Y/%m/%d"), hh)
            if os.path.exists(backup_file_path):
                os.remove(backup_file_path)
                count += 1
    return count


def backup_thinning_to_daily():
    thin_date = dt.date.today() - dt.timedelta(days=30)
    count = 0
    for hh in range(24):
        if hh > 0:
            backup_file_path = "/home/d2esr/char_backup/{:s}/ESR_char_backup_{:02d}00.zip".format(
                thin_date.strftime("%Y/%m/%d"), hh)
            if os.path.exists(backup_file_path):
                os.remove(backup_file_path)
                count += 1
    return count


def main():
    count = backup_thinning_to_hourly()
    count += backup_thinning_to_3hourly()
    count += backup_thinning_to_daily()
    logging.info("Thinning backups, removed "+str(count)+" old files.")


if __name__ == "__main__":
    main()

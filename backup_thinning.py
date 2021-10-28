import os
import datetime as dt
import glob

def backup_thinning_to_hourly():
    thin_date = dt.date.today() - dt.timedelta(days=4)
    # print(thin_date.strftime("C:/char_backup/%Y/%m/%d"))
    count = 0
    # while dd <= d_end:
    for hh in range(24):
        for mm in [10, 20, 30, 40, 50]:
            backup_file_path = "C:/char_backup/{:s}/ESR_char_backup_{:02d}{:02d}.zip".format(
                thin_date.strftime("%Y/%m/%d"), hh, mm)
            # print(backup_file_path)
            if os.path.exists(backup_file_path):
                os.remove(backup_file_path)
                count += 1
            # os.remove("C:/char_backup/2021/04/{:02d}/ESR_char_backup_{:02d}{:02d}.zip".format(
            #     dd, hh, mm
            # ))
    # print(count)
    return count


def backup_thinning_to_3hourly():
    thin_date = dt.date.today() - dt.timedelta(days=10)
    # print(thin_date.strftime("C:/char_backup/%Y/%m/%d"))
    count = 0
    # while dd <= d_end:
    for hh in range(24):
        if hh%3 > 0:
        #for mm in [10, 20, 30, 40, 50]:
            backup_file_path = "C:/char_backup/{:s}/ESR_char_backup_{:02d}00.zip".format(
                thin_date.strftime("%Y/%m/%d"), hh)
            # print(backup_file_path)
            if os.path.exists(backup_file_path):
                os.remove(backup_file_path)
                count += 1
            # os.remove("C:/char_backup/2021/04/{:02d}/ESR_char_backup_{:02d}{:02d}.zip".format(
            #     dd, hh, mm
            # ))
    # print(count)
    return count


def backup_thinning_to_daily():
    thin_date = dt.date.today() - dt.timedelta(days=30)
    # print(thin_date.strftime("C:/char_backup/%Y/%m/%d"))
    count = 0
    # while dd <= dt.date.today() - dt.timedelta(days=30):
    for hh in range(24):
        if hh > 0:
            backup_file_path = "C:/char_backup/{:s}/ESR_char_backup_{:02d}00.zip".format(
                thin_date.strftime("%Y/%m/%d"), hh)
            # print(backup_file_path)
            if os.path.exists(backup_file_path):
                os.remove(backup_file_path)
                count += 1
            # os.remove("C:/char_backup/2021/04/{:02d}/ESR_char_backup_{:02d}{:02d}.zip".format(
            #     dd, hh, mm
            # ))
    #dd += dt.timedelta(days=1)
    #print(dd)
    #print(count)
    return count


def main():
    count = backup_thinning_to_hourly()
    count += backup_thinning_to_3hourly()
    count += backup_thinning_to_daily()
    print(count)


if __name__ == "__main__":
    main()
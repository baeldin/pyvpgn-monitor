import argparse
import binascii


char_save_dir = "/home/d2esr/pvpgn/var/pvpgn/charsave/"


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('charname', type=str, help='character name')
    args = parser.parse_args()
    return args


#https://gist.github.com/cincodenada/6557582
def rotl(num, bits):
    bit = num & (1 << (bits - 1))
    num <<= 1
    if(bit):
        num |= 1

    num &= ((1 << bits) - 1)
    return num


def rehash_save(savebytes):
    print("Old Hash:", savebytes[12:16].hex())
    hash = 0
    savebytes[0xC] = 0;
    savebytes[0xD] = 0;
    savebytes[0xE] = 0;
    savebytes[0xF] = 0;
    for b in savebytes:
        hash = rotl(hash, 32)
        hash += int(b)

    savebytes[0xC] = (hash >> 0) & 0xFF
    savebytes[0xD] = (hash >> 8) & 0xFF
    savebytes[0xE] = (hash >> 16) & 0xFF
    savebytes[0xF] = (hash >> 24) & 0xFF
    print("New Hash:", savebytes[12:16].hex())
    return savebytes


def main():
    args = parse_arguments()
    char_save_file = char_save_dir + args.charname
    print("Removing ladder flag from "+char_save_file)
    with open(char_save_file, "r+b") as f:
        a = bytearray(f.read())
    print(a[0:60])
    a[0x24] &= ~0x40
    print(a[0:60])
    a = rehash_save(a)
    with open(args.charname+".d2s", "w+b") as f:
        f.write(a)


if __name__ == "__main__":
    main()

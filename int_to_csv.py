# mars_cd.datを読み込み、csvに変換するスクリプト
import struct
from sys import argv

FORMAT = "<hhhh"  # リトルエンディアンで4つの16ビット sigined 整数


def int_to_csv(input_file, output_file):
    with open(input_file, mode="rb") as f:
        data = f.read()
    with open(output_file, mode="w") as f:
        f.write("line_cd,station_cd,eigyo_kiro_rel,keisan_kiro_rel\n")
        for i in struct.iter_unpack(FORMAT, data):
            if i[0] == 0:
                # ヘッダー行をスキップ
                continue
            f.write("{},{},{},{}\n".format(i[0], i[1], i[2], i[3]))


if __name__ == "__main__":
    if len(argv) != 3:
        print("Usage: python int_to_csv.py <input_file> <output_file>")
    else:
        int_to_csv(argv[1], argv[2])

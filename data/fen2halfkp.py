from halfkp_libs.halfkp_lib import Half_KP_Converter
from halfkp_libs.chess_lib import Chess_Lib
import os
import traceback
import datetime

DIRECTORY = "/Users/littlecapa/data_lake/krk/data"
FILE_NAME = "KRk.csv"
FILE_NAME_OUT = "KRk_halfkp.csv"
DELIMITER = ";"

def convert_row(row, hkp_converter):
    #row_parts = row.split(";")
    fen = row[0]
    fen_parts = fen.split()
    # Keep only the first three elements (pieces, active color, and castling availability)
    new_fen = ' '.join(fen_parts[:3])
    fen_tensor = hkp_converter.fen2tensor(new_fen).tolist()
    eval = row[1]
    mate = abs(int(row[2]))
    new_eval = Chess_Lib.get_eval_value(eval, mate)
    return [fen_tensor, new_eval, mate]

def main():
    print(0, datetime.datetime.now())
    hkp_converter = Half_KP_Converter()
    for split in ['train', 'val', 'test']:
        filename_in = os.path.join(DIRECTORY, split, FILE_NAME)
        filename_out = os.path.join(DIRECTORY, split, FILE_NAME_OUT)
        import csv

        # Open existing CSV file (f1) for reading
        with open(filename_in, 'r') as file_in:
            # Create a new CSV file (f2) for writing
            with open(filename_out, 'w', newline='') as file_out:
                # Create CSV reader and writer objects
                reader = csv.reader(file_in, delimiter=DELIMITER)
                writer = csv.writer(file_out, delimiter=DELIMITER)

                # Iterate over each row in f1
                for i, row in enumerate(reader, start=1):
                    try:
                        # Assuming some conversion on each element of the row
                        converted_row = convert_row(row, hkp_converter)

                        # Write the converted row to f2
                        #writer.writerow(converted_row)
                        if i % 100 == 0:
                            file_out.flush()
                            print(i, datetime.datetime.now())
                    except Exception as e:
                        print(f"Exception: {e}")
                        print(f"Filename: {filename_in}")
                        print(f"Index: {i}")
                        print(f"Row: {row}")
                        print("Traceback:")
                        traceback.print_exc()
                        raise SystemExit

        print("Conversion and writing completed.")

if __name__ == "__main__":
    main()

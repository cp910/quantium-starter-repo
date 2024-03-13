

import csv
import os

DIRECTORY = "data"
OUTPUT_FILE = "formatted_data.csv"

with open(OUTPUT_FILE, "w") as output_file:
    writer = csv.writer(output_file)

    header = ["sales", "date", "region"]
    writer.writerow(header)

    for file_name in os.listdir(DIRECTORY):
        with open(f"{DIRECTORY}/{file_name}", "r") as input_file:
            reader = csv.reader(input_file)

            row_index = 0
            for input_row in reader:
                if row_index > 0:
                    product = input_row[0]
                    raw_price = input_row[1]
                    quantity = input_row[2]
                    transaction_date = input_row[3]
                    region = input_row[4]

                    if product == "pink morsel":
                        price = float(raw_price[1:])
                        sale = price * int(quantity)

                        output_row = [sale, transaction_date, region]
                        writer.writerow(output_row)
                row_index += 1
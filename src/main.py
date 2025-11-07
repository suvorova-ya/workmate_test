import argparse
import csv
from statistics import fmean
from tabulate import tabulate

def parser_csv_report():

    parser = argparse.ArgumentParser("parser csv files")
    parser.add_argument("--files", nargs="+", required=True, help="csv files can be miltiple files")
    parser.add_argument("--report", required=True, help="report name average-rating.csv")

    args = parser.parse_args()

    report = {}
    for filename in args.files:
        try:
            with open(filename, encoding="utf-8") as file:
                table = csv.DictReader(file)
                for row in table:
                    report.setdefault(row['brand'], []).append(float(row['rating']))
        except FileNotFoundError:
            raise FileNotFoundError("File not find")

    report.update({brand: round(fmean(rating), 2) for brand, rating in report.items()})
    output_report = args.report if args.report.endswith('csv') else args.report + ".csv"

    # Записываем отсортированный отчет
    with open(output_report, 'w', encoding="utf-8", newline="") as f:
        output_file = csv.writer(f)
        for brand, rating in sorted(report.items()):
            output_file.writerow([brand, rating])

    # выводим отчет в консоль
    try:
        with open("average-rating.csv", encoding="utf-8") as f:
            report = csv.reader(f)
            print(tabulate(report, headers=["brand", "rating"], tablefmt="pretty"))
    except FileNotFoundError:
        print("File 'average-rating.csv' not find")



if __name__ == "__main__":
    parser_csv_report()
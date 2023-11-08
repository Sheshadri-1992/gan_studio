import sys
import logging

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


class StockReport:

    def __init__(self):
        self.symbol_dict = {}

    def create_report(self, arg_filename):
        with open(arg_filename, 'r') as my_stock_report:
            stock_record_lines = my_stock_report.readlines()

            for stock_record in stock_record_lines[1:]:
                print(stock_record.strip())


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage : python stock_buy_sell.py <path_to_stock_record.csv>")
        exit(0)

    stock_obj = StockReport()
    stock_obj.create_report(sys.argv[1])

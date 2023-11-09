import sys
import logging
import time
import queue

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', level=logging.DEBUG)


class StockReport:

    def __init__(self):
        self.symbol_dict = {}
        self.output_record = []

    def print_report(self):
        final_value = 0.0
        print("OPEN_TIME, CLOSE_TIME, SYMBOL, QUANTITY, PNL, OPEN_SIDE, CLOSE_SIDE, OPEN_PRICE, CLOSE_PRICE")
        for record in self.output_record:
            print(record)
            final_value = final_value + float(record.split(",")[4])

        print(final_value)

    def match_symbol_pair(self, arg_stock_record: list[str]):
        arg_symbol = arg_stock_record[1]
        if arg_symbol not in self.symbol_dict:
            return

        arg_reduce_qty = int(arg_stock_record[4])

        while self.symbol_dict[arg_symbol].qsize() != 0:
            record = self.symbol_dict[arg_symbol].get()
            qty_to_reduce = min(record[2], arg_reduce_qty)

            record[2] = record[2] - qty_to_reduce
            pnl = round((float(arg_stock_record[3]) - float(record[1])) * arg_reduce_qty, 2)
            arg_reduce_qty = arg_reduce_qty - qty_to_reduce

            output_record_string = (str(record[0]) + "," + arg_stock_record[0] + "," +
                                    arg_symbol + "," + arg_stock_record[4] + "," + str(pnl) + "," +
                                    "B" + "," + "S" + "," + str(record[1]) + "," +
                                    arg_stock_record[3])
            self.output_record.append(output_record_string)

            '''
            If stock quantities still remain then adding the record back
            '''
            if record[2] > 0:
                self.symbol_dict[arg_symbol].put(record)

            if arg_reduce_qty <= 0:
                break

        '''
        Flipping the inventory i.e buying when all opening trades are over
        '''
        if arg_reduce_qty > 0:
            self.symbol_dict[arg_symbol].put([arg_stock_record[0], arg_stock_record[3], arg_reduce_qty])


    def create_report(self, arg_filename: str):
        with open(arg_filename, 'r') as my_stock_report:
            stock_record_lines = my_stock_report.readlines()

            for stock_record in stock_record_lines[1:]:
                stock_record = stock_record.strip().split(",")

                timestamp = int(stock_record[0])
                symbol = stock_record[1]
                side = stock_record[2]
                price = float(stock_record[3])
                qty = int(stock_record[4])

                if symbol not in self.symbol_dict:
                    self.symbol_dict[symbol] = queue.Queue()
                    self.symbol_dict[symbol].put([timestamp, price, qty])
                else:
                    if side == "B":
                        self.symbol_dict[symbol].put([timestamp, price, qty])
                    if side == "S":
                        self.match_symbol_pair(stock_record)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage : python stock_buy_sell.py <path_to_stock_record.csv>")
        exit(0)

    start_time = time.time()
    stock_obj = StockReport()
    stock_obj.create_report(sys.argv[1])
    stock_obj.print_report()
    end_time = time.time()
    total_time = (end_time - start_time)
    # print("Total time ", total_time)

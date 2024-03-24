from boc_spider import BOCSpider
from datetime import datetime
from confs import *
import argparse


def check_params(date_str, currency_abbr):
    try:
        datetime.strptime(date_str, "%Y%m%d")
    except AssertionError:
        raise RuntimeError("输入的日期格式有误！")
    if currency_abbr not in ABBR2ZH.keys():
        raise RuntimeError("输入的币种ABBR有误！")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Get currency value for a specific date.")
    parser.add_argument("date", help="Date in YYYYMMDD format")
    parser.add_argument("currency", help="Currency abbreviation")
    args = parser.parse_args()

    check_params(args.date, args.currency)

    spider = BOCSpider()
    res = spider.get_value_with_date_name(args.date, ABBR2ZH[args.currency])
    print(res)


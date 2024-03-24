from confs import *
from boc_spider import BOCSpider

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time

if __name__ == '__main__':
    # name_list = BOCSpider(BOC_MAIN_URL).get_currency_name()
    # name_list = name_list[1:]
    # name_list.sort()
    # print(name_list, len(name_list))
    # res = {}
    #
    # chrome_options = Options()
    # chrome_options.add_experimental_option('useAutomationExtension', False)
    # chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
    # chrome_options.add_argument('--headless')
    # dict_browser = webdriver.Chrome(options=chrome_options)
    # dict_browser.get(ABBR_URL)
    #
    # tables = dict_browser.find_elements(by=By.XPATH, value="/html/body/main/div/table/tbody/tr[2]/td/table")
    #
    # for table in tables:
    #     rows = table.find_elements(by=By.XPATH, value="tbody/tr")
    #     # print(len(rows))
    #     for row in rows[2:]:
    #         tds = row.find_elements(by=By.XPATH, value="td")
    #         # print(len(tds))
    #         if tds[1].text in name_list:
    #             res[tds[1].text] = tds[-2].text
    #         elif tds[2].text in name_list:
    #             res[tds[1].text] = tds[-2].text
    #
    # print(sorted(res.keys()))
    # for name in name_list:
    #     if name not in res.keys():
    #         print(name)
    for k,v in ZH2ABBR.items():
        print(f"'{v}': '{k}', ")
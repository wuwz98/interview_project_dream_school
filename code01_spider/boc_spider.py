import os.path
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from datetime import datetime
import traceback
import pandas as pd
from confs import *


class BOCSpider:
    def __init__(self, url=BOC_MAIN_URL):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
        self.url = url
        # self.start = start
        # self.end = end
        chrome_options = Options()
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        chrome_options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=chrome_options)

    # for testing
    def get_main_page(self):
        self.browser.get(self.url)
        self.browser.implicitly_wait(IMPLICITLY_WAIT_SEC)
        items = self.browser.find_elements(by=By.XPATH, value=r"/html/body/div/div[5]/div[1]/div[2]/table/tbody/tr")
        print(f"total lenght: {len(items)}")
        header = items[0].find_elements(by=By.XPATH, value=r"th")
        for head in header:
            print(head.text)
        for item in items[:3]:
            td_list = item.find_elements(by=By.XPATH, value=r"td")
            for td in td_list:
                print(td.text)

    # for preprocessing
    def _get_currency_name(self):
        self.browser.get(self.url)
        options = self.browser.find_elements(by=By.XPATH, value=r"/html/body/div/div[5]/div[1]/div[2]/div/form/div/table/tbody/tr/td[6]/select")
        name_list = []
        for option in options:
            currency_names = option.find_elements(by=By.XPATH, value=r"option")
            for name in currency_names:
                name_list.append(name.text)
        self.browser.get(ABBR_URL)
        return name_list

    def get_value_with_date_name(self, date, currency_name):
        def _get_value_list():
            res = []
            rows = self.browser.find_elements(by=By.XPATH, value='/html/body/div/div[4]/table/tbody/tr')
            heads = [_.text for _ in rows[0].find_elements(by=By.XPATH, value=r'th')]
            print(heads)

            for row in rows[1:]:
                tmp = {}
                vals = [_.text for _ in row.find_elements(by=By.XPATH, value=r'td')]
                if len(vals) == 1 and vals[0] == " ":
                    break
                assert len(vals) == len(heads)
                for i, head in enumerate(heads):
                    tmp[head] = vals[i]
                res.append(tmp)
            return res

        def _write_to_dir(date, currency_name):
            os.makedirs(f"{WRITE_DIR}/{date}/{ZH2ABBR[currency_name]}", exist_ok=True)
            clean_df.to_csv(f"{WRITE_DIR}/{date}/{ZH2ABBR[currency_name]}/result.txt", index=False)

        try:
            self.browser.get(self.url)
            self.browser.implicitly_wait(IMPLICITLY_WAIT_SEC)
            start_slot = self.browser.find_element(by=By.XPATH,
                                                   value=r'/html/body/div/div[5]/div[1]/div[2]/div/form/div/table/tbody/tr/td[2]/div/input')
            end_slot = self.browser.find_element(by=By.XPATH,
                                                 value=r'/html/body/div/div[5]/div[1]/div[2]/div/form/div/table/tbody/tr/td[4]/div/input')
            currency_name_slot = Select(self.browser.find_element(by=By.XPATH,
                                                                  value=r'/html/body/div/div[5]/div[1]/div[2]/div/form/div/table/tbody/tr/td[6]/select'))
            search_button = self.browser.find_element(by=By.XPATH,
                                                      value=r'/html/body/div/div[5]/div[1]/div[2]/div/form/div/table/tbody/tr/td[7]/input')
            start_slot.send_keys(date)
            end_slot.send_keys(date)
            currency_name_slot.select_by_value(currency_name)
            search_button.click()
        except Exception as e:
            traceback.print_exc()
            raise RuntimeError(f"数据查询失败！{e}")

        self.browser.implicitly_wait(IMPLICITLY_WAIT_SEC)
        try:
            res_list = _get_value_list()
        except Exception as e:
            traceback.print_exc()
            raise RuntimeError(f"解析数据查询页失败！{e}")

        try:
            res_df = pd.DataFrame(res_list)
            res_df['datetime'] = pd.to_datetime(res_df['发布时间'], format='%Y.%m.%d %H:%M:%S')
            sorted_df = res_df.sort_values(by='datetime')
            clean_df = sorted_df[sorted_df['现汇卖出价'].notna() & (sorted_df['现汇卖出价'] != '')]
            clean_df = clean_df[
                ['货币名称', '现汇买入价', '现钞买入价', '现汇卖出价', '现钞卖出价', '中行折算价', '发布时间']]
            _write_to_dir(date, currency_name)

            if len(clean_df) > 0:
                return clean_df.loc[0, '现汇卖出价']
            else:
                return "value_not_found!"
        except Exception as e:
            traceback.print_exc()
            raise RuntimeError(f"解析数据结果失败！{e}")

import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import csv


def get_browser(url):
    # 不要打开浏览器
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sanbox')

    # 创建WebDriver对象
    browser = webdriver.Chrome()
    # 调用WebDriver对象的get()方法发起请求
    browser.get(url)
    return browser


def has_key(paper_name, keys):
    for key in keys:
        if paper_name.lower().find(key.lower()) != -1:
            return True
    return False


def write_to_file(content, file):
    # 数据的存储文件，可能比较费时
    if os.path.exists(file):
        os.remove(file)
    else:
        f = open(file, "a")
        print(content, file=f)
        f.close()


def download_data(browser, save_file, paper_src, type, keys):
    """
    Args:
        browser:
        save_file:
        paper_src: 论文出处，如CVPR
        type: conference or journal
        keys: 关键字
    """

    start_time = time.time()
    paper_num = 0
    try:
        if type == "C":
            lists = browser.find_elements(By.CLASS_NAME, value="entry.inproceedings")
        else:
            lists = browser.find_elements(By.CLASS_NAME, value="entry.article")

        for li in lists:
            paper_name = li.find_element(By.CLASS_NAME, value="title")
            if has_key(paper_name.text, keys):
                paper_num += 1
                write_to_file(paper_src + "," + paper_name.text, save_file)

    except Exception as e:
        print(e)
    finally:
        end_time = time.time()
        time_used = end_time - start_time
        print(f"Search in {paper_src}, get paper number {paper_num},  time used: {time_used:.4}s.")
        browser.refresh()


def get_url_entity(file):
    entity_list = []
    with open(file, mode='r') as f:
        reader = csv.reader(f)
        entity_list.append((rows[0], rows[1], rows[2]) for rows in reader)

    return entity_list


if __name__ == '__main__':
    urls = get_url_entity("./A_paper_sets.csv")
    keys = ["contrastive"]

    for paper_src, paper_url, type in urls:
        download_data(get_browser(paper_url), "./papers.csv", paper_src, type, keys)

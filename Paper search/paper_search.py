import time
import os
import requests
from bs4 import BeautifulSoup


def has_key(paper_name, keys, logic="and"):
    for key in keys:
        if logic == "and":
            for k in key:
                if paper_name.lower().find(k.lower()) == -1:
                    return False
            return True
        # else:
        #     for k in key:
        #         if paper_name.lower().find(k.lower()) != -1:
        #             return True

            # return False


def write_to_file(content, file):
    # 数据的存储文件，可能比较费时
    f = open(file, "a+")
    print(content, file=f)
    f.close()


def get_data(url, paper_src, type, keys, logic):
    """
    use beautifulsoup to parse data.
    """

    start_time = time.time()

    page = requests.get(url).text
    soup = BeautifulSoup(page, "html.parser")
    if type == "C":
        lists = soup.find_all(name="li", attrs={"class": "entry inproceedings"})
    else:
        lists = soup.find_all(name="li", attrs={"class": "entry article"})

    paper_num = 0
    for li in lists:
        title = li.find(name="span", attrs={"class":"title"}).text
        if has_key(title, keys, logic):
            paper_num += 1
            write_to_file(paper_src + "," + title, save_file)

    end_time = time.time()
    time_used = end_time - start_time
    print(f"Search in {paper_src}, get {paper_num} papers,  time used: {time_used:.4}s.")


def get_url_entity(file):
    with open(file, mode='r') as f:
        lines = f.readlines()
        entity_list = [tuple(line.replace("\n", "").split(",")) for line in lines]

    return entity_list


if __name__ == '__main__':
    urls = get_url_entity("./A_paper_sets.csv")

    # keys dict
    task_dict = {
        # 'multi-modal-papers': ["multi view", "mutli-view", "multi modal", 'multi-modal'],
        # 'trustworthy-papers': ["trust", "reliable"],
        # 'recommend': ["recommend"]
        "multi-view-incomplete": [["incomplete"]]
    }

    for task, keys in task_dict.items():
        save_file = "./" + task + ".csv"
        if os.path.exists(save_file):
            os.remove(save_file)

        print(f" ---- Task: {task} ---- ")
        for paper_src, paper_url, type in urls:
            get_data(paper_url, paper_src, type, keys, "and")

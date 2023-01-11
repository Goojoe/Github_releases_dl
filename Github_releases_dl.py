"""
Python requests下载器
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple requests tqdm
"""
import json
import os
import urllib.request
import yaml

# 禁用SSL警告
import urllib3

urllib3.disable_warnings()


def read_yaml(filepath):
    with open(filepath, "rb") as file:
        config = yaml.safe_load(file)
    return config


def download_webpage(url, proxy=None):
    if proxy:
        proxy = urllib.request.ProxyHandler({"http": proxy})
        opener = urllib.request.build_opener(proxy)
        urllib.request.install_opener(opener)
    try:
        with urllib.request.urlopen(url) as url:
            s = url.read()
            html = s.decode("utf-8")
            return html
    except Exception as e:
        print(e)
        return None


def github(github_url, download_dir, proxy):
    github_url = "https://api.github.com/repos/" + github_url + "/releases/latest"
    github_json = download_webpage(github_url, proxy_url)
    github_data = json.loads(github_json)
    for i in github_data["assets"]:
        os.system(
            f'aria2c.exe -s8 -x64 -j20 --disk-cache=2048M --no-file-allocation-limit=50M --continue=true --remote-time=true --async-dns=true --async-dns-server=119.29.29.29,223.5.5.5,8.8.8.8,1.1.1.1 -d {download_dir} --all-proxy {proxy} {i["browser_download_url"]}'
        )


if __name__ == "__main__":
    config = read_yaml("config.yml")

    proxy_url = config["proxy_url"]
    download_dir = os.getcwd() + "\\" + config["download_dir"]
    
    if ":" in download_dir:
        download_dir = download_dir

    github_url = input("输入Github URL e.g.book-searcher-org/book-searcher:")
    github(
        github_url,
        download_dir,
        proxy_url,
    )
    print(f"====={github_url} 下载完成=====")

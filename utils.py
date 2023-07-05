# coding: utf-8
"""
@File    :   main.py
@Time    :   2023/05/05 18:46:35
@Author  :   lijc210@163.com
@Desc    :   
"""
import os
import socket
import boto3
import json
import requests
import logging
from tqdm import tqdm

S3_FILE_CONF = {
    "ACCESS_KEY": "a35e9409ca044e9696bee64b6a74955b",
    "SECRET_KEY": "b5a729970ad6925bd29edc6c5fa2f31960b9426896b0658654a7f113817f6c0e",
    "BUCKET_NAME": "file",
    "ENDPOINT_URL": "https://ea2399efdad8c26cba1f231fdeec938b.r2.cloudflarestorage.com",
}

# 连接s3
s3 = boto3.client(
    service_name="s3",
    aws_access_key_id=S3_FILE_CONF["ACCESS_KEY"],
    aws_secret_access_key=S3_FILE_CONF["SECRET_KEY"],
    endpoint_url=S3_FILE_CONF["ENDPOINT_URL"],
)


# 日志输出
fh = logging.FileHandler("publish.log", encoding="utf-8", mode="w")  # 用于输出到文件
hdr = logging.StreamHandler()  # 用于输出到控制台
logging.basicConfig(
    level=logging.INFO,  # 控制台打印的日志级别
    handlers=[fh, hdr],
    format="[%(asctime)s] %(levelname)s %(filename)s[%(lineno)d]: %(message)s"
    # 日志格式
)

if socket.gethostname() == "SHBGDZ05373":
    http, https = "http://172.17.15.93:7890", "http://172.17.15.93:7890"
else:
    http, https = "http://127.0.0.1:7890", "http://127.0.0.1:7890"
proxies = {"http": http, "https": https}


    
def put_object(url, key):
    logging.info("开始上传："+url)
    
    headers = {
        "Authorization": "Bearer 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",
        "Accept": "application/octet-stream",
        'X-GitHub-Api-Version':'2022-11-28'
    }

    response = requests.get(url, proxies=proxies, headers=headers, stream=True)
    # print(response.text)
    
    if response.status_code == 200:
        total_size = int(response.headers.get("content-length", 0))
        block_size = 1 * 1024 * 1024  # 缓冲区大小1M
        progress_bar = tqdm(total=total_size, unit="iB", unit_scale=True)

        content = b""
        for data in response.iter_content(block_size):
            content += data
            progress_bar.update(len(data))
            
        s3.put_object(
                Body=content,
                Bucket="file",
                Key=key,
            )
        progress_bar.close()
    else:
        logging.error(str(response.status_code)+"\t"+response.text)


def upload_cf():
    """
    打包完，调用此接口，上传到cloudflares
    """
    url = "https://api.github.com/repos/lijc210/woo-app/releases/latest"

    payload = {}

    headers = {
        "Authorization": "Bearer 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",
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
    }

    response = requests.get(url, proxies=proxies, headers=headers, timeout=5, data=payload)
    # print(response.text)

    res_dict = response.json()
    body = res_dict["body"]
    tag_name = res_dict["tag_name"]
    assets = res_dict["assets"]
    published_at = res_dict["published_at"]
    asset_dict = {}
    for adict in assets:
        name = adict["name"]
        browser_download_url = adict["url"]
        if name.endswith("_x64_zh-CN.msi"):
            asset_dict["windows"] = browser_download_url
            put_object(browser_download_url, name)
        elif name.endswith("_x64.dmg"):
            asset_dict["darwin"] = browser_download_url
            put_object(browser_download_url, name)
        elif name.endswith("_amd64.deb"):
            asset_dict["linux"] = browser_download_url
            put_object(browser_download_url, name)
    data_dict = {}
    data_dict["body"] = body
    data_dict["tag_name"] = tag_name
    data_dict["published_at"] = published_at
    data_dict["assets"] = asset_dict
    with open("data_dict.json","w") as f:
        f.write(json.dumps(data_dict,ensure_ascii=False))
    return True

def updater(target, version):
    """
    返回tauri最新的包
    """
    res = {}
    if os.path.exists("data_dict.json"):
        with open("data_dict.json") as f:
            data_dict = json.loads(f.read())

        if "v"+version == data_dict["tag_name"]:
            
            if target.startswith("darwin"):
                url = data_dict["assets"]["darwin"]
            elif target.startswith("linux"):
                url = data_dict["assets"]["linux"]
            elif target.startswith("windows"):
                url = data_dict["assets"]["windows"]
            else:
                url = ""
            
            res = {
            "url": url,
            "version": version,
            "notes": data_dict["body"],
            "pub_date": data_dict["published_at"],
            "signature": ""
            }
    return res

if __name__ == '__main__':
    upload_cf()
    # res = updater()
    # print(res)
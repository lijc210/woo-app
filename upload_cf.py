# coding: utf-8
"""
@File    :   upload_cf.py
@Time    :   2023/05/05 18:46:35
@Author  :   lijc210@163.com
@Desc    :   
"""
import sys
import boto3
import json
import requests
import logging
from tqdm import tqdm
from collections import defaultdict


# 日志输出
hdr = logging.StreamHandler()  # 用于输出到控制台
logging.basicConfig(
    level=logging.INFO,  # 控制台打印的日志级别
    handlers=[hdr],
    format="[%(asctime)s] %(levelname)s %(filename)s[%(lineno)d]: %(message)s"
    # 日志格式
)


def put_object(url, key, s3, BUCKET_NAME):
    logging.info("开始上传：" + url)

    headers = {
        "Accept": "application/octet-stream",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    response = requests.get(url, headers=headers, stream=True)
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
            Bucket=BUCKET_NAME,
            Key=key,
        )
        progress_bar.close()
    else:
        logging.error(str(response.status_code) + "\t" + response.text)


def get_signature(url):
    headers = {
        "Accept": "application/octet-stream",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    response = requests.get(url, headers=headers, stream=True)
    # print(response.text)

    signature = ""
    if response.status_code == 200:
        signature = response.content.decode()
    else:
        logging.error(str(response.status_code) + "\t" + response.text)
    return signature


def upload_cf(ACCESS_KEY, SECRET_KEY):
    """
    打包完，调用此接口，上传到cloudflares
    """
    S3_FILE_CONF = {
        "ACCESS_KEY": ACCESS_KEY,
        "SECRET_KEY": SECRET_KEY,
        "BUCKET_NAME": "file",
        "ENDPOINT_URL": "https://ea2399efdad8c26cba1f231fdeec938b.r2.cloudflarestorage.com",
    }

    BUCKET_NAME = S3_FILE_CONF["BUCKET_NAME"]

    # 连接s3
    s3 = boto3.client(
        service_name="s3",
        aws_access_key_id=S3_FILE_CONF["ACCESS_KEY"],
        aws_secret_access_key=S3_FILE_CONF["SECRET_KEY"],
        endpoint_url=S3_FILE_CONF["ENDPOINT_URL"],
    )

    url = "https://api.github.com/repos/lijc210/wooapp/releases/latest"

    payload = {}

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Content-Type": "application/json",
    }

    response = requests.get(url, headers=headers, timeout=5, data=payload)
    # print(response.text)

    res_dict = response.json()
    body = res_dict["body"]
    tag_name = res_dict["tag_name"]
    assets = res_dict["assets"]
    published_at = res_dict["published_at"]
    asset_dict = defaultdict(dict)
    for adict in assets:
        name = adict["name"]
        url = adict["url"]
        # signature
        if name.endswith("_x64_zh-CN.msi.zip.sig"):
            signature = get_signature(url)
            asset_dict["windows"]["signature"] = signature
        elif name.endswith("_x64.app.tar.gz.sig"):
            signature = get_signature(url)
            asset_dict["darwin"]["signature"] = signature
        elif name.endswith("_amd64.AppImage.tar.gz.sig"):
            signature = get_signature(url)
            asset_dict["linux"]["signature"] = signature
        # url
        if name.endswith("_x64_zh-CN.msi.zip"):
            asset_dict["windows"]["url"] = f"https://file.cizai.io/{name}"
            put_object(url, name, s3, BUCKET_NAME)
        elif name.endswith("_x64.app.tar.gz"):
            asset_dict["darwin"]["url"] = f"https://file.cizai.io/{name}"
            put_object(url, name, s3, BUCKET_NAME)
        elif name.endswith("_amd64.AppImage.tar.gz"):
            asset_dict["linux"]["url"] = f"https://file.cizai.io/{name}"
            put_object(url, name, s3, BUCKET_NAME)

    data_dict = {}
    data_dict["body"] = body
    data_dict["tag_name"] = tag_name
    data_dict["published_at"] = published_at
    data_dict["assets"] = dict(asset_dict)

    # print(data_dict)

    # 版本上传到cloudflares
    s3.put_object(
        Body=json.dumps(data_dict, ensure_ascii=False),
        Bucket=BUCKET_NAME,
        Key="wooapp.json",
    )
    return True


if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("缺少参数")
    else:
        ACCESS_KEY = sys.argv[1]
        SECRET_KEY = sys.argv[2]
        upload_cf(ACCESS_KEY, SECRET_KEY)

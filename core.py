#!/usr/bin/env python
# coding=utf-8

import os
import hashlib
import logging

import trio
import asks

asks.init("trio")


URLS_DATA = "data.txt"
PICS_FILENAME_LENGTH = 16
PICS_EXT = ".jpg"
PICS_DIR = "pics"
# 每次请求延迟（秒）
DELAY_TIME = 0.35
# 最大并发数，尽量不要设置得过大
MAX_CONCURRENCY = 64
# 最多重试次数
MAX_RETRY = 5
# 队列容量
MAX_QSIZE = 180000
# 日志等级
LOG_LEVEL = logging.INFO
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
)

Q = trio.Queue(MAX_QSIZE)


def get_logger():
    """
    获取 logger 实例
    """
    formatter = logging.Formatter("%(asctime)s - %(message)s")
    logger = logging.getLogger("monitor")
    logger.setLevel(LOG_LEVEL)

    sh = logging.StreamHandler()
    sh.setFormatter(formatter)
    logger.addHandler(sh)
    return logger


LOGGER = get_logger()


def get_headers(url):
    """
    根据对应 url 返回 headers
    """
    if url.startswith("http://i.meizitu.net/"):
        return {"User-Agent": USER_AGENT, "Referer": "http://www.mzitu.com"}
    if url.startswith("http://img.mmjpg.com/"):
        return {"User-Agent": USER_AGENT, "Referer": "http://www.mmjpg.com"}


def prepare():
    """
    准备工作
    """
    # 如果文件夹不存在，则创建文件夹
    if not os.path.exists(PICS_DIR):
        os.mkdir(PICS_DIR)

    # 获取所有 url
    with open(URLS_DATA, "r", encoding="utf8") as f:
        for u in f.readlines():
            Q.put_nowait((u.strip(), MAX_RETRY))


async def download(sem, url):
    """
    异步获取请求数据

    :param sem: Semaphore 实例
    :param url: 请求链接
    """
    # 实际 url 以及 重试次数
    url, rt = url
    try:
        # 使用 hash 构建文件名，唯一对应 hash 值
        file_name = hashlib.sha224(url.encode("utf8")).hexdigest()[
            :PICS_FILENAME_LENGTH
        ] + PICS_EXT
        file_path = os.path.join(PICS_DIR, file_name)
        if os.path.exists(file_path):
            LOGGER.info("Ignore: {} has existed".format(file_path))
            return
        await trio.sleep(DELAY_TIME)
        async with sem:
            resp = await asks.get(url, headers=get_headers(url))
            img = resp.content
            async with await trio.open_file(file_path, mode="ab") as f:
                await f.write(img)
                LOGGER.info("Save: {}".format(file_path))
    except Exception as e:
        if rt > 0:
            await Q.put((url, rt - 1))
            LOGGER.error("Url: {} download failed".format(url))
            LOGGER.error(e)


async def run():
    """
    运行主函数
    """
    # 创建可复用 Semaphore 实例，减少开销
    sem = trio.Semaphore(MAX_CONCURRENCY)
    async with trio.open_nursery() as nursery:
        while not Q.empty():
            nursery.start_soon(download, sem, await Q.get())


if __name__ == "__main__":
    prepare()
    trio.run(run)

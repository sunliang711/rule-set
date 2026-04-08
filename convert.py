#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import logging
import re


def setup_log(logfile, log_level):
    LOG_LEVEL = {'debug': logging.DEBUG , 'info': logging.INFO, 'warn': logging.WARN, 'error': logging.ERROR, 'fatal': logging.FATAL}
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%Y/%m/%d %H:%M:%S"

    config = {
        'level': LOG_LEVEL.get(log_level, logging.INFO),
        'format': LOG_FORMAT,
        'datefmt': DATE_FORMAT,
    }
    if logfile:
        config['filename'] = logfile

    logging.basicConfig(**config)

def convert_content(content):
    # 保持与 convert.sh 一致，直接按文本规则转换，避免 YAML 解析丢失注释
    content = re.sub(r'^payload', '# payload', content, flags=re.MULTILINE)
    content = re.sub(r'^\s+-\s+(.+)', r'\1', content, flags=re.MULTILINE)
    content = re.sub(r'^\s+', '', content, flags=re.MULTILINE)
    return content

def convert1(dir,destDir):
    os.makedirs(destDir, exist_ok=True)

    for file in sorted(os.listdir(dir)):
        if not file.endswith('.yaml'):
            continue

        filename = os.path.join(dir, file)
        if not os.path.isfile(filename):
            continue

        with open(filename,'r', encoding='utf-8') as f:
            content = convert_content(f.read())
            destFile = os.path.join(destDir,os.path.splitext(file)[0]) + ".list"
            logging.info("converting %s to %s", filename, destFile)
            with open(destFile,'w', encoding='utf-8') as out:
                out.write(content)

def main():
    parser = argparse.ArgumentParser(description="get opensea collection floor price")
    parser.add_argument('--log-level', help='log level, default level: info', choices=['debug', 'info', 'warn', 'error', 'fatal'])
    parser.add_argument('--log-file', help = 'log file')
    args = parser.parse_args()

    setup_log(args.log_file,args.log_level)

    convert1("clash","surge")


if __name__ == '__main__':
    main()


#### no extra dependency required
#### python3 convert.py

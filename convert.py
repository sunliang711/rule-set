#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import argparse
import logging
import yaml


def setup_log(logfile, log_level):
    LOG_LEVEL = {'debug': logging.DEBUG , 'info': logging.INFO, 'warn': logging.WARN, 'error': logging.ERROR, 'fatal': logging.FATAL}
    LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
    DATE_FORMAT = "%Y/%m/%d %H:%M:%S"

    logging.basicConfig(filename=logfile, level=LOG_LEVEL.get(log_level, logging.ERROR), format=LOG_FORMAT, datefmt=DATE_FORMAT)

def convert1(dir,destDir):
    for file in os.listdir(dir):
        filename = os.path.join(dir, file)
        print("filename:{}".format(filename))
        with open(filename,'r') as f:
            yml = yaml.safe_load(f)
            destFile = os.path.join(destDir,os.path.splitext(file)[0]) + ".list"
            print("dest file: {}".format(destFile))
            with open(destFile,'w') as out:
                for item in yml['payload']:
                    out.write("{}\n".format(item))

def main():
    parser = argparse.ArgumentParser(description="get opensea collection floor price")
    parser.add_argument('--log-level', help='log level,default level: warn', choices=['debug', 'info', 'warn', 'error', 'fatal'])
    parser.add_argument('--log-file', help = 'log file')
    args = parser.parse_args()

    setup_log(args.log_file,args.log_level)

    convert1("clash","surge")


if __name__ == '__main__':
    main()


#### pip3 install pyyaml
#### python3 convert.py

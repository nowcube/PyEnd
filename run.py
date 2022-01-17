#!/usr/bin/python
# -*- coding: UTF-8 -*-
from scrapy import cmdline
# import uuid
import os

# id = str(uuid.uuid4()).replace('-', '')

# cmdline.execute("scrapy crawl hot -o result_{0}.json".format(id).split())

if os.path.exists('result.json'):
    os.remove('result.json')
    cmdline.execute("scrapy crawl hot -o result.json".split())
else:
    cmdline.execute("scrapy crawl hot -o result.json".split())
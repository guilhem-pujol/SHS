#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import unicodedata

def sanitize(content):
    content = ''.join(c for c in unicodedata.normalize('NFD', content) if unicodedata.category(c) != 'Mn')
    content = content.lower()
    content = content.replace(u'ς', u'σ')
    content = content.replace('\r\n', '\n')
    return content

def getFile(filename):
    f = open(filename, 'r')
    content = f.read().decode('utf-8')
    return sanitize(content)

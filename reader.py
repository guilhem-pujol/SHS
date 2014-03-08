#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import unicodedata
from debug import toASCII
from textstructure import *

class InputError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

def sanitize(content):
    content = ''.join(c for c in unicodedata.normalize('NFD', content) if unicodedata.category(c) != 'Mn')
    content = content.lower()
    content = content.replace(u'ς', u'σ')
    content = content.replace('\r\n', '\n')
    return content

def getFile(filename):
    f = open(filename, 'r')
    content = f.read().decode('utf-8')
    content = sanitize(content)
    
    result = Text()
    for line in content.split("\n"):
        verse = buildVerseFromLine(line)
        if verse != None:
            result.addVerse(verse)
    
    return result
    
def buildVerseFromLine(line):
    line = line.replace("|", "-")
    lineData = line.split("\t")
    if len(lineData) < 5: return None
    (metrics, syllables) = (lineData[3], lineData[4].split("-"))
    
    pos = 0
    feet = []
    for metricData in metrics:
        if metricData == "d":
            expected = [Syllable.long_syl, Syllable.short_syl, Syllable.short_syl]
            metric = Foot.dactyl
        elif metricData == "s":
            expected = [Syllable.long_syl, Syllable.long_syl]
            metric = Foot.spondee
        else:
            raise InputError("Unknown metric : \""+metricData+"\"")
        
        if len(syllables) < pos + len(expected):
            raise InputError("Too few syllables to match given metric")
        
        feet.append(Foot(
            [Syllable(syllables[pos+i], x) for (i,x) in enumerate(expected)],
            metric))
        
        pos += len(expected)
        
    return Verse(feet)
        

#!/usr/bin/env python2
# -*- coding: utf-8 -

from debug import toASCII
from collections import defaultdict

class StructureError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Text():
    def __init__(self, name):
        self.name = name
        self.verses = []
        self.numMatch = 0
        
        self.begin = 0
        self.end = 0
        
    def addVerse(self, verse):
        if verse.__class__ == Verse:
            self.verses.append(verse)
        else:
            raise StructureError("Text.addVerse: argument must be a Verse")
            
        self.begin = 0
        self.end = len(self.verses) - 1
    
    def __str__(self):
        return "\n".join([str(v) for v in self.verses])
        
    def text(self, linear = False):
        if linear: return " ".join([v.text() for v in self.verses])
        else: return "\n".join([v.text(True) for v in self.verses])

    def html(self, lines = False):
        res = ''
        for i in range(self.begin, self.end + 1):
            if i > self.begin:
                res += '<br />'
            if lines:
                res += str(i+1) + ' '
            v = self.verses[i]
            if v.numMatch > 0:
                res += '<span style="background-color: #ffff82">'
            res += v.html()
            if v.numMatch > 0:
                res += '</span>'
        return res
        
    def search(self, pattern):
        self.numMatch = 0
        self.matchByPos = defaultdict(int)
        
        for i in range(self.begin, self.end + 1):
            v = self.verses[i]
            self.numMatch += v.search(pattern)
            for pos, n in v.matchByPos.iteritems():
                self.matchByPos[pos] += n

        return self.numMatch
        

class Verse():
    def __init__(self, name, feet):
        self.name = name
        self.feet = []
        for f in feet:
            if f.__class__ == Foot:
                self.feet.append(f)
            else:
                raise StructureError("Verse(): argument must be a Foot list")
        self.numMatch = 0
        self.matchByPos = None

    def __str__(self):
        return " | ".join([str(f) for f in self.feet])
        
    def text(self, linear = False):
        if linear: return " ".join([f.text() for f in self.feet])
        else: return " | ".join([f.text(True) for f in self.feet])

    def html(self):
        return ' | '.join([foot.html() for foot in self.feet])
        
    def search(self, pattern):
        self.numMatch = sum([f.search(pattern) for f in self.feet])
        
        self.matchByPos = defaultdict(int)
        for i, f in enumerate(self.feet):
            if f.metric == Foot.spondee:
                self.matchByPos[str(i + 1)] = f.syllables[0].numMatch
                self.matchByPos[str(i + 1)+"0"] = f.syllables[1].numMatch
            elif f.metric == Foot.dactyl:
                self.matchByPos[str(i + 1)] = f.syllables[0].numMatch
                self.matchByPos[str(i + 1)+"1"] = f.syllables[1].numMatch
                self.matchByPos[str(i + 1)+"2"] = f.syllables[2].numMatch
        
        return self.numMatch
        
class Foot():
    dactyl = 0
    spondee = 1
    
    def __init__(self, syllables, metric):
        if metric == Foot.dactyl:
            if len(syllables) != 3:
                raise StructureError("Foot(): a dactyl needs 3 Syllables")
        elif metric == Foot.spondee:
            if len(syllables) != 2:
                raise StructureError("Foot(): a spondee needs 2 Syllables")
        else:
            raise StructureError("Foot(): unknown metric")
  
        self.syllables = []      
        self.metric = metric
        
        for s in syllables:
            if s.__class__ == Syllable:
                self.syllables.append(s)
            else:
                raise StructureError("Foot(): argument must be a Syllable list")
                
        self.numMatch = 0

    def __str__(self):
        return " - ".join([str(s) for s in self.syllables])
        
    def text(self, linear = False):
        if linear: return " ".join([s.text for s in self.syllables])
        else: return " - ".join([s.text for s in self.syllables])

    def html(self):
      return ' - '.join([syllable.html() for syllable in self.syllables])
        
    def search(self, pattern):
        self.matchByPos = [s.search(pattern) for s in self.syllables]
        self.numMatch = sum(self.matchByPos)
        return self.numMatch
    
class Syllable():
    long_syl = 0
    short_syl = 1
    
    def __init__(self, text, syl_type):
        if syl_type != Syllable.long_syl and syl_type != Syllable.short_syl:
            raise StructureError("Syllable(): unknown type")
        
        self.text = text    
        self.syl_type = syl_type
        self.numMatch = 0

    def __str__(self):
        return toASCII(self.text)
        
    def text(self):
        return self.text

    def html(self):
      cols = []
      if self.numMatch > 0:
        cols.append('<span style="color: #ff6022">')
      cols.append(self.text)
      if self.numMatch > 0:
        cols.append('</span>')
      return ''.join(cols)
        
    def search(self, pattern):
        self.numMatch = 0
        for startPos in range(len(self.text) - len(pattern) + 1):
            isMatch = True
            for i in range(len(pattern)):
                if pattern[i] == 'C':
                    isMatch = not isVowel(self.text[startPos + i])
                elif pattern[i] == 'V':
                    isMatch = isVowel(self.text[startPos + i])
                else:
                    isMatch = (self.text[startPos + i] == pattern[i])
                
                if not isMatch: break
            
            if isMatch:
                self.numMatch += 1
        
        return self.numMatch
        
def isVowel(letter):
    return letter in [u'α', u'ε', u'ι', u'ο', u'υ', u'η', u'ω']

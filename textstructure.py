#!/usr/bin/env python2
# -*- coding: utf-8 -

from debug import toASCII

class StructureError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)

class Text():
    def __init__(self):
        self.verses = []
        self.numMatch = 0
        
    def addVerse(self, verse):
        if verse.__class__ == Verse:
            self.verses.append(verse)
        else:
            raise StructureError("Text.addVerse: argument must be a Verse")
    
    def __str__(self):
        return "\n".join([str(v) for v in self.verses])
        
    def text(self, linear = False):
        if linear: return " ".join([v.text() for v in self.verses])
        else: return "\n".join([v.text(True) for v in self.verses])
        
    def search(self, pattern):
        self.numMatch = sum([v.search(pattern) for v in self.verses])
        

class Verse():
    def __init__(self, feet):
        self.feet = []
        for f in feet:
            if f.__class__ == Foot:
                self.feet.append(f)
            else:
                raise StructureError("Verse(): argument must be a Foot list")
        self.numMatch = 0

    def __str__(self):
        return " | ".join([str(f) for f in self.feet])
        
    def text(self, linear = False):
        if linear: return " ".join([f.text() for f in self.feet])
        else: return " | ".join([f.text(true) for f in self.feet])
        
    def search(self, pattern):
        self.numMatch = sum([f.search(pattern) for f in self.feet])
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
        
    def search(self, pattern):
        self.numMatch = sum([s.search(pattern) for s in self.syllables])
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
        
    def search(self, pattern):
        self.numMatch = 0
        for startPos in range(len(self.text) - len(pattern) + 1):
            isMatch = True
            for i in range(len(pattern)):
                if pattern[i] == 'C':
                    isMatch = not isVoyel(self.text[startPos + i])
                elif pattern[i] == 'V':
                    isMatch = isVoyel(self.text[startPos + i])
                else:
                    isMatch = (self.text[startPos + i] == pattern[i])
                
                if not isMatch: break
            
            if isMatch:
                self.numMatch += 1
        
        return self.numMatch
        
def isVoyel(letter):
    return letter in [u'α', u'ε', u'ι', u'ο', u'υ', u'η', u'ω']

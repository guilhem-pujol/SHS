#!/usr/bin/env python2
# -*- coding: utf-8 -

class StructureError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        repr(self.value)

class Text():
    def __init__(self):
        self.verses = []
        
    def addVerse(self, verse):
        if verse.__class__ == Verse:
            self.verses.append(verse)
        else:
            raise StructureError("Text.addVerse: argument must be a Verse")
    
    def __str__(self):
        return "\n".join([str(v) for v in self.verses])
        
    def text(self):
        return " ".join([v.text()] for v in self.verses)

class Verse():
    def __init__(self, feet):
        self.feet = []
        for f in feet:
            if f.__class__ == Foot:
                self.feet.append(f)
            else:
                raise StructureError("Verse(): argument must be a Foot list")

    def __str__(self):
        return " | ".join([str(f) for f in self.feet])
        
    def text(self):
        return " ".join([f.text()] for f in self.feet)
        
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

    def __str__(self):
        return " - ".join([str(s) for s in self.syllables])
        
    def text(self):
        return " ".join([s.text()] for s in self.syllables)
    
class Syllable():
    long_syl = 0
    short_syl = 1
    
    def __init__(self, text, syl_type):
        if syl_type != Syllable.long_syl and syl_type != Syllable.short_syl:
            raise StructureError("Syllable(): unknown type")
  
        self.text = text    
        self.syl_type = syl_type

    def __str__(self):
        return self.text
        
    def text(self):
        return str(self)

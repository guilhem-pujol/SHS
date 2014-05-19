#!/usr/bin/env python2
# -*- coding: utf-8 -

from debug import toASCII
from collections import defaultdict
from heapq import nlargest

class StructureError(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

class Text():
  allPos = ['1', '10', '11', '12',
            '2', '20', '21', '22',
            '3', '30', '31', '32',
            '4', '40', '41', '42',
            '5', '50', '51', '52',
            '6', '60']
  def __init__(self, name):
    self.name = name
    self.verses = []
    self.numMatch = 0

    self.begin = 0
    self.end = 0
    self.beginText = ''
    self.endText = ''

    self.pattern = ''

  def addVerse(self, verse):
    if verse.__class__ == Verse:
      self.verses.append(verse)
    else:
      raise StructureError('Text.addVerse: argument must be a Verse')
    self.resetRange()

  def __str__(self):
    return '\n'.join([str(v) for v in self.verses])

  def text(self, linear = False):
    if linear: return ' '.join([v.text() for v in self.verses])
    else: return '\n'.join([v.text(True) for v in self.verses])

  def search(self, pattern):
    if pattern == self.pattern:
      return self.numMatch
    self.pattern = pattern
    self.numMatch = 0
    self.matchByPos = defaultdict(int)

    for i in range(self.begin, self.end + 1):
      v = self.verses[i]
      self.numMatch += v.search(pattern)
      for pos, n in v.matchByPos.iteritems():
        self.matchByPos[pos] += n
    
    return self.numMatch

  def stats(self):
    res = [[], []]
    for idx in range(23):
      acc = (defaultdict(int), defaultdict(int))
      for i in range(self.begin, self.end + 1):
        v = self.verses[i]
        tmp = v.stats(idx)
        for k in range(2):
          for (p, r) in tmp[k].iteritems():
            acc[k][p] += r
      for k in range(2):
        l = acc[k].items()
        l = nlargest(10, l, key = lambda x: x[1])
        res[k].append([p for (p, _) in l])
    return res


  def result1(self):
    res = []
    for i in range(self.begin, self.end + 1):
      v = self.verses[i]
      res.append((v.name, v.numMatch))
    return res

  def result2(self):
    res = []
    for pos in Text.allPos:
      res.append((pos, self.matchByPos[pos]))
    return res

  def setRange(self, begin, end):
    vb = -1
    ve = -1
    for (i, v) in enumerate(self.verses):
      if v.name == begin:
        vb = i
      if v.name == end:
        ve = i
      if vb != -1 and ve != -1:
        break
    else:
      return False
    if vb > ve:
      return False
    self.begin = vb
    self.end = ve
    self.beginText = begin
    self.endText = end
    return True

  def resetRange(self):
    self.begin = 0
    self.end = len(self.verses) - 1
    self.beginText = self.verses[self.begin].name
    self.endText = self.verses[self.end].name

class Verse():
  def __init__(self, name, feet):
    self.name = name
    self.feet = []
    for f in feet:
      if f.__class__ == Foot:
        self.feet.append(f)
      else:
        raise StructureError('Verse(): argument must be a Foot list')
    self.numMatch = 0
    self.matchByPos = None

  def __str__(self):
    return ' | '.join([str(f) for f in self.feet])

  def text(self, linear = False):
    if linear: return ' '.join([f.text() for f in self.feet])
    else: return ' | '.join([f.text(True) for f in self.feet])

  def search(self, pattern):
    self.numMatch = sum([f.search(pattern) for f in self.feet])

    self.matchByPos = defaultdict(int)
    for i, f in enumerate(self.feet):
      if f.metric == Foot.spondee:
        self.matchByPos[str(i + 1)] = f.syllables[0].numMatch
        self.matchByPos[str(i + 1)+'0'] = f.syllables[1].numMatch
      elif f.metric == Foot.dactyl:
        self.matchByPos[str(i + 1)] = f.syllables[0].numMatch
        self.matchByPos[str(i + 1)+'1'] = f.syllables[1].numMatch
        self.matchByPos[str(i + 1)+'2'] = f.syllables[2].numMatch

    return self.numMatch

  def stats(self, idx):
    res = [defaultdict(int), defaultdict(int)]
    acc = []
    if idx == 0:
      for idx in range(22):
        f = self.feet[idx/4]
        acc.append(f.stats(idx%4))
    else:
      f = self.feet[(idx-1)/4]
      acc.append(f.stats((idx-1)%4))
    for tmp in acc:
      for k in range(2):
        for (p, r) in tmp[k].iteritems():
          res[k][p] += r
    return res

class Foot():
  dactyl = 0
  spondee = 1

  def __init__(self, syllables, metric):
    if metric == Foot.dactyl:
      if len(syllables) != 3:
        raise StructureError('Foot(): a dactyl needs 3 Syllables')
    elif metric == Foot.spondee:
      if len(syllables) != 2:
        raise StructureError('Foot(): a spondee needs 2 Syllables')
    else:
      raise StructureError('Foot(): unknown metric')

    self.syllables = []
    self.metric = metric

    for s in syllables:
      if s.__class__ == Syllable:
        self.syllables.append(s)
      else:
        raise StructureError('Foot(): argument must be a Syllable list')

    self.numMatch = 0

  def __str__(self):
    return ' - '.join([str(s) for s in self.syllables])

  def text(self, linear = False):
    if linear: return ' '.join([s.text for s in self.syllables])
    else: return ' - '.join([s.text for s in self.syllables])

  def search(self, pattern):
    self.matchByPos = [s.search(pattern) for s in self.syllables]
    self.numMatch = sum(self.matchByPos)
    return self.numMatch

  def stats(self, idx):
    if self.metric == Foot.dactyl and idx == 1:
      return (defaultdict(int), defaultdict(int))
    if self.metric == Foot.spondee and idx >= 2:
      return (defaultdict(int), defaultdict(int))
    idx = (idx+1)/2
    return self.syllables[idx].stats()

class Syllable():
  long_syl = 0
  short_syl = 1

  def __init__(self, text, syl_type):
    if syl_type != Syllable.long_syl and syl_type != Syllable.short_syl:
      raise StructureError('Syllable(): unknown type')

    self.text = text
    self.letters = filter(lambda c: not isSpecial(c), text)
    self.syl_type = syl_type
    self.numMatch = 0

  def __str__(self):
    return toASCII(self.text)

  def text(self):
    return self.text

  def search(self, pattern):
    self.numMatch = 0
    for startPos in range(len(self.letters) - len(pattern) + 1):
      isMatch = True
      for i in range(len(pattern)):
        if pattern[i] == 'C':
          isMatch = not isVowel(self.letters[startPos + i])
        elif pattern[i] == 'V':
          isMatch = isVowel(self.letters[startPos + i])
        else:
          isMatch = (self.letters[startPos + i] == pattern[i])

        if not isMatch: break

      if isMatch:
        self.numMatch += 1

    return self.numMatch

  def stats(self):
    res = (defaultdict(int), defaultdict(int))
    for startPos in range(len(self.letters)):
      for endPos in range(startPos, len(self.letters)):
        s = self.letters[startPos:endPos+1]
        res[0][s] += 1
        k = ''
        for c in s:
          if not isVowel(c):
            k += 'C'
          else:
            k += 'V'
        res[1][k] += 1
    return res

def isSpecial(letter):
  return ord(letter) in [32, 44, 46, 180, 59, 183]

def isVowel(letter):
  return letter in [u'α', u'ε', u'ι', u'ο', u'υ', u'η', u'ω']

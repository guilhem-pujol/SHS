#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import unicodedata
from collections import defaultdict
from collections import deque

### Auxiliary classes and functions

class Position:

  __slots__ = ['verse', 'foot', 'syllable', 'syllable_str']

  S0 = 0
  S1 = 1
  D0 = 2
  D1 = 3
  D2 = 4

  def __init__(self, verse, foot, syllable):
  self.verse = verse
  self.foot = foot
  self.syllable = syllable
  self.syllable_str = Position.syllable_to_str(foot, syllable)
  
  @staticmethod
  def syllable_to_str(foot, syllable):
  return str(foot+1) + (
    '0' if syllable == 1 else
    str(syllable - 2) if syllable > 2 else
    '')


def get_file(file):
  f = open(file, 'r')
  content = f.read().decode('utf-8')
  content = ''.join(c for c in unicodedata.normalize('NFD', content) if unicodedata.category(c) != 'Mn')
  content = content.lower()
  content = content.replace(u'ς', u'σ')
  content = content.replace('\r\n', '\n')
  return content

def return_file(file, out):
  f = open(file, 'w')
  for l in out:
  	f.write(l.encode('utf-8'))

metres = []
metres_inv = dict()
for i in range(32):
  m = bin(i)[2:]
  m = '0' * (5-len(m)) + m + '0'
  m = m.replace('0', 's').replace('1', 'd')
  metres.append(m)
  metres_inv[m] = i

### Get the input file

verses = [] # [(metre, feet)]

lines = get_file('in.txt').split('\n')
for l in lines:
  # <ignore> id <ignore> metric verse
  tabs = l.split('\t')
  if len(tabs) < 5:
  	continue
  
  text = tabs[4].split('-')
  text = [x for l in text for x in l.split('|')]
  feet = []
  idx = 0
  tabs[3] = tabs[3].encode('utf-8')
  for m in tabs[3]:
  	foot = []
  	# One long
  	foot.append(text[idx])
  	idx += 1
  	if m == 'd':
  		# Two short
  		foot.append(text[idx])
  		idx += 1
  		foot.append(text[idx])
  		idx += 1
  	else:
  		# One long
  		foot.append(text[idx])
  		idx += 1
  	feet.append(foot)
  if idx != len(text):
  	print 'Bad metre'
  verses.append((metres_inv[tabs[3]], feet))

### Collect positions for each n-gram and pattern

occ = [defaultdict(int) for k in range(3)] # Occurrences
pos = [defaultdict(list) for k in range(3)] # Positions
mixed_pos = defaultdict(list)
patterns_pos = defaultdict(list)
sums = [0]*3

def without_symbols(s):
  for c in s:
  if ord(c) in [32, 44, 46, 180, 59, 183]:
    return False
  return True

vowels = u'αειουηω'

def to_vc_pattern(s):
  res = u''
  for c in s:
  if c in vowels:
    res += 'v'
  else:
    res += 'c'
  return res

for (vid, (metre, feet)) in enumerate(verses):
  for (fid, foot) in enumerate(feet):
  if len(foot) == 2:
    sid = Position.S0 - 1
  else:
    sid = Position.D0 - 1
  for syllable in foot:
    sid += 1
    p = Position(vid, fid, sid)
    for k in range(4):
    for i in range(len(syllable) - k):
      s = syllable[i:i+k+1]
      if without_symbols(s):
      if k < 3:
        occ[k][s] += 1
        sums[k] += 1
        pos[k][s].append(p)
      mixed_pos[s].append(p)
    if without_symbols(syllable):
    pattern = to_vc_pattern(syllable)
    if u'v' in pattern:
      mixed_pos[pattern].append(p)
      patterns_pos[pattern].append(p)

### Statistical functions

def moving_verse(l, n):
  q = deque()
  nb = 0
  idx = 0
  res = []
  for vid in range(len(verses)):
  while idx < len(l) and l[idx].verse <= vid + n/2:
    q.append(l[idx].verse)
    nb += 1
    idx += 1
  while len(q) > 0 and q[0] < vid - n/2:
    q.popleft()
    nb -= 1
  res.append(nb)
  return res

def syllables(l):
  res = dict()
  for foot in range(6):
  for syllable in range(Position.S0, Position.D2+1):
    if foot == 5 and syllable >= Position.D0:
    continue
    res[Position.syllable_to_str(foot, syllable)] = 0

  for p in l:
  res[p.syllable_str] += 1

  return res

def moving_syllables(l, syllable_str, n):
  l = filter(lambda p: p.syllable_str == syllable_str, l)
  return moving_verse(l, n)


### We will work on the most frequent n-grams/patterns
### Below is the output t CSV format

most_frequent = []
for k in range(3):
  l = [(-v, k) for (k, v) in occ[k].items()]
  l.sort()
  most_frequent.append([k for (_, k) in l[:20]])

for (k, l) in enumerate(most_frequent):
  print 'Most frequent {}-grams'.format(k+1)
  print ','.join(l).encode('utf-8')

l = [(-len(p), k) for (k, p) in patterns_pos.items()]
l.sort()
sorted_patterns = [k for (_, k) in l]
print 'Patterns sorted by frequency'
print ','.join(sorted_patterns).encode('utf-8')
print

print 'For each 'interesting' n-grams and patterns, moving frequency and frequency per syllable'
print

todo = [x for sub in most_frequent for x in sub] + sorted_patterns
for k in todo:
  print k.encode('utf-8')
  print 'Moving frequency over 10 verses'
  for (i, nb) in enumerate(moving_verse(mixed_pos[k], 10)):
  print '{},{}'.format(i+1, nb)
  print 'Frequency per syllable'
  l = syllables(mixed_pos[k]).items()
  l.sort()
  for (s, nb) in l:
  print '{},{}'.format(s, nb)



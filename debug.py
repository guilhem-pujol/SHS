#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import string

greekChars = [u"ξ",  u"α", u"β", u"γ", u"δ", u"ε", u"ζ", u"η", u"θ", u"ι", u"κ", u"λ", u"μ", u"ν", u"ο", u"π", u"ρ", u"σ", u"ς", u"τ", u"υ", u"φ", u"χ", u"ψ", u"ω"]
asciiChars = [u"ks", u"a", u"b", u"g", u"d", u"e", u"z", u"E", u"t", u"i", u"k", u"l", u"m", u"n", u"o", u"p", u"r", u"s", u"s", u"t", u"u", u"f", u"c", u"x", u"O"]

def toASCII(greek_str):
    result = reduce(lambda x, (s, r): x.replace(s, r), zip(greekChars, asciiChars), greek_str)
    result = filter(lambda x: x in string.printable, result)
    return result

def toGreek(ascii_str):
    result = reduce(lambda x, (s, r): x.replace(s, r), zip(asciiChars, greekChars), ascii_str)
    return result


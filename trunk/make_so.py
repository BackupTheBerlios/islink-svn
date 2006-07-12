#!/usr/bin/python
# -*- coding: latin-1 -*-

import re
import sys

class Sagnord:
  def __init__(self, line):
    l = re.split('\t', re.split('\n', line)[0])
    self.nh = l[0]
    self.gerandi = l[1]
    self.tholandi = re.split(',', l[2]) #self.faFoll(l[2])
    self.samsett = []
    for i in l[3:]:
      self.samsett.append(re.split(',', i))
#      self.samsett.append([ss[0], ss[1:]]) #self.faFoll(ss[1])])

#  def faFoll(self, s):
#    foll = []
#    for i in range(0, len(s)):
#      foll.append(s[i])
#    return foll

def codeFS(fs):
  if fs == '�':
    return "SA"
  elif fs == '�':
    return 'SI'
  elif fs == 'ni�ur �':
    return 'SNIDURI'
  elif fs == 'fram � fyrir':
    return 'SFRAMIFYRIR'
  elif fs == 'inn �':
    return 'SINNI'
  elif fs == 'til':
    return 'STIL'
  elif fs == 'um sig':
    return 'SUMSIG'
  elif fs == 'fyrir':
    return 'SFYRIR'
  elif fs == 'undir':
    return 'SUNDIR'
  elif fs == 'sig':
    return 'SSIG'
  elif fs == 'inn �':
    return 'SINNA'
  elif fs == '�r':
    return 'SUR'
  elif fs == '�t':
    return 'SUT'
  elif fs == '� m�ti':
    return 'SAMOTI'
  elif fs == 'ni�ur':
    return 'SNIDUR'
  elif fs == 'saman':
    return 'SSAMAN'
  elif fs == 'upp':
    return 'SUPP'
  elif fs == 'af':
    return 'SAF'
  elif fs == '�t af':
    return 'SUTAF'
  elif fs == 'upp af':
    return 'SUPPAF'
  elif fs == 'undan':
    return 'SUNDAN'
  elif fs == 'a�':
    return 'SAD'
  elif fs == 'upp �':
    return 'SUPPI'
  elif fs == 'fram':
    return 'SFRAM'
  elif fs == 'burt':
    return 'SBURT'
  elif fs == 'vi�':
    return 'SVID'
  elif fs == 'me�':
    return 'SMED'
  elif fs == 'um':
    return 'SUM'
  elif fs == 'yfir':
    return 'SYFIR'
  elif fs == 'upp vi�':
    return 'SUPPVID'
  elif fs == 'til um':
    return 'STILUM'
  elif fs == 'gegn':
    return 'SGEGN'
  else:
    print 'Unknown forsetning "%s"' % fs
    assert False

def append(str, x, sep):
  if str == '':
    str = x
  else:
    str = '%s %s %s' % (str, sep, x)
  return str

def lesaUpplysingar(f):
  uppl = dict()
  inf = file(f, 'r')
  for line in inf:
    if len(line) > 1:
      so = Sagnord(line)
      uppl[so.nh] = so

  return uppl


def handleGermynd(myndir, inf, uppl, beyging):
  assert uppl.gerandi == 'n'

  haettir = ['f', 'v']
  personur = ['f', 'o', 't']
  tidir = ['n', 't']
  tolur = ['e', 'f']

  for persona in personur:
    for tid in tidir:
      for tala in tolur:
        ord = '%s.s' % (re.split('\n', inf.readline())[0])

        andlag = ''
        optional = False
        for th in uppl.tholandi:
          if th == 'x':
            optional = True
          elif len(th) == 1:
            andlag = append(andlag, 'S***%s+' % th, 'or')
          else:
            assert len(th) == 3
            andlag = append(andlag, '(S***%s+ & S***%s+)' % (th[0], th[2]), 'or')

        if optional and andlag != '':
          andlag = '{%s}' % andlag

        for ss in uppl.samsett:
          optional = False
          cfs = codeFS(ss[0])
          andl = ''
          for th in ss[1:]:
            if th == 'x':
              optional = True
            else:
              assert len(th) == 1

              andl = append(andl, 'S***%s+' % th, 'or')

          if andl == '':
            andl = append(andlag, '%s+', cfs)
          else:
            if optional:
              andl = '{%s}' % andl
            else:
              andl = '(%s)' % andl

            andlag = append(andlag, '(%s+ & %s)' % (cfs, andl), 'or')

        gefur = '(F%s%s*n- & {E+} & (%s) & {@IK+})' % (tala, persona, andlag)

        if ord in myndir:
          myndir[ord] = '%s or %s' % (myndir[ord], gefur)
        else:
          myndir[ord] = gefur


def make_so(myndir, f, upplysingar):
  fs = re.split('\.', f)
  beyging = fs[len(fs) - 1]

  inf = file(f, 'r')
  nh = re.split('\n', inf.readline())[0]
  sogn = "%s.%s" % (nh, beyging)

  if upplysingar.has_key(sogn):
    uppl = upplysingar[sogn]

    handleGermynd(myndir, inf, uppl, beyging)
  else:
    print "%s not found" % sogn
    assert False



if __name__ == '__main__':
  # usage: make_so
  upplysingar = lesaUpplysingar('data/sagnir')

  myndir = dict()

  for f in sys.argv[1:]:
    make_so(myndir, f, upplysingar)

  for mynd in myndir:
    print "%s: %s;" % (mynd, myndir[mynd])

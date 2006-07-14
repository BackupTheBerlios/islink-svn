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
    self.flokkur = l[3]
    self.samsett = []
    for i in l[4:]:
      self.samsett.append(re.split(',', i))
#      self.samsett.append([ss[0], ss[1:]]) #self.faFoll(ss[1])])

#  def faFoll(self, s):
#    foll = []
#    for i in range(0, len(s)):
#      foll.append(s[i])
#    return foll

def codeFS(fs):
  if fs == 'á':
    return 'TA'
  elif fs == 'í':
    return 'TI'
  elif fs == 'niður í':
    return 'TNIDURI'
  elif fs == 'fram í fyrir':
    return 'TFRAMIFYRIR'
  elif fs == 'inn í':
    return 'TINNI'
  elif fs == 'til':
    return 'TTIL'
  elif fs == 'um sig':
    return 'TUMSIG'
  elif fs == 'fyrir':
    return 'TFYRIR'
  elif fs == 'undir':
    return 'TUNDIR'
  elif fs == 'sig':
    return 'TSIG'
  elif fs == 'inn á':
    return 'TINNA'
  elif fs == 'úr':
    return 'TUR'
  elif fs == 'út':
    return 'TUT'
  elif fs == 'á móti':
    return 'TAMOTI'
  elif fs == 'niður':
    return 'TNIDUR'
  elif fs == 'saman':
    return 'TSAMAN'
  elif fs == 'upp':
    return 'TUPP'
  elif fs == 'af':
    return 'TAF'
  elif fs == 'út af':
    return 'TUTAF'
  elif fs == 'upp af':
    return 'TUPPAF'
  elif fs == 'undan':
    return 'TUNDAN'
  elif fs == 'að':
    return 'TAD'
  elif fs == 'upp í':
    return 'TUPPI'
  elif fs == 'fram':
    return 'TFRAM'
  elif fs == 'burt':
    return 'TBURT'
  elif fs == 'við':
    return 'TVID'
  elif fs == 'með':
    return 'TMED'
  elif fs == 'um':
    return 'TUM'
  elif fs == 'yfir':
    return 'TYFIR'
  elif fs == 'upp við':
    return 'TUPPVID'
  elif fs == 'til um':
    return 'TTILUM'
  elif fs == 'gegn':
    return 'TGEGN'
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

        gefur = '(F%s%s*n- & (({AE+} & (%s)) or ((%s) & {AE+})) & {AV+ or AR+ or AS+ or AH+} & {@IK+})' % (tala, persona, andlag, andlag)

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

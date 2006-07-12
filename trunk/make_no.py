#!/usr/bin/python

import re
import sys

def make_no(myndir, inf):
  kyn = re.split('\W+', inf.readline())[0]
  if kyn == 'kk':
    kyn = 'k'
  elif kyn == 'kvk':
    kyn = 'v'
  elif kyn == 'hk':
    kyn = 'h'

  foll = ['n', 'a', 'd', 'g']
  akvednir = ['o', 'a']
  tolur = ['e', 'f']

  for tala in tolur:
    for akvedni in akvednir:
      for fall in foll:
        ord = '%s.n' % re.split('\n', inf.readline())[0]
        stada = '%st%s%s%s' % (tala, kyn, fall, akvedni)
        gefur = '({[[@L%s%s%s%s-]]} & (({S***g+} & F%s+) or (S%s- & {S***g+})))' % (tala, kyn, fall, akvedni, stada, stada)
	if fall == 'g':
          gefur = '(({[[@L%s%s%s%s-]]} & S%s-) or (%s))' % (tala, kyn, fall, akvedni, stada, gefur)
        if ord in myndir:
          myndir[ord] = '%s or %s' % (myndir[ord], gefur)
        else:
          myndir[ord] = gefur


if __name__ == '__main__':
  myndir = dict()

  for f in sys.argv[1:]:
    make_no(myndir, file(f, 'r'))

  for mynd in myndir:
    print "%s: %s;" % (mynd, myndir[mynd])

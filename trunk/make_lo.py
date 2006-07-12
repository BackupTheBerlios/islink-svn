#!/usr/bin/python

import re
import sys

def lesaLinu(inf, myndir, akvedni, tala, kyn, fall, st):
  ord = '%s.l' % re.split('\n', inf.readline())[0]
  if ord != '--.l':
    gefur = '%s%s%s%s%s' % (tala, kyn, fall, akvedni, st)
    if akvedni == 'a':
      gefur = 'L%s+' % gefur
    else:
      gefur = '{AL%s-} & (L%s+ or LS%s-)' % (st, gefur, gefur)
    if ord in myndir:
      myndir[ord] = '%s or %s' % (myndir[ord], gefur)
    else:
      myndir[ord] = gefur


def make_lo(myndir, inf):
  kyn = ['k', 'v', 'h']
  foll = ['n', 'a', 'd', 'g']
  akvednir = ['o', 'a']
  tolur = ['e', 'f']
  stig = ['f', 'm', 'e']

  for akvedni in akvednir:
    for tala in tolur:
      for k in kyn:
        for fall in foll:
          lesaLinu(inf, myndir, akvedni, tala, k, fall, "n")

  for tala in tolur:
    for k in kyn:
      for fall in foll:
        lesaLinu(inf, myndir, akvedni, tala, k, fall, "*")

  for akvedni in akvednir:
    for tala in tolur:
      for k in kyn:
        for fall in foll:
          lesaLinu(inf, myndir, akvedni, tala, k, fall, "e")


if __name__ == '__main__':
  myndir = dict()

  for f in sys.argv[1:]:
    make_lo(myndir, file(f, 'r'))

  for mynd in myndir:
    print "%s: %s;" % (mynd, myndir[mynd])

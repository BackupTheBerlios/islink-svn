import re
import sys

def make_no(inf):
  kyn = re.split('\W+', inf.readline())[0]
  if kyn == 'kk':
    kyn = 'k'
  elif kyn == 'kvk':
    kyn = 'v'
  elif kyn == 'hk':
    kyn = 'h'

  foll = ['n', 'a', 'd', 'g']
  akvednir = ['a', 'o']
  tolur = ['e', 'f']

  myndir = dict()
  for tala in tolur:
    for akvedni in akvednir:
      for fall in foll:
        ord = '%s.n' % re.split('\n', inf.readline())[0]
        stada = '%st%s%s%s' % (tala, kyn, fall, akvedni)
        gefur = '({[[@A%s%s%s%s-]]} & (({SE***g+} & F%s+) or (S%s- & {SE***g+})))' % (tala, kyn, fall, akvedni, stada, stada)
	if fall == 'g':
          gefur = '(({[[@A%s%s%s%s-]]} & SE%s-) or (%s))' % (tala, kyn, fall, akvedni, stada, gefur)
        if ord in myndir:
          myndir[ord] = '%s or %s' % (myndir[ord], gefur)
        else:
          myndir[ord] = gefur

  for mynd in myndir:
    print "%s: %s;" % (mynd, myndir[mynd])

if __name__ == '__main__':
  for f in sys.argv[1:]:
    make_no(file(f, 'r'))

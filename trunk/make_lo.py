import re
import sys

def lesaLinu(inf, myndir, akvedni, tala, kyn, fall, st):
  ord = '%s.l' % re.split('\n', inf.readline())[0]
  if ord != '--.l':
    gefur = '%s%s%s%s%s' % (tala, kyn, fall, akvedni, st)
    gefur = 'A%s+ or BA%s-' % (gefur, gefur)
    if ord in myndir:
      myndir[ord] = '%s or %s' % (myndir[ord], gefur)
    else:
      myndir[ord] = gefur


def make_lo(inf):  
  kyn = ['k', 'v', 'h']
  foll = ['n', 'd', 'a', 'g']
  akvednir = ['a', 'o']
  tolur = ['e', 'f']
  stig = ['n', 'm', 'e']
  
  myndir = dict()

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

  for mynd in myndir:
    print "%s: %s;" % (mynd, myndir[mynd])


if __name__ == '__main__':
  for f in sys.argv[1:]:
    make_lo(file(f, 'r'))

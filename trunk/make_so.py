import re
import sys

class Sagnord:
  def __init__(self, line):
    l = re.split('\t', re.split('\n', line)[0])
    self.nh = l[0]
    self.gerandi = l[1]
    self.tholandi = self.faFoll(l[2])
    self.samsett = []
    for i in range(3, len(l)):
      ss = re.split(',', l[i])
      self.samsett.append([ss[0], self.faFoll(ss[1])])

  def faFoll(self, s):
    foll = []
    for i in range(0, len(s)):
      foll.append(s[i])
    return foll


def lesaUpplysingar(f):
  uppl = dict()
  inf = file(f, 'r')
  for line in inf:
    if len(line) > 1:
      so = Sagnord(line)
      uppl[so.nh] = so

  return uppl


def make_so(f, upplysingar):
  fs = re.split('\.', f)
  beyging = fs[len(fs) - 1]

  myndir = dict()

  inf = file(f, 'r')
  nh = re.split('\n', inf.readline())[0]
  print nh
  sogn = "%s.%s" % (nh, beyging)
  print sogn
  if upplysingar.has_key(sogn):
    uppl = upplysingar[sogn]
    print uppl.nh
    print uppl.gerandi
    print uppl.tholandi
    print uppl.samsett
  else:
    print "not found"

  for mynd in myndir:
    print "%s: %s;" % (mynd, myndir[mynd])

if __name__ == '__main__':
  # usage: make_so
  upplysingar = lesaUpplysingar('ord/sagnir')

  for f in sys.argv[1:]:
    make_so(f, upplysingar)

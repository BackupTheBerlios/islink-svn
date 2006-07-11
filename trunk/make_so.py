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
  if fs == 'niður í':
    return NIDUR_I
  if fs == 'á':
    return NIDUR_I
  else:
    print 'Unknown forsetning "%s"' % fs
    assert False

def append(str, x, sep):
  if str == '':
    str = x
  else:
    str = '%s %s %s' % (str, sep, x)

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
        ord = '%s.%s.s' % (re.split('\n', inf.readline())[0], beyging)

        andlag = ''
        optional = False
        for th in uppl.tholandi:
          if th == 'x':
            optional = True
          elif len(th) == 1:
            append(andlag, 'S***%s+' % th, 'or')
          else:
            assert len(th == 3)
            append(andlag, '(S***%s+ & S***%s+)' % (th[0], th[2]), 'or')

        if optional:
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

              append(andl, 'S***%s+' % th, 'or')

          if andl == '':
            append(andlag, '%s', cfs)
          else:
            if optinal:
              andl = '{%s}' % andl
            else:
              andl = '(%s)' % andl

            append(andlag, '(%s & %s)' % (cfs, andl), 'or')

        gefur = 'F%s%s*n- & {E+} & (%s) & {@IK+}' % (tala, persona, andlag)

        if ord in myndir:
          myndir[ord] = '%s or %s' % (myndir[ord], gefur)
        else:
          myndir[ord] = gefur

def make_so(f, upplysingar):
  fs = re.split('\.', f)
  beyging = fs[len(fs) - 1]

  myndir = dict()

  inf = file(f, 'r')
  nh = re.split('\n', inf.readline())[0]
  print nh
  sogn = "%s.%s" % (nh, beyging)
  print sogn

  if upplysingar.has_key('mála.vb'):
    print "hk1"
  if upplysingar.has_key('kyssa.vb'):
    print "hk2"

  if upplysingar.has_key(sogn):
    uppl = upplysingar[sogn]

    handleGermynd(myndir, inf, uppl, beyging)
  else:
    print "%s not found" % sogn
    print upplysingar
    assert False

  for mynd in myndir:
    print "%s: %s;" % (mynd, myndir[mynd])

if __name__ == '__main__':
  # usage: make_so
  upplysingar = lesaUpplysingar('data/sagnir')

  for f in sys.argv[1:]:
    make_so(f, upplysingar)

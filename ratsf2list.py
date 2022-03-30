##    Copyright 2008, 2009 Charles S. Hubbard, Jr.
##
##    This file is part of Rationale.
##
##    Rationale is free software: you can redistribute it and/or modify
##    it under the terms of the GNU General Public License as published by
##    the Free Software Foundation, either version 3 of the License, or
##    (at your option) any later version.
##
##    Rationale is distributed in the hope that it will be useful,
##    but WITHOUT ANY WARRANTY; without even the implied warranty of
##    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
##    GNU General Public License for more details.
##
##    You should have received a copy of the GNU General Public License
##    along with Rationale.  If not, see <http://www.gnu.org/licenses/>.


import csnd
import sys
import StringIO
import os

sf2file = sys.argv[1]
sf2presets = []

#csdout = StringIO.StringIO()
#csderr = StringIO.StringIO()
#oldstdout = sys.stdout
#oldstderr = sys.stderr
#sys.stdout = csdout
#sys.stderr = csderr
command = 'csound -nd test.orc test.sco'
orc = '''
sr = 44100
ksmps = 16
nchnls = 2

gifile sfload "''' + sf2file + '''"

        instr 11
sfplist gifile
        endin
'''
sco = '''
i11 0 .1
'''

cs = csnd.CppSound()
cs.setCommand(command)
cs.setOrchestra(orc)
cs.setScore(sco)
#cs.setPythonMessageCallback()
cs.exportForPerformance()
cs.compile()
cs.perform()

del cs

#sys.stderr = oldstderr
#sys.stdout = oldstdout

#startflag = 'Preset list'# of "%s"' % sf2file
#csdout.seek(0)
#flag = 0
#for line in csdout:
#    if line.count(startflag):
#        flag = 1
#    elif flag == 1:
#        if len(line.split()) == 0:
#            flag = 0
#        else:
#            ind = line.split()[0][:-1]
#            name = line.split()[1]
#            for word in line.split()[2:-2]:
#                name += ' %s' % word
#            prog = line.split()[-2].split(':')[1]
#            bank = line.split()[-1].split(':')[1]
#            sys.stdout.write('%s"%s %s%s' % (bank, prog, name, os.linesep))
#
##print sf2presets
#
#sys.stdout.flush()
#
#
##csderr.close()

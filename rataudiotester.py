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
import os
import sys
import threading
import time
import StringIO

rtmodule = sys.argv[1]
#csdout = StringIO.StringIO()
#csderr = StringIO.StringIO()
#oldstdout = sys.stdout
#oldstderr = sys.stderr
#sys.stdout = csdout
#sys.stderr = csderr
command = 'csound -+rtaudio=' + rtmodule + ' -odac0 test.orc test.sco'
csd = '''
<CsoundSynthesizer>
<CsInstruments>

        instr 11
        endin
</CsInstruments>
<CsScore>

</CsScore>
</CsoundSynthesizer>
'''

cs = csnd.CppSound()
cs.setCSD(csd)
cs.setCommand(command)
#cs.setPythonMessageCallback()
cs.exportForPerformance()
cs.compile()
del cs

#sys.stderr = oldstderr
#sys.stdout = oldstdout
#
#startflag = ''
#endflag = '!@#$%^&'
#
#if rtmodule == 'portaudio':
#    startflag = 'PortAudio: available'
#    endflag = 'error'
#if rtmodule == 'alsa':
#    startflag = '*** ALSA:'
#    endflag = 'Failed to initialise'
#if rtmodule == 'jack':
#    startflag = 'available JACK'
#    endflag = '*** rtjack:'
#if rtmodule == 'mme':
#    sys.stdout.write(rtmodule + '\n')
#if rtmodule == 'coreaudio':
#    sys.stdout.write(rtmodule + '\n')
#
#csdout.seek(0)
#flag = 0
#for line in csdout:
#    if line.count(startflag):
#        flag = 1
#    elif flag == 1:
#        if line.count(endflag):
#            flag = 0
#            break
#        elif not line.count('detected'):
#            sys.stdout.write(line)
#
#sys.stdout.flush()


#csderr.close()

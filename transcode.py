#/usr/bin/python

#import subprocess
#subprocess.check_output(['HandBrakeCLI', '--main-feature', '-m', '-q 20', '--strict-anamorphic', '--crop', '--detelecine', '--decomb', '-i /mnt/media/video/music/Underworld\ -\ Everything\,\ Everything/Underworld\ -\ Everything\,\ Everything.iso', '-o testoutput.mkv', '-E copy:ac3', '-e x264', '-x ref=5:mixed-refs=1:b-adapt=2:bframes=5:weightb=1:direct=auto:me=umh:subq=8:8x8dct=1:trellis=1:psy-rd=1,0:deblock=-2,-2:rc-lookahead=40:aq-strength=1.2:b-pyramid=2'])

from subprocess import Popen, PIPE
from threading import Thread
from Queue import Queue, Empty

io_q = Queue()

def stream_watcher(identifier, stream):

    for line in stream:
        io_q.put((identifier, line))

    if not stream.closed:
        stream.close()

proc = Popen(['HandBrakeCLI', '--main-feature', '-m', '-q', '20', '--strict-anamorphic', '--crop', '--detelecine', '--decomb', '-i', 'underworld.iso', '-o', 'testoutput.mkv', '-E', 'copy:ac3', '-e', 'x264', '-x', 'ref=5:mixed-refs=1:b-adapt=2:bframes=5:weightb=1:direct=auto:me=umh:subq=8:8x8dct=1:trellis=1:psy-rd=1,0:deblock=-2,-2:rc-lookahead=40:aq-strength=1.2:b-pyramid=2'], stdout=PIPE, stderr=PIPE)

Thread(target=stream_watcher, name='stdout-watcher',
        args=('STDOUT', proc.stdout)).start()
Thread(target=stream_watcher, name='stderr-watcher',
        args=('STDERR', proc.stderr)).start()

def printer():
    while True:
        try:
            # Block for 1 second.
            item = io_q.get(True, 1)
        except Empty:
            # No output in either streams for a second. Are we done?
            if proc.poll() is not None:
                break
        else:
            identifier, line = item
            print identifier + ':', line

Thread(target=printer, name='printer').start()

# from pocketsphinx import LiveSpeech

# speech_detector = LiveSpeech(fsg='./fsg_tlpm_test.test')

# for phrase in speech_detector:
#     print(phrase)

import sys, os, pyaudio
from pocketsphinx import Decoder
# from sphinxbase.sphinxbase import *

# modeldir = "files/sphinx/models"

# Create a decoder with certain model
# config = Decoder.default_config()
# config.set_string('-hmm', os.path.join(modeldir, 'en-us/en-us'))
# config.set_string('-dict', os.path.join(modeldir, 'en-us/cmudict-en-us.dict'))
#disable -logfn to get logs in console
# config.set_string('-logfn', 'files/sphinx.log')
# config.set_string('-keyphrase', 'abracadabra')
#decoder = Decoder(config)

#decoder.set_kws('keyword', 'keyword.list')
#decoder.set_search('keyword')


#!/usr/bin/env python3
"""
Recognize live speech from the default audio device.
"""

# MIT license (c) 2022, see LICENSE for more information.
# Author: David Huggins-Daines <dhdaines@gmail.com>

from pocketsphinx import Endpointer, Decoder, set_loglevel
import subprocess
import sys
import os


def main():
    # set_loglevel("INFO")
    ep = Endpointer()
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=ep.sample_rate, input=True)
    stream.start_stream()
    decoder = Decoder(
        samprate=ep.sample_rate,
    )
    print(ep.frame_bytes)


    while True:
        frame = stream.read(ep.frame_bytes//2)
        # print(len(frame))
        # sys.exit()
        prev_in_speech = ep.in_speech
        speech = ep.process(frame)
        if speech is not None:
            if not prev_in_speech:
                print("Speech start at %.2f" % (ep.speech_start), file=sys.stderr)
                decoder.start_utt()
            decoder.process_raw(speech)
            hyp = decoder.hyp()
            if hyp is not None:
                print("PARTIAL RESULT:", hyp.hypstr, file=sys.stderr)
            if not ep.in_speech:
                print("Speech end at %.2f" % (ep.speech_end), file=sys.stderr)
                decoder.end_utt()
                print(decoder.hyp().hypstr)


try:
    main()
except KeyboardInterrupt:
    pass
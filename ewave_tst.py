import ewave_tst

with ewave_tst.open('HIROSHIMA30_1.wav') as w:
    print("samplerate = {0.sampling_rate} Hz, length = {0.nframes} samples, "
          "channels = {0.nchannels}, dtype = {0.dtype!r}".format(w))
    data = w.read()


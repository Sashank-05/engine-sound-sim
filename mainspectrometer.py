import controls
import engine_factory
from audio_device import AudioDevice
import random
import matplotlib.pyplot as plt
import matplotlib.animation
import numpy
import threading
import math

# engine = engine_factory.v_four_90_deg()
# engine = engine_factory.w_16()
engine = engine_factory.v_8_LS()
# engine = engine_factory.inline_5_crossplane()
# engine = engine_factory.inline_6()
#engine = engine_factory.boxer_4_crossplane_custom([1, 1, 0, 0])  # (rando := random.randrange(360)))
# engine = engine_factory.boxer_4_half()
# engine = engine_factory.random()
# engine = engine_factory.fake_rotary_2rotor()

audio_device = AudioDevice()
stream = audio_device.play_stream(engine.gen_audio)

print('\nEngine is running...')
# print(rando)

RATE = 44100
BUFFER = 882

fig = plt.figure()
line1 = plt.plot([],[])[0]
line2 = plt.plot([],[])[0]

r = range(0,int(RATE/2+1),int(RATE/BUFFER))
l = len(r)

def init_line():
        line1.set_data(r, [-1000]*l)
        line2.set_data(r, [-1000]*l)
        return (line1,line2,)





def get_rms( block ):
    # RMS amplitude is defined as the square root of the 
    # mean over time of the square of the amplitude.
    # so we need to convert this string of bytes into 
    # a string of 16-bit samples...

    # we will get one short out for each 
    # two chars in the string.
    count = len(block)/2
    format = "%dh"%(count)
    shorts = struct.unpack( format, block )

    # iterate over the block.
    sum_squares = 0.0
    for sample in shorts:
        # sample is a signed short in +/- 32768. 
        # normalize it to 1.0
        n = sample * SHORT_NORMALIZE
        sum_squares += n*n

    return math.sqrt( sum_squares / count )

def update_line(i):
    data = stream
    
    data = numpy.log10(numpy.sqrt(get_rms(data) / BUFFER)) * 10
    line1.set_data(r, data)
    line2.set_data(numpy.maximum(line1.get_data(), line2.get_data()))
    return (line1,line2)

plt.xlim(0, 20000)
plt.ylim(-60, 0)
plt.xlabel('Frequency')
plt.ylabel('dB')
plt.title('Spectrometer')
plt.grid()

line_ani = matplotlib.animation.FuncAnimation(
    fig, update_line, init_func=init_line, interval=0, blit=True
)

print(stream)
try:
    #threading.Thread(target=lambda: plt.show()).start()
    plt.show()
    controls.capture_input(engine)  # blocks until user exits
except KeyboardInterrupt:
    pass

print('Exiting...')
stream.close()
audio_device.close()

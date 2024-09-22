import threading
import numpy
from pynput import keyboard
import time
import controls
import engine_factory
from audio_device import AudioDevice
import random
import os
import matplotlib.pyplot as plt

import matplotlib.animation
#engine = engine_factory.inline_16()
#engine = engine_factory.inline_1()
#engine = engine_factory.v_four_90_deg()
#engine = engine_factory.w_16()
#engine = engine_factory.v_8_LS()
#engine = engine_factory.inline_5_crossplane()
#engine = engine_factory.inline_6()
#engine = engine_factory.boxer_4_crossplane_custom([0, 1, 0, 0])  # (rando := random.randrange(360)))
#engine = engine_factory.inline_4_1_spark_plug_disconnected()
#engine = engine_factory.inline_4()
# engine = engine_factory.boxer_4_half()
#engine = engine_factory.electric()
#engine = engine_factory.random()
engine = engine_factory.fake_rotary_2rotor()
#engine = engine_factory.V_12()
#engine = engine_factory.v_twin_60_deg()
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

def update_line(i):
    data = stream
    data = numpy.log10(numpy.sqrt(
        numpy.real(data)**2+numpy.imag(data)**2) / BUFFER) * 10
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



  

gear = 1
is_acc = True
clutch = False

def reduce_speed():
    global gear
    global is_acc
    global clutch
    while True:
        
        if clutch:
           engine.brake(1)
           return

        if is_acc:
            if engine._rpm <= 800:
                break
            if gear == 1:
                engine.brake(40)
            elif gear == 2:
                engine.no_acc(7)
            elif gear == 3:
                engine.no_acc(5)
            elif gear == 4:
                engine.no_acc(1)
            elif gear == 5:
                engine.no_acc(0.1)
            elif gear == 6:
                engine.no_acc(0.01)
            
        time.sleep(0.01)
        #os.system('cls')

        print(f"{engine._rpm}     gear : " + str(gear) + " ", end="\r")


def on_press(key):
    
    global clutch
    global gear
    global is_acc
    
    
    if key == keyboard.Key.esc:
        return False  # stop listener
    try:
        k = key.char  # single-char keys
    except:
        k = key.name  # other keys
    if k == 'w':
        is_acc = False
        if clutch:
             engine.throttle(1000)
             return 
        if gear == 1:
            engine.throttle(450.0)

        elif gear == 2:
            engine.throttle(100.0)
        elif gear == 3:
            engine.throttle(48.0)
        elif gear == 4:
            engine.throttle(24)
        elif gear == 5:
            engine.throttle(12)
        elif gear == 6:
            engine.throttle(5)
            #time.sleep(0.7)
        time.sleep(0.02)
    elif k == "e":

        if gear < 6 and gear >= 1:
            gear += 1

        if gear == 1:

            if engine._rpm > 6000:
                engine.specific_rpm(engine._rpm-5000)
            elif engine._rpm > 4000:
                engine.specific_rpm(engine._rpm-2000)
            elif engine._rpm > 2000:
                engine.specific_rpm(engine._rpm-1000)
            else:
                engine.specific_rpm(engine._rpm-500)

        elif gear == 2:
            if engine._rpm > 5000:  # speed is approx 80 here
                engine.specific_rpm(engine._rpm-3000)

            elif engine._rpm > 4000:
                engine.specific_rpm(engine._rpm-2000)
            else:
                engine.specific_rpm(engine._rpm-500)

        elif gear == 3:
            if engine._rpm > 5000:  # speed is approx 110 here
                engine.specific_rpm(engine._rpm-2000)

            elif engine._rpm > 4000:
                engine.specific_rpm(engine._rpm-1000)
            else:
                engine.specific_rpm(engine._rpm-400)
        elif gear == 4:
            if engine._rpm > 5000:  # speed is approx 130 here
                engine.specific_rpm(engine._rpm-3000)

            elif engine._rpm > 3000:
                engine.specific_rpm(engine._rpm-1000)
            else:
                engine.specific_rpm(engine._rpm-500)
        elif gear == 5:
            if engine._rpm > 5000:  # speed is approx 150 here
                engine.specific_rpm(engine._rpm-3000)

            elif engine._rpm > 4000:
                engine.specific_rpm(engine._rpm-2000)
            else:
                engine.specific_rpm(engine._rpm-400)
        elif gear == 6:
            engine.specific_rpm(engine._rpm-25)
        os.system('cls')

        print(f"{engine._rpm}     gear : " + str(gear) + "  ", end="\r")
        


    elif k == "q":
        if gear > 1 and gear < 6:
            gear -= 1

        if engine._rpm > 7000:
            engine.specific_rpm(engine._rpm+1000)
        elif engine._rpm > 6000:
            engine.specific_rpm(engine._rpm+500)
        elif engine._rpm > 5000:
            engine.specific_rpm(engine._rpm+400)
        elif engine._rpm > 4000:
            engine.specific_rpm(engine._rpm+300)
        elif engine._rpm > 3000:
            engine.specific_rpm(engine._rpm+200)
        elif engine._rpm > 2000:
            engine.specific_rpm(engine._rpm+100)
        elif engine._rpm > 1000:
            engine.specific_rpm(engine._rpm+50)
        elif engine._rpm > 0:
            engine.specific_rpm(engine._rpm+20)
        os.system('cls')
        print(f"{engine._rpm}     gear : " + str(gear) + "  ", end="\r")
            


    elif k == 's':
        is_acc = True
        engine.brake(50)

    elif k == 'c':
        is_acc = False
        clutch = True
        os.system('cls')

        print(f"clutch     gear : " + str(gear) + "  ", end="\r")
    
        


def on_release(key):
    global gear
    global is_acc
    global clutch

    try:
        k = key.char  # single-char keys
    except:
        k = key.name

    if k == keyboard.Key.esc:
        return False
    if k == 'w':
        is_acc = True
        thread = threading.Thread(target=reduce_speed)
        thread.start()
    elif k == 'c':
         clutch = False

for i in range(0,8):
    engine.throttle(1500)
    time.sleep(0.05)
    #print(i)
    
for i in range(0,8):
    engine.brake(150)
    time.sleep(0.05)
    #print(i)

listener = keyboard.Listener(on_press=on_press, on_release=on_release)
#t = threading.Thread(target=lambda: plt.savefig('img.png'))

listener.start()  # start to listen on a separate thread
listener.join()
os.system('cls')

stream.close()
audio_device.close()

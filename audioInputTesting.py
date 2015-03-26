import alsaaudio
import time
import audioop
from Controllers.Controllers import AudioController

controller = AudioController(channel=1, rate=16000)

inputs = []

while(True):
    input = controller.getinput()
    if(input):
        inputs.append(input)
        sum = 0
        for i in inputs:
            sum += i
        average = sum / len(inputs)
        if len(inputs) > 10:
            inputs = []
        print(" " * int(input / 5) + "*")
    # time.sleep(0.001)


# inp = alsaaudio.PCM(alsaaudio.PCM_CAPTURE, alsaaudio.PCM_NONBLOCK)

# inp.setchannels(1)
# inp.setrate(16000)
# inp.setformat(alsaaudio.PCM_FORMAT_S16_LE)

# inp.setperiodsize(160)

# while(True):
#     l, data = inp.read()
#     if l:
#         print(">"*(audioop.max(data, 2)/80))
#     time.sleep(0.001)

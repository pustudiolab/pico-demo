from machine import Pin, PWM, UART
import utime

'''
['C', 'Cs', 'D', 'Ds', 'E', 'F', 'Fs', 'G', 'Gs', 'A', 'As', 'B']
  0    1     2    3     4    5    6     7    8     0    10    11
 12   13    14   15    16   17   18    19   20    21    22    23
 24   25    26   27    28   29   30    31   32    33    34    35
 36   37    38   39    40   41   42    43   44    45    46    47
'''

# Start with A1
note_frequencies = [130.81]
note_names = ['C', 'Cs', 'D', 'Ds', 'E', 'F', 'Fs', 'G', 'Gs', 'A', 'As', 'B']

for note in range(1, 49):
    note_frequencies.append(note_frequencies[0] * (2. ** (float(note) / 12.)))
    print(str(note_names[note % 12]) + ' ' + str(note_frequencies[-1]))

# Read music csv file
music = []
with open('mario_2.txt','r') as file:
    for line in file:
        line = line.rstrip('\n')
        line = line.rstrip('\r')
        music.append(line.split(','))
        
print(music)

print('\n')
tempo_bpm = music[0][0]
print('tempo (BPM):           ' + str(tempo_bpm))
quarter_note_time = 60. / float(tempo_bpm)
print('Quarter note time (s): ' + str(quarter_note_time))
print('\n')

speaker = PWM(Pin(15))
board_led = Pin(25, Pin.OUT)
uart1 = UART(1, baudrate=9600, tx=Pin(8), rx=Pin(9), timeout=50)
uart0 = UART(0, baudrate=9600, tx=Pin(16), rx=Pin(17), timeout=50)

# Starting synchronization
txData = bytes("START", 'utf-8')
board_led.on()
while True:
    rxData = uart1.readline()
    if not rxData is None:
        if "START" in rxData.decode('utf-8'):
            break
for i in range(5):
    uart1.write(txData + b'\n')
board_led.off()

for idx in range(1, len(music)):
    print(music[idx])
    if int(music[idx][1]) >= 0:
        note_duration = 4 * quarter_note_time / float(music[idx][0])
        note_freq = note_frequencies[int(music[idx][1])]
        note_name = note_names[int(music[idx][1]) % 12]
        
        start_time = utime.ticks_ms()
        
        speaker.freq(round(note_freq))
        speaker.duty_u16(2 ** 15)
        print('Playing note ' + note_name + ' @' + str(note_freq) + 'Hz, 1 / ' + str(int(music[idx][0])) + ' -th note')
    else:
        note_duration = 4 * quarter_note_time / float(music[idx][0])
        
        start_time = utime.ticks_ms()
        
        speaker.duty_u16(0)
        
        print('Rest, 1 / ' + str(int(music[idx][0])) + ' -th note')
        
            
    while utime.ticks_diff(utime.ticks_ms(), start_time) < note_duration * 1000:
        pass
    
speaker.duty_u16(0)

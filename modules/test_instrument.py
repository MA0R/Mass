"""code for conencting to a single instrument and sending it info"""
import visa
rm = visa.ResourceManager()
b = rm.open_resource('ASRL2::INSTR')

b.baud_rate = 2400
b.parity = visa.constants.Parity.even
b.stop_bits = visa.constants.StopBits.one
b.data_bits = 7

run = True

while run:
    s = raw_input("... ")
    if s == 'q':
        run = False
    else:
        b.write(s)
        try:
            print(b.read())
        except visa.VisaIOError:
            print("Fialed to read")
print("stopped")

#LIFT
#SINK returns "ready"

#MOVE n
#go down twice, wiat time and check for 'ready'.
#sink1 is 20s, and 20s for second sink.
#Wait 20s after it reports that it is ready.
#ask identity, IDENTIFY. (For both).

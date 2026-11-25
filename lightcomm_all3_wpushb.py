from machine import Pin, ADC
import time

# --- Setup ---
led1 = Pin(15, Pin.OUT)   # Channel 1 LED (GP15)
led2 = Pin(14, Pin.OUT)   # Channel 2 LED (GP14)
ldr1 = ADC(26)            # Channel 1 LDR (ADC0 GP26)
ldr2 = ADC(27)            # Channel 2 LDR (ADC1 GP27)
button = Pin(16, Pin.IN, Pin.PULL_UP)  # Pushbutton (GP16)

# Parameters
bit_time = 0.3
samples_per_bit = 5
settle_time = 0.05
preamble = "10101010"

# --- Inputs ---
message = input("Enter the message to send: ")
mode = int(input("Select channel mode (1=Ch1, 2=Ch2, 3=Split): "))

# --- Helper: convert char to 8-bit binary ---
def char_to_bin(c):
    ascii_val = ord(c)
    bin_str = ""
    for i in range(8):
        bin_str = str(ascii_val % 2) + bin_str
        ascii_val //= 2
    return bin_str

# --- Build binary messages ---
if mode == 1:
    binary1 = preamble + "".join(char_to_bin(c) for c in message)
    binary2 = ""
elif mode == 2:
    binary1 = ""
    binary2 = preamble + "".join(char_to_bin(c) for c in message)
else:  # mode 3 = split
    mid = len(message) // 2
    msg1 = message[:mid]
    msg2 = message[mid:]
    binary1 = preamble + "".join(char_to_bin(c) for c in msg1)
    binary2 = preamble + "".join(char_to_bin(c) for c in msg2)

print("Binary1:", binary1)
print("Binary2:", binary2)

# --- Auto threshold for each LDR ---
def calibrate(led, ldr):
    led.value(0)
    time.sleep(1)
    off = sum(ldr.read_u16() for _ in range(10)) / 10
    led.value(1)
    time.sleep(1)
    on = sum(ldr.read_u16() for _ in range(10)) / 10
    led.value(0)
    time.sleep(0.5)
    return (on + off) / 2

threshold1 = calibrate(led1, ldr1)
threshold2 = calibrate(led2, ldr2)
print("Threshold1:", threshold1)
print("Threshold2:", threshold2)

# --- Wait for pushbutton press ---
print("Press the button to start transmission...")
while button.value():  # HIGH until pressed
    time.sleep(0.05)
print("Button pressed! Starting transmission...")

# --- Transmission ---
max_len = max(len(binary1), len(binary2))
received1, received2 = "", ""

for i in range(max_len):
    bit1 = binary1[i] if i < len(binary1) else '0'
    bit2 = binary2[i] if i < len(binary2) else '0'

    # Set LEDs
    led1.value(1 if bit1 == '1' else 0)
    led2.value(1 if bit2 == '1' else 0)
    time.sleep(settle_time)

    # Read LDRs
    if binary1:  # only if channel 1 is used
        readings1 = [ldr1.read_u16() for _ in range(samples_per_bit)]
        ones1 = sum(1 for r in readings1 if r > threshold1)
        detected1 = '1' if ones1 > samples_per_bit // 2 else '0'
        received1 += detected1 if i < len(binary1) else ""
    if binary2:  # only if channel 2 is used
        readings2 = [ldr2.read_u16() for _ in range(samples_per_bit)]
        ones2 = sum(1 for r in readings2 if r > threshold2)
        detected2 = '1' if ones2 > samples_per_bit // 2 else '0'
        received2 += detected2 if i < len(binary2) else ""

    print(f"i={i} | Ch1 sent:{bit1}, Ch2 sent:{bit2}")

    time.sleep(bit_time - settle_time)

led1.value(0)
led2.value(0)
print("Transmission complete.")

# --- Strip preambles ---
if received1.startswith(preamble): received1 = received1[len(preamble):]
if received2.startswith(preamble): received2 = received2[len(preamble):]

# --- Decode binaries ---
def bin_to_text(binary):
    msg = ""
    for i in range(0, len(binary), 8):
        byte = binary[i:i+8]
        if len(byte) == 8:
            msg += chr(int(byte, 2))
    return msg

decoded1 = bin_to_text(received1)
decoded2 = bin_to_text(received2)

final_message = decoded1 + decoded2
print("Decoded (Ch1):", decoded1)
print("Decoded (Ch2):", decoded2)
print("Final recombined message:", final_message)

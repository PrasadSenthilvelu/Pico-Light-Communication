# Light-Based Communication Using Raspberry Pi Pico

An experimental light-based communication system implemented using a Raspberry Pi Pico, LEDs and Light Dependent Resistors (LDRs), using optical signals to transmit and decode ASCII-encoded messages.

## Overview

This project explores optical communication using a Raspberry Pi Pico, LEDs and LDRs. Messages are encoded into binary sequences and transmitted using LEDs, while LDRs detect the corresponding changes in light intensity and convert them back into digital information.

The system supports single-channel transmission through either of two optical channels, as well as a split mode in which a message is divided between the two channels.

## Hardware

- Raspberry Pi Pico
- LEDs (2)
- Light Dependent Resistors (LDRs) (2)
- Resistors
- Pushbutton
- Breadboard and jumper wires

## How It Works

- **Message encoding:** Each character in the input message is converted into an 8-bit ASCII binary representation.
- **Optical transmission:** Binary bits are transmitted by switching LEDs on and off, representing `1` and `0`, respectively.
- **Light detection:** LDRs detect changes in light intensity and provide analog readings to the Pico through its ADC pins.
- **Automatic calibration:** Threshold values for distinguishing between illuminated and unilluminated states are determined independently for each channel.
- **Majority-vote detection:** Multiple LDR readings are taken during each bit interval, with the detected bit determined by majority voting.
- **Preamble:** A predefined binary sequence is transmitted before the message to serve as a calibration pattern.
- **Dual-channel transmission:** The system supports transmission through either channel individually or splitting the message across both channels.

## Transmission Modes

| Mode | Description |
|---|---|
| Channel 1 | Transmits the message through the first LED–LDR channel. |
| Channel 2 | Transmits the message through the second LED–LDR channel. |
| Split | Divides the message into two portions and transmits them through the two channels. |

## Hardware Configuration

| Component | Raspberry Pi Pico Pin |
|---|---|
| LED 1 | GP15 |
| LED 2 | GP14 |
| LDR 1 | GP26 (ADC0) |
| LDR 2 | GP27 (ADC1) |
| Pushbutton | GP16 |

Each LDR is connected as part of a voltage-divider circuit to an analog input of the Pico.

## Software

- MicroPython
- Thonny IDE

## Code

The implementation is available in [`lightcomm_all3_wpushb.py`](lightcomm_all3_wpushb.py).



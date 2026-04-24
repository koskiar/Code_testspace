Testing on Raspberry Pi
I can’t run code directly in a Raspberry Pi emulator myself, but this GUI and GPIO setup is fully compatible with Raspberry Pi 4 Model B. Here’s how you can test it:

Setup Instructions
Install dependencies:

sudo apt update
sudo apt install python3 python3-pip
pip3 install RPi.GPIO

Then:

python3 main.py

What you’ll see:

A window titled “Raspberry Pi Test Kit”

Fields for:

Tester Name

Board ID

Dropdown to select a test

Button to run the test

After running a test, a popup confirms the result is saved.
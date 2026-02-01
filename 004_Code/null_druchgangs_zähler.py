import machine
import time

# Konfiguration
INPUT_PIN = 21
pico_pin = machine.Pin(INPUT_PIN, machine.Pin.IN, machine.Pin.PULL_DOWN)
#zusätzlich zum intenen Pulldown noch externen (10k, intern hat 50k oder 100k oder so)für schnelleres 0V.

# Variablen für die Messung
pulse_count = 0

# Interrupt Service Routine (ISR)
def handle_interrupt(pin):
    global pulse_count
    pulse_count += 1

pico_pin.irq(trigger=machine.Pin.IRQ_RISING, handler=handle_interrupt)
#interrup: triggern auf rising edge

print("Frequenzmessung gestartet (Dioden-Schutzschaltung)...")

while True:
    # Torzeit: 1 Sekunde lang Impulse zählen
    pulse_count = 0
    time.sleep(1.0)
    
    frequency = pulse_count
    
    if frequency > 0:
        print(f"Frequenz: {frequency} Hz")
    else:
        print("Kein Signal erkannt.")
        
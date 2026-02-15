from machine import Pin
import rp2
import time

# --- 1. PIO Programm Definition ---
# Wir entfernen psel_sig aus dem Dekorator, um Kompatibilitätsprobleme zu vermeiden
@rp2.asm_pio()
def pulse_counter():
    mov(x, invert(null))     # Setze Zähler x auf den Maximalwert (0xFFFFFFFF)
    
    label("loop")
    wait(1, pin, 0)          # Warte auf High am Pin
    wait(0, pin, 0)          # Warte auf Low am Pin
    jmp(x_dec, "loop")       # Dekrementiere x und springe zu loop

# --- 2. Hardware Konfiguration ---
INPUT_PIN = 21
# Interner Pull-Down ist wichtig, damit der Pin bei offenem Kontakt nicht "schwebt"
pin_in = Pin(INPUT_PIN, Pin.IN, Pin.PULL_DOWN)

# Initialisierung der State Machine
# in_base=pin_in sagt dem PIO, welcher physikalische Pin für den Befehl 'wait(..., pin, 0)' genutzt wird.
sm = rp2.StateMachine(0, pulse_counter, in_base=pin_in)

MAX_COUNT = 0xFFFFFFFF

def get_frequency(gate_time=1.0):
    # Register x im PIO manuell zurücksetzen, bevor wir starten
    # (Damit wir immer beim Maximum anfangen)
    sm.active(0)
    sm.exec("mov(x, invert(null))")
    
    sm.active(1)             # Messung starten
    time.sleep(gate_time)    # Torzeit abwarten
    sm.active(0)             # Messung stoppen
    
    # Wert aus dem internen Register x in den Python-Speicher schieben
    sm.exec("mov(isr, x)")
    sm.exec("push()")
    
    raw_value = sm.get()
    
    # Differenz berechnen (da der PIO rückwärts zählt)
    pulses = MAX_COUNT - raw_value
    return pulses / gate_time

# --- 3. Hauptschleife ---
print("PIO Frequenzmessung (korrigiert) gestartet...")

while True:
    try:
        freq = get_frequency(1.0)
        if freq > 0:
            print(f"Frequenz: {int(freq)} Hz")
        else:
            print("Kein Signal erkannt.")
    except Exception as e:
        print(f"Fehler bei der Messung: {e}")
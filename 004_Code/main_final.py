import math
from machine import Pin, SPI, Timer
import rp2
import network
import socket
import time

# --- HOCHSCHULE BREMEN | BACHELORARBEIT | NILS RENNER | 2025/26 ---

led = Pin("LED", Pin.OUT)

# 1. Start-Check: LED blinkt 5 mal schnell
for _ in range(5):
    led.value(1)
    time.sleep(0.1)
    led.value(0)
    time.sleep(0.1)

led.value(1) # LED bleibt an -> WLAN wird gestartet

# =================================================================
# PIO FREQUENZZÄHLER KONFIGURATION
# =================================================================
@rp2.asm_pio()
def pulse_counter():
    mov(x, invert(null))     
    label("loop")
    wait(1, pin, 0)          
    wait(0, pin, 0)          
    jmp(x_dec, "loop")       

INPUT_PIN = 21
pin_in = Pin(INPUT_PIN, Pin.IN, Pin.PULL_DOWN)
sm = rp2.StateMachine(0, pulse_counter, in_base=pin_in)
MAX_COUNT = 0xFFFFFFFF

frequency_history = [0, 0, 0, 0, 0]
last_measured_freq = 0

KALIBRIERUNGS_FAKTOR = 1.007  
TORZEIT_MS = 2000 
TORZEIT_SEK = TORZEIT_MS / 1000

def measure_tick(t):
    global last_measured_freq
    sm.active(0)
    sm.exec("mov(isr, x)")
    sm.exec("push()")
    raw_value = sm.get()
    
    sm.exec("mov(x, invert(null))")
    sm.active(1)
    
    pulses = MAX_COUNT - raw_value
    korrigierte_freq = (pulses / TORZEIT_SEK) * KALIBRIERUNGS_FAKTOR
    
    if pulses < 1: 
        last_measured_freq = 0
    else:
        last_measured_freq = round(korrigierte_freq, 0) 
    
    frequency_history.insert(0, last_measured_freq)
    if len(frequency_history) > 5:
        frequency_history.pop()

sm.active(1)
freq_timer = Timer(-1)
freq_timer.init(period=TORZEIT_MS, mode=Timer.PERIODIC, callback=measure_tick)

# =================================================================
# FILTER LOGIK (AUF WIDERSTANDS-EINGABE ANGEPASST)
# =================================================================

### Initialisierung
# Startwerte
freq0 = 1000  # Jetzt als Widerstandswert (R) in Ohm interpretiert
Q_val = 1
H0_val = 1

# Digitalpoti-Parameter
max_step = 255
r_ges = 9.65e3
wiper_r = 4 

freq_wiper = 0
freq_r     = 0
Q_wiper = 0
Q_r     = 0
H0_wiper = 0
H0_r     = 0

def clamp_and_round(x):
    return int(round(max(0, min(255, x))))

# Frequenz-zu-Bit Berechnung auskommentiert
# def freq_2_bit(freq0):
#     freq_c = 1e-6
#     wfreq0 = freq0 * 2 * math.pi
#     freq_r = 1/(wfreq0 * freq_c)
#     freq_wiper = max_step * (1 - freq_r/r_ges) + wiper_r    
#     return clamp_and_round(freq_wiper), freq_r                                      

def Q_2_bit(Q_val):
    r_opv = 1000
    Q_r = Q_val * r_opv
    Q_wiper = max_step * (1 - Q_r/r_ges) + wiper_r
    return clamp_and_round(Q_wiper), Q_r

def H0_2_bit(H0_val):
    r_opv = 1000
    H0_r = r_opv/H0_val
    H0_wiper = max_step * (1 - H0_r/r_ges) + wiper_r
    return clamp_and_round(H0_wiper), H0_r

def bit_2_res(bit):
    res = r_ges * (1 - (bit-wiper_r)/max_step)      
    return res

def update_filter(r_val, q_v, h_v):
    global freq_wiper, freq_r, Q_wiper, Q_r, H0_wiper, H0_r, freq0, Q_val, H0_val
    freq0, Q_val, H0_val = r_val, q_v, h_v
    
    # Direkte Berechnung des Wiper-Werts aus dem Widerstand (r_val)
    freq_r = r_val
    freq_wiper = clamp_and_round(max_step * (1 - freq_r/r_ges) + wiper_r)
    
    Q_wiper,    Q_r    = Q_2_bit(Q_val)
    H0_wiper,   H0_r   = H0_2_bit(H0_val)

    set_wiper0(cs1, freq_wiper)
    set_wiper1(cs1, freq_wiper)
    set_wiper0(cs2, Q_wiper)
    set_wiper1(cs2, H0_wiper)

### SPI und Pins Initialisieren
spi = SPI(0, baudrate=1_000_000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB,
    sck=Pin(18), mosi=Pin(19), miso=Pin(16))

cs1 = Pin(17, Pin.OUT, value=1) 
cs2 = Pin(20, Pin.OUT, value=1) 

def mcp_write(cs_pin, command, value):
    cs_pin.value(0)           
    spi.write(bytes([command & 0xFF, value & 0xFF]))  
    cs_pin.value(1)           

def set_wiper0(cs_pin, value):  
    cmd = 0x00                 
    mcp_write(cs_pin, cmd, value)

def set_wiper1(cs_pin, value):    
    cmd = 0x10                 
    mcp_write(cs_pin, cmd, value)

update_filter(freq0, Q_val, H0_val)

ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid="Pico-Filter", password="filter123")
ap.ifconfig(("192.168.4.1", "255.255.255.0", "192.168.4.1", "8.8.8.8"))

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    conn, addr = s.accept()
    request = conn.recv(1024).decode('utf-8')
    
    if "/set?" in request:
        try:
            params = request.split(' ')[1].split('?')[1].split('&')
            new_r = freq0
            new_q = Q_val
            new_h = H0_val
            for p in params:
                k, v = p.split('=')
                if k == 'res': new_r = float(v)
                if k == 'Q':   new_q = float(v)
                if k == 'H0':  new_h = float(v)
            update_filter(new_r, new_q, new_h)
        except:
            pass

    history_rows = "".join([f"<tr><td>{f} Hz</td></tr>" for f in frequency_history])

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Pico Filter Control</title>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="15">
        <style>
            body {{ font-family: 'Segoe UI', Arial, sans-serif; margin: 0; padding: 20px; background: #eceff1; color: #333; }}
            .container {{ max-width: 1000px; margin: auto; }}
            .header {{ 
                background: #263238; color: white; padding: 20px; border-radius: 8px; 
                margin-bottom: 20px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.1); 
            }}
            .layout {{ display: flex; gap: 25px; flex-wrap: wrap; }}
            .card {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); flex: 1; min-width: 300px; }}
            h2 {{ color: #0078d7; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-top: 0; }}
            table {{ border-collapse: collapse; margin-top: 15px; width: 100%; }}
            th, td {{ border: 1px solid #e0e0e0; padding: 10px; text-align: center; }}
            th {{ background: #f5f5f5; font-weight: 600; }}
            .freq-display {{ font-size: 3em; color: #0078d7; font-weight: bold; margin: 15px 0; text-align: center; }}
            .btn {{ background: #0078d7; color: white; border: none; padding: 12px 20px; border-radius: 4px; cursor: pointer; font-size: 16px; width: 100%; }}
            .btn:hover {{ background: #005a9e; }}
            input {{ padding: 10px; border: 1px solid #ccc; border-radius: 4px; margin-bottom: 15px; width: 90%; }}
            label {{ font-weight: bold; font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1 style="margin:0; font-size: 2.2em; letter-spacing: 1px;">
                    Self-Tuned Biquad-Filter
                </h1>
                
                <p style="margin: 8px 0 15px 0; font-size: 1.1em; color: #81d4fa; font-weight: 300;">
                    Digitale Parametersteuerung & Echtzeit-Validierung via RP2350
                </p>
                
                <div style="height: 1px; background: rgba(255,255,255,0.2); width: 60%; margin: 10px auto;"></div>
                
                <p style="margin: 10px 0 0 0; font-size: 0.9em; opacity: 0.9; word-spacing: 2px;">
                    <strong>Hochschule Bremen</strong> &nbsp;•&nbsp; 
                    Bachelorarbeit &nbsp;•&nbsp; 
                    <strong>Nils Renner</strong> &nbsp;•&nbsp; 
                    2025/26
                </p>
            </div>

            <div class="layout">
                <div class="card">
                    <h2>Filter-Parameter</h2>
                    <form action="/set" method="get">
                        <label>Soll-Widerstand (f<sub>0</sub>-bestimmend) [&Omega;]:</label><br>
                        <input type="number" name="res" value="{freq0}">
                        <label>Güte (Q):</label><br>
                        <input type="number" name="Q" step="0.1" value="{Q_val}"><br>
                        <label>Verstärkung (H0):</label><br>
                        <input type="number" name="H0" step="0.1" value="{H0_val}"><br>
                        <input type="submit" class="btn" value="Werte an Filter senden">
                    </form>

                    <h2 style="margin-top:20px;">Aktuelle Wiper-Konfiguration</h2>
                    <table>
                        <tr><th>Parameter</th><th>Soll</th><th>Wiper (Bit)</th><th>R-Ist</th></tr>
                        <tr><td>Widerstand R</td><td>{freq0} &Omega;</td><td>{freq_wiper}</td><td>{bit_2_res(freq_wiper):.1f} &Omega;</td></tr>
                        <tr><td>Güte (Q)</td><td>{Q_val}</td><td>{Q_wiper}</td><td>{bit_2_res(Q_wiper):.1f} &Omega;</td></tr>
                        <tr><td>Verstärkung (H0)</td><td>{H0_val}</td><td>{H0_wiper}</td><td>{bit_2_res(H0_wiper):.1f} &Omega;</td></tr>
                    </table>
                </div>

                <div class="card">
                    <h2>Frequenzerfassung</h2>
                    <div class="freq-display">{last_measured_freq} Hz</div>
                    <table>
                        <tr><th>Letzte 5 Messungen</th></tr>
                        {history_rows}
                    </table>
                    <p style="text-align:center; color: #666; font-size: 0.8em; margin-top: 30px;">
                        🔄 Automatischer Refresh alle 15 Sekunden
                    </p>
                </div>
            </div>
        </div>
    </body>
    </html>
    """
    
    conn.send('HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n')
    conn.send(html)
    conn.close()
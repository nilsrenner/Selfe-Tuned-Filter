import math
from machine import Pin, SPI
#import machine

import network
import socket
import time


led = Pin("LED", Pin.OUT)

# 1. Start-Check: LED blinkt 5 mal schnell
for _ in range(5):
    led.value(1)
    time.sleep(0.1)
    led.value(0)
    time.sleep(0.1)

led.value(1) # LED bleibt an -> WLAN wird gestartet




###   Initialisierung
# Sollwerte
freq0 = 160  # Bauteilbedingte Grenzfrequenz in Hz
Q_val = 1
H0_val = 1

# Digitalpoti-Parameter
max_step = 255
r_ges = 9.65e3
wiper_r = 4  #2  # wiper_r von ca 70 Ohm


freq_wiper = 0
freq_r     = 0

Q_wiper = 0
Q_r     = 0

H0_wiper = 0
H0_r     = 0


# Werte berechnen
def clamp_and_round(x):
    return int(round(max(0, min(255, x))))

def freq_2_bit(freq0):
    freq_c = 1e-6   #1uF
    #vielleicht einzelne rges für jeden wiper?
    wfreq0 = freq0 * 2 * math.pi
    freq_r = 1/(wfreq0 * freq_c)
    freq_wiper = max_step * (1 - freq_r/r_ges) + wiper_r    # mein R in der Gleichung
    return clamp_and_round(freq_wiper), freq_r                                      

def Q_2_bit(Q_val):
    r_opv = 1000
    Q_r = Q_val * r_opv
    Q_wiper = max_step * (1 - Q_r/r_ges) + wiper_r
    return clamp_and_round(Q_wiper), Q_r

def H0_2_bit(H0_val):
    r_opv = 1000
    H0_r = r_opv/H0_val
    H0_wiper = max_step * (1 - H0_r/r_ges) + wiper_r
    #H0_wiper = int(round(H0_wiper))
    return clamp_and_round(H0_wiper), H0_r

def bit_2_res(bit):
    res = r_ges * (1 - (bit-wiper_r)/max_step)      #vorher bit-wiper_r
    return res

def update_filter(freq0, Q_val, H0_val):
    global freq_wiper, freq_r, Q_wiper, Q_r, H0_wiper, H0_r
    freq_wiper, freq_r = freq_2_bit(freq0)
    Q_wiper,    Q_r    = Q_2_bit(Q_val)
    H0_wiper,   H0_r   = H0_2_bit(H0_val)

    set_wiper0(cs1, freq_wiper)
    set_wiper1(cs1, freq_wiper)
    set_wiper0(cs2, Q_wiper)
    set_wiper1(cs2, H0_wiper)

    print("Filter aktualisiert:")
    print(" freq =", freq0, "->", freq_wiper, "(", bit_2_res(freq_wiper), "Ohm )")
    print(" Q    =", Q_val, "->", Q_wiper,    "(", bit_2_res(Q_wiper),    "Ohm )")
    print(" H0   =", H0_val, "->", H0_wiper,   "(", bit_2_res(H0_wiper),   "Ohm )")


### SPI und Pins Initialisieren
# SPI Channel 0 auf GPIO18/19/16
spi = SPI(0, baudrate=1_000_000, polarity=0, phase=0, bits=8, firstbit=SPI.MSB,
    sck=Pin(18), mosi=Pin(19), miso=Pin(16))

# Chip-Selects (aktiv low)
cs1 = Pin(17, Pin.OUT, value=1) #Mittenfreqzenzbestimmend
cs2 = Pin(20, Pin.OUT, value=1) #Für Q und H0 wiper0 = Q

# Befehlswort aufbauen
def mcp_write(cs_pin, command, value):
    cs_pin.value(0)           # CS low -> Chip wird angesprochen
    spi.write(bytes([command & 0xFF, value & 0xFF]))  # 16 Bit: [Cmd|Data]
    cs_pin.value(1)           # CS high -> Chip wird freigegeben


def set_wiper0(cs_pin, value):  # Immer Wiper0 des Chips
    cmd = 0x00                 # 0000 00xx = Wiper 0 Adresse + Write
    mcp_write(cs_pin, cmd, value)

def set_wiper1(cs_pin, value):  # Immer Wiper1 des Chips  
    cmd = 0x10                 # 0001 00xx = Wiper 1 Adresse + Write
    mcp_write(cs_pin, cmd, value)
    
        
    
    
# eigenes WLAN aufbauen statt WLAN verbinden

ap = network.WLAN(network.AP_IF)
ap.active(True)

ap.config(
    essid="Pico-Filter",
    password="filter123"
)

# Feste IP setzen
ap.ifconfig(("192.168.4.1", "255.255.255.0", "192.168.4.1", "8.8.8.8"))

print("Access Point aktiv")
print("SSID: Pico-Filter")
print("IP:", ap.ifconfig()[0])
time.sleep(1)

#HTTP Server
addr = socket.getaddrinfo("0.0.0.0", 80)[0][-1]
server = socket.socket()
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # sonst startet der gleiche Server beim reupload nicht
server.bind(addr)
server.listen(1)

print("HTTP Server läuft...")
AP_IP = ap.ifconfig()[0]
print("http://%s/filter" % AP_IP)

update_filter(freq0, Q_val, H0_val)


# Frequenzzähler
INPUT_PIN = 21
freq_pin = Pin(INPUT_PIN, Pin.IN, Pin.PULL_DOWN)
pulse_count = 0
last_measured_freq = 0

def handle_interrupt(pin):
    global pulse_count
    pulse_count += 1

freq_pin.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

history = []



###         Mailoop
while True:
    # 1. Torzeit: 1 Sekunde lang Impulse zählen (blockiert hier kurz)
    pulse_count = 0      
    time.sleep(1.0)      
    last_measured_freq = pulse_count
    
    # Historie aktualisieren (neuester Wert oben)
    history.insert(0, last_measured_freq)
    if len(history) > 5:
        history.pop()

    try:
        # Wichtig: Timeout, damit der Loop nicht bei accept() hängen bleibt
        server.settimeout(0.1) 
        client, remote_addr = server.accept()
        request = client.recv(1024).decode()

        if "GET /set?" in request:
            line = request.split("\r\n")[0]
            path = line.split(" ")[1]
            query = path.split("?")[1]
            params = query.split("&")

            for p in params:
                key, value = p.split("=")
                if key == "freq":
                    freq0 = float(value)
                elif key == "Q":
                    Q_val = float(value)
                elif key == "H0":
                    H0_val = float(value)
            
            update_filter(freq0, Q_val, H0_val)

        # HTML für die Frequenz-Tabelle generieren
        history_rows = ""
        for val in history:
            history_rows += f"<tr><td>{val} Hz</td></tr>"

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Pico Filter UI</title>
            <meta charset="UTF-8">
            <style>
                body {{ font-family: sans-serif; margin: 20px; }}
                .layout {{ display: flex; gap: 50px; }}
                table {{ border-collapse: collapse; margin-top: 10px; }}
                th, td {{ border: 1px solid #999; padding: 8px; text-align: center; }}
                th {{ background: #eee; }}
            </style>
        </head>
        <body>
            <h1>Pico Filter Steuerung</h1>

            <div class="layout">
                <div>
                    <h2>Parameter setzen</h2>
                    <form action="/set" method="get">
                        <label>Freq (Hz):</label><br>
                        <input type="number" name="freq" step="1" value="{freq0}"><br><br>
                        <label>Q:</label><br>
                        <input type="number" name="Q" step="0.1" value="{Q_val}"><br><br>
                        <label>H0:</label><br>
                        <input type="number" name="H0" step="0.1" value="{H0_val}"><br><br>
                        <input type="submit" value="Setzen">
                    </form>

                    <h2>Aktuelle Filterwerte</h2>
                    <table>
                        <tr><th>Parameter</th><th>Wert</th><th>Widerstand (Ist)</th></tr>
                        <tr><td>Freq</td><td>{freq0} Hz</td><td>{bit_2_res(freq_wiper):.1f} Ω</td></tr>
                        <tr><td>Q</td><td>{Q_val}</td><td>{bit_2_res(Q_wiper):.1f} Ω</td></tr>
                        <tr><td>H0</td><td>{H0_val}</td><td>{bit_2_res(H0_wiper):.1f} Ω</td></tr>
                    </table>
                </div>

                <div>
                    <h2>Frequenz-Verlauf</h2>
                    <p>Aktuell: <b>{last_measured_freq} Hz</b></p>
                    <table>
                        <tr><th>Letzte 5 Messungen</th></tr>
                        {history_rows}
                    </table>
                    <small>(Seite manuell neu laden für Update)</small>
                </div>
            </div>
        </body>
        </html>
        """

        response = "HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n" + html
        client.send(response)
        client.close()

    except OSError:
        # Kein Client verbunden -> Loop läuft weiter für die nächste Messung
        pass
    except Exception as e:
        print("Fehler im Loop:", e)
        if 'client' in locals():
            client.close()


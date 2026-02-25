# Self-Tuned-Filter

## Kontext
Diese Bachelorarbeit wurde im März 2026 an der **Hochschule Bremen** (Fakultät 4: Elektrotechnik und Informatik) abgegeben. Ziel war das Design, die Simulation und die messtechnische Verifizierung eines analogen, selbsteinstellenden Filters auf Basis eines spannungsgesteuerten Biquad-Filters.

## Projektbeschreibung
Das System passt seine Resonanzfrequenz eigenständig an die anliegende Eingangsfrequenz an. Die zentrale Steuerung übernimmt ein **Raspberry Pi Pico 2 W**, der als digitale Schnittstelle dient.

* **Wissenschaftlicher Kern:** Eigenständige Herleitung und Verifikation der Gleichungen zur Resonanzfrequenz (Korrektur fehlerhafter Angaben im ASLK-PRO Manual).
* **Hardware:** Entwicklung eines PCB für die Umsetzung des Self-Tuned Systems.
* **Software:** MicroPython-Skript zur Steuerung des Filters über eine webbasierte Oberfläche. Nulldurchgangszähler für die Eingangsfrequenzdetektion.
* **Ergebnis:** Für frequenzgebende Widerstände von 1 kΩ wurde die Funktionalität im Bereich von ca. **240 Hz bis über 12 kHz** nachgewiesen. 



---

## Struktur des Repositoriums
Die Quelldaten sind wie folgt strukturiert:

| Ordner / Datei | Inhalt |
| :--- | :--- |
| **`001_Simulation_und_Schaltungsentwurf`** | Datenblätter, Simulationen und PCB-Entwürfe (V1 & V2). |
| **`002_3D_Modell`** | 3D-Modell der PCB-Halterung für den Versuchsaufbau. |
| **`003_Messdaten`** | Rohdaten der Messungen (Oszilloskop und Red Pitaya). |
| **`004_Code`** | MicroPython-Skripts für den Raspberry Pi Pico 2 W. |
| **`005_Dokumentation`** | LaTeX-Quellcode der Arbeit. |
| **`Bachelor_Thesis_Renner_2026.pdf`** | Die Bachelorarbeit in digitaler Form. |

---

## Autor & Prüfer
* **Autor:** Nils Renner
* **Prüfer:** Prof. Dr.-Ing. Mirco Meiners & Prof. Dr. Sören Peik

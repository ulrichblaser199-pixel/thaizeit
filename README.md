# 🕒 ThaiZeit (เวลาไทย)

[![Lizenz: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python: 3.8+](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Plattformen: Linux | Windows | macOS](https://img.shields.io/badge/Platform-Linux%20%7C%20Windows%20%7C%20macOS-brightgreen.svg)](#-plattformunabh%C3%A4ngigkeit)

> **Desktop-Uhr & Kulturkalender mit traditioneller thailändischer Zeitrechnung, Phonetik und Feiertagslexikon.**

**ThaiZeit** ist ein leichtgewichtiges Desktop-Programm auf Basis von Python und Tkinter. Es stellt die aktuelle Uhrzeit und anstehende Kalenderereignisse synchron in **thailändischer Originalschrift**, **lateinischer Lautschrift (Umschrift)** und auf **Deutsch** dar. Ergänzt wird die Anzeige durch ein integriertes Kulturlexikon, das Hintergründe und Traditionen zu thailändischen Feiertagen in 3–4 kompakten Sätzen erklärt.

---

## ✨ Hauptfunktionen

* **Traditionelles 6-Stunden-Zeitsystem:** Korrekte Abbildung der thailändischen Tagesphasen (*Tii* / ตี, *Mong Chao* / โมงเช้า, *Bai* / บ่าย, *Mong Yen* / โมงเย็น, *Thum* / ทุ่ม).
* **Grammatikalisch korrekte Wortbildung:** Automatische Umsetzung aller Zahlen und Minuten in Thai-Wortformen (z. B. *Yii Sip* für 20, *Sip Et* für 11).
* **Vollständige Lautschrift:** Stunde, Minute und Sekunde werden als vollständige Wörter phonetisch ausgeschrieben (ideal zum Erlernen der Aussprache).
* **Buddhistischer Kalender (B.E.):** Automatische Umrechnung des aktuellen Kalenderjahres in die buddhistische Zeitrechnung (z. B. $2026 \rightarrow 2569$ bzw. พ.ศ. ๒๕๖๙).
* **Kulturelles Feiertagslexikon:** Erkennt thailändische Feiertage automatisch anhand von Schlagwörtern in Kalenderdateien und blendet kompakte Hintergrundinformationen zu Riten, Speisen und Traditionen ein.
* **Ganztags- und Heute-Erkennung:** Feiertage am heutigen Tag bleiben den gesamten Kalendertag über sichtbar und werden mit dem Status `[วันนี้ • HEUTE]` hervorgehoben.
* **iCal-Unterstützung (.ics):** Liest lokale Kalenderdateien oder exportierte Google-Kalender ein.
* **Out-of-the-Box lauffähig:** Enthält eine mitgelieferte Kalenderdatei (`beispiel_termine.ics`) für den sofortigen Test ohne manuelle Konfiguration.

---

## 📸 Vorschau

```text
                           วันอาทิตย์
                     วันที่ ๔ ตุลาคม พ.ศ. ๒๕๖๙
             สิบ โมงเช้า สี่สิบแปด นาที สามสิบหก วินาที
  Wan Athit, 4. Tulakhom 2569 (B.E.) • sip mong chao si sip paet nathi, sam sip hok wina-thii
                       [Sonntag, 04.10.2026 • 10:48:36 Uhr]

📅 Nächstes Ereignis & Feiertagsbedeutung • วันสำคัญที่จะมาถึง:
✦ วันอังคาร ๑๓ ตุลาคม ๒๕๖๙ : วันนวมินทรมหาราช
   (Wan Angkhan, 13. Tulakhom • Ganztägig)
   [Dienstag, 13.10.2026 • Ganztägig]

💡 Bedeutung & Tradition für Thais (Wan Nawamintharamaharat • 13. Oktober):
Dieser Gedenktag erinnert an den Todestag von König Bhumibol Adulyadej (Rama IX.), der Thailand
über 70 Jahre lang regierte. Thais tragen an diesem Tag häufig Gelb, halten Gedenkminuten ab und
besuchen Tempel für Verdienstzeremonien (Tham Bun) zu Ehren des unvergessenen Monarchen.
```

*(Ein Screenshot der grafischen Benutzeroberfläche kann als `preview.png` im Repository hinterlegt werden).*

---

## 📁 Projektstruktur

```text
thaizeit/
├── thaizeit.py             # Hauptprogramm mit UI & Kalenderlogik
├── beispiel_termine.ics    # Mitgelieferter Beispielkalender mit Feiertagen
├── requirements.txt        # Python-Abhängigkeiten (icalendar)
├── .gitignore              # Schützt private Kalender vor Uploads
├── LICENSE                 # MIT-Open-Source-Lizenz
└── README.md               # Projektdokumentation
```

---

## 🚀 Installation & Schnellstart

### 1. Repository klonen

```bash
git clone https://github.com/DEIN-BENUTZERNAME/thaizeit.git
cd thaizeit
```

### 2. Abhängigkeiten installieren

Das Programm benötigt Python 3 (ab Version 3.8) und die Bibliothek `icalendar`:

```bash
pip install -r requirements.txt
```

*Hinweis für Linux (Debian, Ubuntu, Raspberry Pi OS): Falls Tkinter noch nicht installiert ist:*
```bash
sudo apt update && sudo apt install python3-tk
```

### 3. Programm starten

```bash
python3 thaizeit.py
```
*(Unter Windows genügt in der Regel `python thaizeit.py` oder ein Doppelklick auf die Datei).*

Beim ersten Start greift das Programm automatisch auf `beispiel_termine.ics` im selben Ordner zu und zeigt das nächste thailändische Fest mit Beschreibung an.

---

## ⚙️ Eigene Kalender einbinden

Um eigene Termine oder synchronisierte Feiertage einzubinden, gibt es zwei einfache Wege:

### Option A: Datei im Projektordner (Empfohlen)
Platziere deine Kalenderdatei einfach als **`kalender.ics`** direkt im Projektordner neben `thaizeit.py`. Das Programm bevorzugt diese Datei automatisch vor den Beispieldaten.

### Option B: Benutzerordner anpassen
In `thaizeit.py` (Zeile 300) können beliebige Pfade hinterlegt werden:

```python
self.kalender_pfade = [
    os.path.join(skript_ordner, "kalender.ics"),
    "~/Thaidatum/kalender.ics",
    "~/Thaidatum/FerienTh.ics",
    "~/Thaidatum/FerienEng.ics"
]
```

*Hinweis zum Datenschutz:* Die Datei `.gitignore` ist so konfiguriert, dass private `.ics`-Dateien (außer der Beispieldatei) bei Git-Commits automatisch ignoriert werden.

---

## 💻 Plattformunabhängigkeit

| Betriebssystem | Besonderheiten & Hinweise |
| :--- | :--- |
| **Linux / Raspberry Pi** | Ideal als Info-Display im Dauerbetrieb (z. B. auf einem Pi-Touchscreen). Standard-Schriftarten (*DejaVu Sans* / *Noto Sans*) werden automatisch genutzt. |
| **Windows** | Nutzt nativ die Systemschriftart **Segoe UI**, die thailändische Zeichen gestochen scharf darstellt. Keine Zusatzinstallationen nötig. |
| **macOS** | Greift automatisch auf Systemschriftarten wie *Helvetica Neue* und *Thonburi* zurück. |

---

## 🎯 Einsatzbereiche

* **Deutsch-thailändische Partnerschaften & Familien:** Gemeinsamer Überblick über Tageszeit, Datum und anstehende Feste.
* **Sprachlernende:** Verinnerlichen der thailändischen Ziffern, Wochentage, Monate und des 6-Stunden-Uhrzeitsystems durch synchrone Lautschrift.
* **Kultureller Leitfaden:** Verstehen, warum thailändische Feiertage zelebriert werden und welche Traditionen damit verbunden sind.
* **Smart Home / Wanduhr:** Leichtgewichtig genug, um rund um die Uhr auf einem Raspberry Pi im Wohnzimmer oder Büro zu laufen.

---

## 📄 Lizenz

Dieses Projekt ist unter der [MIT License](LICENSE) frei verfügbar – Nutzung, Anpassung und Weitergabe sind ausdrücklich erwünscht.
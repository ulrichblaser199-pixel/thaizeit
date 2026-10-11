# 🕒 ThaiZeit (เวลาไทย)

> **Desktop-Uhr & Kulturkalender mit thailändischer Zeitrechnung, Phonetik und Feiertagslexikon.**

Ein leichtgewichtiges Python/Tkinter-Programm, das die aktuelle Systemzeit und bevorstehende iCal-Termine synchron in **thailändischer Originalschrift**, **Lautschrift (Umschrift)** und auf **Deutsch** darstellt. Ergänzt wird die Anzeige durch kulturelle Hintergrundinformationen zu thailändischen Feiertagen.

## ✨ Funktionen

* **Traditionelle Zeitrechnung (6-Stunden-System):** Korrekte Abbildung der thailändischen Tagesphasen (*Tii*, *Mong Chao*, *Bai*, *Mong Yen*, *Thum*).

* **Grammatikalisch korrekte Zahlwörter:** Automatische Umsetzung von Zahlen und Minuten in Thai-Wörter (z. B. Berücksichtigung von *Yii Sip* für 20 oder *Et* für 1).

* **Buddhistischer Kalender (B.E.):** Anzeige des aktuellen Kalenderjahres nach der buddhistischen Zeitrechnung (z. B. $2026 \rightarrow 2569$).

* **Dreisprachige Synopse:** Jede Zeile wird in thailändischen Schriftzeichen, lateinischer Umschrift zur Aussprachehilfe und auf Deutsch ausgegeben.

* **Kulturelles Feiertagslexikon:** Erkennt thailändische Feiertage automatisch und blendet eine kompakte Erklärung (3–4 Sätze) zu Bräuchen, Hintergründen und Traditionen ein.

* **iCal-Unterstützung (.ics):** Liest lokale Kalenderdateien oder synchronisierte Online-Kalender (z. B. Google Kalender) ein und hebt das nächste Event hervor.

## 📸 Vorschau

```
                           วันอาทิตย์
                     วันที่ ๔ ตุลาคม พ.ศ. ๒๕๖๙
                  สิบ โมงเช้า สี่สิบแปด นาที ๐ วินาที
        Wan Athit, 4. Tulakhom 2569 (B.E.) • sip mong chao si sip paet nathi
                       [Sonntag, 04.10.2026 • 10:48:00 Uhr]

📅 Nächstes Ereignis & Feiertagsbedeutung:
✦ วันอังคาร ๑๓ ตุลาคม ๒๕๖๙ • เที่ยงคืน ศูนย์ นาที : วันนวมินทรมหาราช
   (Wan Angkhan, 13. Tulakhom • thiang khuen suun nathi)
   [Dienstag, 13.10.2026 um 00:00 Uhr]

💡 Bedeutung & Tradition für Thais:
Dieser Gedenktag erinnert an den Todestag von König Bhumibol Adulyadej (Rama IX.) ...

```

## 🚀 Voraussetzungen & Installation

### 1. Python-Pakete installieren

Das Programm nutzt Standard-Bibliotheken (`tkinter`, `datetime`, `os`) sowie optional `icalendar` für das Auslesen von Terminen:

```
pip install icalendar

```

*Unter Linux (Debian/Ubuntu/Raspberry Pi OS) kann Tkinter bei Bedarf separat installiert werden:*

```
sudo apt-get install python3-tk

```

### 2. Repository klonen

```
git clone https://github.com/DEIN-BENUTZERNAME/thaizeit.git
cd thaizeit

```

### 3. Kalenderpfade anpassen

Öffne `thaizeit.py` und passe im Bereich `ThaiZeitApp.__init__` deine Kalenderpfade an:

```
self.kalender_pfade = [
    "~/Thaidatum/kalender.ics",
    "~/Thaidatum/FerienTh.ics"
]

```

### 4. Starten

```
python3 thaizeit.py

```

## 💡 Zielgruppe

Dieses Projekt eignet sich besonders für:

* **Deutsch-thailändische Familien und Paare**

* **Sprachlernende**, die das thailändische Uhrzeit- und Kalendersystem verinnerlichen möchten

* **Expats in Thailand**, die anstehende Feiertage und deren Bedeutung im Blick behalten wollen

* **Raspberry-Pi-Projekte** (z. B. als kleiner Info-Monitor oder Nachttisch-Uhr)

## 📄 Lizenz

Dieses Projekt ist unter der [MIT License](LICENSE) frei verfügbar.
#!/usr/bin/env python3
"""
Thaizeit.py
Desktop-Uhr & Kulturkalender zur synchronen Anzeige von aktuellem Datum,
Uhrzeit und iCal-Terminen in thailändischer Schrift, Lautschrift und Deutsch.
"""

__version__ = "0.5.2"
__author__ = "Ulrich Blaser"

import os
import datetime
import tkinter as tk

# Optionaler Import von icalendar mit Fallback-Schutz
try:
    from icalendar import Calendar
    ICAL_VERFUEGBAR = True
except ImportError:
    ICAL_VERFUEGBAR = False

# --- Wörterbücher für thailändische Zeit & Sprache ---

wochentage = {
    0: ("วันจันทร์", "Wan Chan", "Montag"),
    1: ("วันอังคาร", "Wan Angkhan", "Dienstag"),
    2: ("วันพุธ", "Wan Phut", "Mittwoch"),
    3: ("วันพฤหัสบดี", "Wan Pharuehat", "Donnerstag"),
    4: ("วันศุกร์", "Wan Suk", "Freitag"),
    5: ("วันเสาร์", "Wan Sao", "Samstag"),
    6: ("วันอาทิตย์", "Wan Athit", "Sonntag")
}

monate = {
    1: ("มกราคม", "Mokkarakhom", "Januar"),
    2: ("กุมภาพันธ์", "Kumphaphan", "Februar"),
    3: ("มีนาคม", "Minakhom", "März"),
    4: ("เมษายน", "Mesayon", "April"),
    5: ("พฤษภาคม", "Phruetsaphakhom", "Mai"),
    6: ("มิถุนายน", "Mithunayon", "Juni"),
    7: ("กรกฎาคม", "Karakadakhom", "Juli"),
    8: ("สิงหาคม", "Singhakhom", "August"),
    9: ("กันยายน", "Kanyayon", "September"),
    10: ("ตุลาคม", "Tulakhom", "Oktober"),
    11: ("พฤศจิกายน", "Phruetsachikayon", "November"),
    12: ("ธันวาคม", "Thanwakhom", "Dezember")
}

thai_ziffern_map = {
    '0': '๐', '1': '๑', '2': '๒', '3': '๓', '4': '๔',
    '5': '๕', '6': '๖', '7': '๗', '8': '๘', '9': '๙'
}

thai_zahlen = {
    0: "ศูนย์", 1: "หนึ่ง", 2: "สอง", 3: "สาม", 4: "สี่", 5: "ห้า",
    6: "หก", 7: "เจ็ด", 8: "แปด", 9: "เก้า", 10: "สิบ",
    11: "สิบเอ็ด", 12: "สิบสอง"
}

latin_zahlen = {
    0: "suun", 1: "neung", 2: "song", 3: "sam", 4: "si", 5: "ha",
    6: "hok", 7: "jet", 8: "paet", 9: "kao", 10: "sip",
    11: "sip et", 12: "sip song"
}

FEIERTAGE_BEDEUTUNG = [
    {
        "keywords": ["นวมินทร", "nawamin", "navamin", "king bhumibol memorial", "passing of king rama 9", "13 october", "13 oktober", "13. oktober"],
        "name": "Wan Nawamintharamaharat (วันนวมินทรมหาราช • 13. Oktober)",
        "info": "Dieser Gedenktag erinnert an den Todestag von König Bhumibol Adulyadej (Rama IX.), der Thailand über 70 Jahre lang mit außerordentlicher Hingabe regierte. Im Jahr 2023 verlieh das thailändische Königshaus diesem Feiertag offiziell den Ehrennamen 'Wan Nawamintharamaharat' zum ewigen Andenken an seine Verdienste. Thais tragen an diesem Tag häufig Gelb, halten landesweit Gedenkminuten ab und besuchen Tempel für Verdienstzeremonien (Tham Bun) zu Ehren des unvergessenen Monarchen."
    },
    {
        "keywords": ["songkran", "สงกรานต์", "thai new year", "wasserfest"],
        "name": "Songkran (วันสงกรานต์ • Traditionelles Neujahr)",
        "info": "Songkran ist das bedeutendste Familienfest in Thailand und markiert den traditionellen Jahreswechsel. Thais reisen zu ihren Familien, um den Älteren mit duftendem Wasser Respekt zu erweisen und Buddha-Statuen rituell zu reinigen. Die weltbekannten Wasserschlachten auf den Straßen symbolisieren spirituelle Reinigung und das fröhliche Fortspülen von Unglück und Sorgen des alten Jahres."
    },
    {
        "keywords": ["loi krathong", "loy krathong", "ลอยกระทง", "lichterfest"],
        "name": "Loy Krathong (วันลอยกระทง • Lichterfest)",
        "info": "In der Vollmondnacht des 12. Mondmonats lassen Thais kunstvoll geschmückte Flößchen (Krathongs) aus Bananenstauden auf Flüssen und Seen schwimmen. Der Brauch ehrt die Wassergöttin Mae Khongkha und bittet um Verzeihung für die Verschmutzung des Wassers. Zugleich symbolisiert das Davonschwimmen der brennenden Kerzen das Loslassen von Groll, Sorgen und schlechtem Karma."
    },
    {
        "keywords": ["makha bucha", "มาฆบูชา", "magha puja"],
        "name": "Makha Bucha (วันมาฆบูชา)",
        "info": "Dieser hohe buddhistische Feiertag erinnert an die spontane Versammlung von 1.250 erleuchteten Mönchen um den Buddha, ohne vorherige Absprache. Thais besuchen an diesem Tag Tempel, bringen Opfergaben dar (Tham Bun) und hören sich Predigten über die Kernlehren des Buddha an. Am Abend findet die feierliche Wian-Tian-Prozession statt, bei der Gläubige mit Kerzen, Räucherstäbchen und Lotusblumen andächtig das Hauptheiligtum umrunden."
    },
    {
        "keywords": ["visakha bucha", "วิสาขบูชา", "vesak", "wesak"],
        "name": "Visakha Bucha (วันวิสาขบูชา • Höchster Feiertag)",
        "info": "Visakha Bucha gilt als der heiligste Tag des Buddhismus, da er an Geburt, Erleuchtung und das vollkommene Verlöschen (Parinirvana) Buddhas am selben Vollmondtag erinnert. Gläubige in ganz Thailand verbringen den Tag mit Meditation, dem Befolgen der buddhistischen Tugendregeln und großzügigen Spenden. Abends versammeln sich Millionen Thais zu stimmungsvollen Lichterprozessionen um die Tempel."
    },
    {
        "keywords": ["asahna bucha", "อาสาฬหบูชา", "asalha puja"],
        "name": "Asahna Bucha (วันอาสาฬหบูชา)",
        "info": "Der Feiertag gedenkt der allerersten Lehrrede Buddhas über die 'Vier Edlen Wahrheiten' und der Gründung der ersten Mönchsgemeinschaft (Sangha). Damit vollendete sich das 'Dreifache Juwel' aus Buddha, Dharma und Sangha. Für Thais ist dies ein Tag tiefer Einkehr, an dem viele Gläubige Tempel aufsuchen und sich auf die anschließende Fastenzeit einstimmen."
    },
    {
        "keywords": ["khao phansa", "เข้าพรรษา", "buddhist lent", "regenzeit"],
        "name": "Khao Phansa (วันเข้าพรรษา • Buddhistische Fastenzeit)",
        "info": "Khao Phansa leitet die dreimonatige Regenzeitklausur ein, in der sich Mönche traditionell in ihre Klöster zurückziehen und nicht umherreisen dürfen. Gläubige stiften zu diesem Anlass riesige kunstvoll geschnitzte Wachskerzen und neue Gewänder an die Mönche. Viele Thais nutzen diese dreimonatige Periode für eigene asketische Gelübde, wie etwa den vorübergehenden Verzicht auf Alkohol oder Fleisch."
    },
    {
        "keywords": ["ok phansa", "ออกพรรษา", "end of lent"],
        "name": "Ok Phansa (วันออกพรรษา • Ende der Fastenzeit)",
        "info": "Mit Ok Phansa endet die dreimonatige Regenzeit-Klosterklausur der Mönche. Im ganzen Land feiern die Menschen diesen Tag mit farbenfrohen Prozessionen und der traditionellen Kathina-Zeremonie, bei der den Klöstern neue Mönchsroben dargebracht werden. In manchen Provinzen finden spektakuläre Drachenbootrennen und illuminierte Bootsparaden statt."
    },
    {
        "keywords": ["chakri", "จักรี", "6 april", "6. april"],
        "name": "Chakri-Gedenktag (วันจักรี • 6. April)",
        "info": "An diesem Nationalfeiertag wird der Gründung der herrschenden Chakri-Dynastie und Bangkoks als Hauptstadt im Jahr 1782 durch König Rama I. gedacht. Für Thais verkörpert das Königshaus ein wichtiges Symbol nationaler Einheit und Stabilität. Die Menschen legen Blumen an Monumenten nieder und gedenken der Verdienste aller bisherigen Monarchen für die Unabhängigkeit des Landes."
    },
    {
        "keywords": ["coronation", "ฉัตรมงคล", "krönungstag", "4 mai", "4. mai"],
        "name": "Krönungstag (วันฉัตรมงคล • 4. Mai)",
        "info": "An diesem Feiertag gedenkt das Land der offiziellen Krönungszeremonie von König Maha Vajiralongkorn (Rama X.). Regierungsgebäude und Straßen werden landesweit festlich mit königlichen Symbolen, gelben Stoffen und Porträts geschmückt. Thais bekunden an diesem Tag ihren Respekt gegenüber der Monarchie und dem amtierenden Staatsoberhaupt."
    },
    {
        "keywords": ["king rama x", "rama 10", "vajiralongkorn", "วชิราลงกรณ", "เฉลิมพระชนมพรรษา ร.10", "28 juli", "28. juli", "28 july"],
        "name": "Geburtstag von König Rama X. (28. Juli)",
        "info": "Der Geburtstag des amtierenden Königs ist ein hoher Nationalfeiertag in Thailand. Das Volk ehrt den Monarchen durch das Tragen von Gelb (der Farbe des Montags, an dem der König geboren wurde) sowie durch religiöse Verdienstzeremonien. Landesweit organisieren Bürger und Behörden gemeinnützige Hilfsaktionen und Freiwilligenarbeit im Dienst der Allgemeinheit."
    },
    {
        "keywords": ["queen sirikit", "muttertag", "mother's day", "วันแม่", "12 august", "12. august"],
        "name": "Muttertag & Geburtstag der Königinmutter (12. August)",
        "info": "Zu Ehren von Königinmutter Sirikit wird ihr Geburtstag zugleich als nationaler Muttertag gefeiert. Kinder knien an diesem Tag traditionell vor ihren Müttern nieder und überreichen weiße Jasminblüten als Zeichen bedingungsloser und reiner Dankbarkeit. Im ganzen Land hängen hellblaue Flaggen (ihre Geburtsfarbe), und Tempel werden für familiäre Segnungen besucht."
    },
    {
        "keywords": ["chulalongkorn", "ปิยมหาราช", "จุฬาลงกรณ์", "rama 5", "23 oktober", "23. oktober", "23 october"],
        "name": "Chulalongkorn-Tag (วันปิยมหาราช • 23. Oktober)",
        "info": "Dieser Gedenktag ehrt König Rama V. (Chulalongkorn), der als einer der größten Herrscher Thailands gilt. Ihm gelang es durch geschickte Diplomatie und Reformen, die Kolonisierung des Landes abzuwenden sowie die Sklaverei friedlich abzuschaffen. Thais bringen an seinen Standbildern rosafarbene Rosen dar, um ihre Dankbarkeit für die Modernisierung des Landes zu zeigen."
    },
    {
        "keywords": ["bhumibol", "rama 9", "vatertag", "father's day", "วันพ่อ", "5 dezember", "5. dezember", "5 december"],
        "name": "Nationalfeiertag & Geburtstag König Bhumibol (5. Dezember)",
        "info": "Der 5. Dezember war der Geburtstag des 2016 verstorbenen, tief verehrten Königs Bhumibol Adulyadej und ist Thailands Nationalfeiertag sowie Vatertag. Kinder ehren ihre Väter mit gelben Canna-Blumen, während das Land die über 4.000 königlichen Entwicklungsprojekte des Monarchen würdigt. Gelbe Kleidung drückt bis heute die tiefe Dankbarkeit und Verbundenheit vieler Thais mit ihm aus."
    },
    {
        "keywords": ["constitution", "รัฐธรรมนูญ", "10 dezember", "10. dezember", "10 december"],
        "name": "Verfassungstag (วันรัฐธรรมนูญ • 10. Dezember)",
        "info": "Der Verfassungstag erinnert an den Übergang Thailands von der absoluten zur konstitutionellen Monarchie im Jahr 1932 durch König Rama VII. (Prajadhipok). Der Tag würdigt das Zustandekommen der ersten dauerhaften Verfassung des Landes. Viele Thais nutzen diesen Feiertag für Familienausflüge sowie das Gedenken an die Entwicklung der Demokratie in Thailand."
    },
    {
        "keywords": ["new year", "neujahr", "ปีใหม่", "silvester", "สิ้นปี", "1. januar"],
        "name": "Neujahrstag (วันขึ้นปีใหม่ • 1. Januar)",
        "info": "Neben Songkran im April wird auch der internationale Jahreswechsel in Thailand als Feiertag begangen. Thais beginnen den 1. Januar meist frühmorgens im Tempel mit Gaben an Mönche, um das Jahr mit gutem Karma und Segen zu starten. Anschließend besuchen Familien gemeinsam heilige Schreine und verbringen Zeit im Kreis der Verwandten."
    }
]


def suche_feiertags_info(summary, ics_desc=""):
    """Sucht nach passender Beschreibung im Feiertags-Lexikon oder nutzt Kalendernotizen."""
    suchtext = f"{summary} {ics_desc}".lower()
    for eintrag in FEIERTAGE_BEDEUTUNG:
        for kw in eintrag["keywords"]:
            if kw in suchtext:
                return {
                    "titel": eintrag["name"],
                    "text": eintrag["info"]
                }

    if ics_desc and len(ics_desc.strip()) > 20:
        return {
            "titel": "Kalender-Notiz / Information",
            "text": ics_desc.strip()
        }
    return None


def arabisch_zu_thai_ziffern(zahl):
    """Wandelt arabische Ziffern (0-9) in traditionelle Thai-Ziffern um."""
    return ''.join(thai_ziffern_map.get(ch, ch) for ch in str(zahl))


def zahl_zu_thai(n):
    """Wandelt Zahlen von 0 bis 59 in grammatikalisch korrekte Thai-Wörter um."""
    if n == 0:
        return "ศูนย์"
    if n <= 10:
        return thai_zahlen[n]
    if n < 20:
        return "สิบเอ็ด" if n == 11 else "สิบ" + thai_zahlen[n - 10]

    zehner = n // 10
    einer = n % 10
    zehner_text = "ยี่สิบ" if zehner == 2 else thai_zahlen[zehner] + "สิบ"

    if einer == 0:
        return zehner_text
    elif einer == 1:
        return zehner_text + "เอ็ด"
    return zehner_text + thai_zahlen[einer]


def zahl_zu_latin(n):
    """Wandelt Zahlen von 0 bis 59 in Lautschrift-Wörter um."""
    if n == 0:
        return "suun"
    if n <= 10:
        return latin_zahlen[n]
    if n < 20:
        return "sip et" if n == 11 else "sip " + latin_zahlen[n - 10]

    zehner = n // 10
    einer = n % 10
    zehner_text = "yi sip" if zehner == 2 else latin_zahlen[zehner] + " sip"

    if einer == 0:
        return zehner_text
    elif einer == 1:
        return zehner_text + " et"
    return f"{zehner_text} {latin_zahlen[einer]}"


def hour_thai(stunde):
    """Formatiert die Stunde gemäß dem traditionellen thailändischen 6-Stunden-Zeitsystem."""
    if stunde == 0:
        return "เที่ยงคืน"
    elif 1 <= stunde <= 5:
        return f"ตี {thai_zahlen[stunde]}"
    elif 6 == stunde:
        return "หกโมงเช้า"
    elif 7 <= stunde <= 10:
        return f"{thai_zahlen[stunde]} โมงเช้า"
    elif stunde == 11:
        return "สิบเอ็ดโมงเช้า"
    elif stunde == 12:
        return "เที่ยง"
    elif 13 <= stunde <= 15:
        diff = stunde - 12
        return "บ่ายโมง" if diff == 1 else f"บ่าย {thai_zahlen[diff]} โมง"
    elif 16 <= stunde <= 18:
        return f"{thai_zahlen[stunde - 12]} โมงเย็น"
    else:
        thum = stunde - 18
        return "หนึ่งทุ่ม" if thum == 1 else f"{thai_zahlen[thum]} ทุ่ม"


def hour_latin(stunde):
    """Gibt die Stunde im thailändischen System als Lautschrift wieder."""
    if stunde == 0:
        return "thiang khuen"
    elif 1 <= stunde <= 5:
        return f"dtii {latin_zahlen[stunde]}"
    elif stunde == 6:
        return "hok mong chao"
    elif 7 <= stunde <= 10:
        return f"{latin_zahlen[stunde]} mong chao"
    elif stunde == 11:
        return "sip et mong chao"
    elif stunde == 12:
        return "thiang"
    elif 13 <= stunde <= 15:
        diff = stunde - 12
        return "bai mong" if diff == 1 else f"bai {latin_zahlen[diff]} mong"
    elif 16 <= stunde <= 18:
        return f"{latin_zahlen[stunde - 12]} mong yen"
    else:
        thum = stunde - 18
        return "neung thum" if thum == 1 else f"{latin_zahlen[thum]} thum"


def aktuelles_datum_zeit():
    """Liest die aktuelle Systemzeit aus und erzeugt Thai-, Lautschrift- und DE-Daten."""
    jetzt = datetime.datetime.now()
    buddhist_jahr = jetzt.year + 543  # Thailändisches Kalenderjahr (B.E.)

    wochentag_thai, wochentag_latin, wochentag_de = wochentage[jetzt.weekday()]
    monat_thai, monat_latin, monat_de = monate[jetzt.month]

    tag_thai = arabisch_zu_thai_ziffern(jetzt.day)
    jahr_thai = arabisch_zu_thai_ziffern(buddhist_jahr)
    stunde_thai = hour_thai(jetzt.hour)
    min_thai_text = zahl_zu_thai(jetzt.minute)
    sek_thai = arabisch_zu_thai_ziffern(jetzt.second)

    thai_daten = {
        "weekday": wochentag_thai,
        "date": f"วันที่ {tag_thai} {monat_thai} พ.ศ. {jahr_thai}",
        "time": f"{stunde_thai} {min_thai_text} นาที {sek_thai} วินาที"
    }

    thai_latin = {
        "weekday": wochentag_latin,
        "date": f"{jetzt.day}. {monat_latin} {buddhist_jahr} (B.E.)",
        "time": f"{hour_latin(jetzt.hour)} {zahl_zu_latin(jetzt.minute)} nathi, {zahl_zu_latin(jetzt.second)} wina-thii"
    }

    de_daten = {
        "weekday": wochentag_de,
        "date": jetzt.strftime("%d.%m.%Y"),
        "time": jetzt.strftime("%H:%M:%S Uhr")
    }

    return thai_daten, thai_latin, de_daten


def to_local_naive_datetime(dt):
    """Wandelt Zeitzonen-fähige datetimes und Ganztags-Dates sicher in lokale naive datetime um."""
    if isinstance(dt, datetime.datetime):
        if dt.tzinfo is not None:
            return dt.astimezone().replace(tzinfo=None)
        return dt
    elif isinstance(dt, datetime.date):
        return datetime.datetime.combine(dt, datetime.time.min)
    return datetime.datetime.now()


def ersetze_jahr_sicher(dt, ziel_jahr):
    """Setzt ein Datum oder Datetime sicher auf ein neues Jahr (inkl. 29. Februar Fallback)."""
    try:
        return dt.replace(year=ziel_jahr)
    except ValueError:
        return dt.replace(year=ziel_jahr, month=2, day=28)


def lade_mehrere_kalender_dateien(pfade):
    """Lädt mehrere .ics-Dateien ein und ignoriert nicht vorhandene Pfade tolerant."""
    kalenders = []
    if not ICAL_VERFUEGBAR:
        return kalenders

    for pfad in pfade:
        aufgeloester_pfad = os.path.expanduser(pfad)
        if not os.path.isfile(aufgeloester_pfad):
            continue
        try:
            with open(aufgeloester_pfad, 'r', encoding='utf-8') as f:
                cal = Calendar.from_ical(f.read())
                kalenders.append(cal)
        except Exception as e:
            print(f"Hinweis: Kalenderdatei '{aufgeloester_pfad}' konnte nicht gelesen werden: {e}")

    return kalenders


def termine_naechste(kalenders, anzahl=1):
    """
    Ermittelt das nächste bevorstehende Event (inkl. Unterstützung für ganztägige
    Feiertage am heutigen Tag sowie jährlich wiederkehrende RRULE-Einträge).
    """
    jetzt = datetime.datetime.now()
    heute_datum = jetzt.date()
    bevorstehende = []

    for calendar in kalenders:
        try:
            for komponent in calendar.walk():
                if komponent.name == "VEVENT":
                    dtstart = komponent.get('dtstart')
                    if not dtstart:
                        continue

                    val = dtstart.dt
                    is_ganztaegig = isinstance(val, datetime.date) and not isinstance(val, datetime.datetime)
                    start_dt = to_local_naive_datetime(val)

                    dtend = komponent.get('dtend')
                    end_dt = to_local_naive_datetime(dtend.dt) if dtend else start_dt

                    rrule = komponent.get('rrule')
                    ist_jaehrlich = False
                    if rrule and 'FREQ' in rrule:
                        freqs = [str(f).upper() for f in rrule['FREQ']]
                        if 'YEARLY' in freqs:
                            ist_jaehrlich = True

                    if ist_jaehrlich:
                        dauer = end_dt - start_dt
                        start_dt = ersetze_jahr_sicher(start_dt, jetzt.year)
                        if (is_ganztaegig and start_dt.date() < heute_datum) or (not is_ganztaegig and start_dt + dauer < jetzt):
                            start_dt = ersetze_jahr_sicher(start_dt, jetzt.year + 1)
                        end_dt = start_dt + dauer

                    summary = str(komponent.get('summary', 'Ohne Titel'))
                    description = str(komponent.get('description', '')).strip()

                    if is_ganztaegig:
                        if start_dt.date() >= heute_datum:
                            bevorstehende.append((start_dt, summary, description, is_ganztaegig))
                    elif end_dt >= jetzt:
                        bevorstehende.append((start_dt, summary, description, is_ganztaegig))
        except Exception as e:
            print(f"Fehler beim Parsen von Kalenderkomponente: {e}")

    bevorstehende.sort(key=lambda x: x[0])
    naechste = bevorstehende[:anzahl]

    if not naechste:
        if not ICAL_VERFUEGBAR:
            return [{"hinweis": "Das Python-Modul 'icalendar' ist nicht installiert.\nBitte führe 'pip install icalendar' im Terminal aus."}]
        if not kalenders:
            return [{"hinweis": "Keine aktiven .ics-Kalenderdateien gefunden.\n(Lege 'kalender.ics' im Skriptordner ab oder passe 'kalender_pfade' an)"}]
        return [{"hinweis": "Keine anstehenden Termine in nächster Zeit."}]

    ergebnis = []
    for dt, summe, beschreibung, ganztaegig in naechste:
        w_thai, w_latin, w_de = wochentage[dt.weekday()]
        m_thai, m_latin, m_de = monate[dt.month]

        t_thai = arabisch_zu_thai_ziffern(dt.day)
        j_thai = arabisch_zu_thai_ziffern(dt.year + 543)

        ist_heute = (dt.date() == heute_datum)

        if ganztaegig:
            status_tag = " [วันนี้ • HEUTE]" if ist_heute else ""
            zeile1 = f"✦{status_tag} {w_thai} {t_thai} {m_thai} {j_thai} : {summe}"
            zeile2 = f"   ({w_latin}, {dt.day}. {m_latin} • Ganztägig)"
            zeile3 = f"   [{w_de}, {dt.strftime('%d.%m.%Y')} • Ganztägig]"
        else:
            zeit_thai = f"{hour_thai(dt.hour)} {zahl_zu_thai(dt.minute)} นาที"
            zeit_lat = f"{hour_latin(dt.hour)} {zahl_zu_latin(dt.minute)} nathi"
            status_tag = " [วันนี้ • HEUTE]" if ist_heute else ""
            zeile1 = f"✦{status_tag} {w_thai} {t_thai} {m_thai} {j_thai} • {zeit_thai} : {summe}"
            zeile2 = f"   ({w_latin}, {dt.day}. {m_latin} • {zeit_lat})"
            zeile3 = f"   [{w_de}, {dt.strftime('%d.%m.%Y um %H:%M')} Uhr]"

        info = suche_feiertags_info(summe, beschreibung)

        ergebnis.append({
            "thai": zeile1,
            "latin": zeile2,
            "german": zeile3,
            "info": info
        })

    return ergebnis


class ThaiZeitApp:
    def __init__(self, root):
        self.root = root
        self.root.title(f"Thai Zeit & Kalender v{__version__} • เวลาไทย")
        self.root.geometry("920x720")
        self.root.minsize(760, 560)
        self.root.configure(bg="#0f172a")

        skript_ordner = os.path.dirname(os.path.abspath(__file__))
        self.kalender_pfade = [
            os.path.join(skript_ordner, "kalender.ics"),
            os.path.join(skript_ordner, "beispiel_termine.ics"),
            "~/Thaidatum/kalender.ics",
            "~/Thaidatum/FerienTh.ics",
            "~/Thaidatum/FerienEng.ics"
        ]
        self.alle_kalender = lade_mehrere_kalender_dateien(self.kalender_pfade)

        self._init_ui()
        self._aktualisiere_uhrzeit()
        self._aktualisiere_termine()

    def _init_ui(self):
        main_frame = tk.Frame(self.root, bg="#0f172a", padx=25, pady=20)
        main_frame.pack(fill="both", expand=True)

        card_time = tk.Frame(main_frame, bg="#1e293b", relief="flat", highlightthickness=1, highlightbackground="#334155")
        card_time.pack(fill="x", pady=(0, 15), ipady=12)

        self.lbl_thai_weekday = tk.Label(card_time, text="", font=("Segoe UI", 26, "bold"), fg="#38bdf8", bg="#1e293b")
        self.lbl_thai_weekday.pack(pady=(5, 2))

        self.lbl_thai_date = tk.Label(card_time, text="", font=("Segoe UI", 18), fg="#e2e8f0", bg="#1e293b")
        self.lbl_thai_date.pack(pady=2)

        self.lbl_thai_time = tk.Label(card_time, text="", font=("Segoe UI", 22, "bold"), fg="#4ade80", bg="#1e293b")
        self.lbl_thai_time.pack(pady=(2, 8))

        sub_info_frame = tk.Frame(card_time, bg="#1e293b")
        sub_info_frame.pack(fill="x", padx=15, pady=4)

        self.lbl_latin = tk.Label(sub_info_frame, text="", font=("Segoe UI", 12), fg="#94a3b8", bg="#1e293b")
        self.lbl_latin.pack()

        self.lbl_german = tk.Label(sub_info_frame, text="", font=("Segoe UI", 11, "italic"), fg="#64748b", bg="#1e293b")
        self.lbl_german.pack(pady=(2, 0))

        card_cal = tk.Frame(main_frame, bg="#1e293b", relief="flat", highlightthickness=1, highlightbackground="#334155")
        card_cal.pack(fill="both", expand=True, ipady=10)

        header_cal = tk.Frame(card_cal, bg="#1e293b")
        header_cal.pack(fill="x", padx=15, pady=(10, 5))

        tk.Label(
            header_cal,
            text="📅 Nächstes Ereignis & Feiertagsbedeutung • วันสำคัญที่จะมาถึง",
            font=("Segoe UI", 15, "bold"),
            fg="#f8fafc",
            bg="#1e293b"
        ).pack(side="left")

        self.txt_termine = tk.Text(
            card_cal,
            bg="#1e293b",
            relief="flat",
            highlightthickness=0,
            padx=20,
            pady=10,
            wrap="word",
            cursor="arrow"
        )
        self.txt_termine.pack(fill="both", expand=True)

        self.txt_termine.tag_configure("thai", font=("Segoe UI", 15, "bold"), foreground="#38bdf8")
        self.txt_termine.tag_configure("latin", font=("Segoe UI", 11), foreground="#94a3b8")
        self.txt_termine.tag_configure("german", font=("Segoe UI", 11, "italic"), foreground="#64748b")
        self.txt_termine.tag_configure("info_header", font=("Segoe UI", 12, "bold"), foreground="#f59e0b")
        self.txt_termine.tag_configure("info_body", font=("Segoe UI", 11), foreground="#cbd5e1", spacing1=4, spacing3=6)
        self.txt_termine.tag_configure("hinweis", font=("Segoe UI", 12), foreground="#94a3b8")

    def _aktualisiere_uhrzeit(self):
        try:
            thai, latin, de = aktuelles_datum_zeit()

            self.lbl_thai_weekday.config(text=thai["weekday"])
            self.lbl_thai_date.config(text=thai["date"])
            self.lbl_thai_time.config(text=thai["time"])

            self.lbl_latin.config(
                text=f"{latin['weekday']}, {latin['date']} • {latin['time']}"
            )
            self.lbl_german.config(
                text=f"[{de['weekday']}, {de['date']} • {de['time']}]"
            )
        except Exception as err:
            print(f"Fehler bei Uhrzeit-Update: {err}")

        self.root.after(1000, self._aktualisiere_uhrzeit)

    def _aktualisiere_termine(self):
        try:
            self.alle_kalender = lade_mehrere_kalender_dateien(self.kalender_pfade)
            termine = termine_naechste(self.alle_kalender, anzahl=1)

            self.txt_termine.config(state="normal")
            self.txt_termine.delete("1.0", tk.END)

            for eintrag in termine:
                if "hinweis" in eintrag:
                    self.txt_termine.insert(tk.END, eintrag["hinweis"] + "\n\n", "hinweis")
                else:
                    self.txt_termine.insert(tk.END, eintrag["thai"] + "\n", "thai")
                    self.txt_termine.insert(tk.END, eintrag["latin"] + "\n", "latin")
                    self.txt_termine.insert(tk.END, eintrag["german"] + "\n\n", "german")

                    if eintrag.get("info"):
                        info = eintrag["info"]
                        self.txt_termine.insert(tk.END, f"💡 Bedeutung & Tradition für Thais ({info['titel']}):\n", "info_header")
                        self.txt_termine.insert(tk.END, f"{info['text']}\n\n", "info_body")

            self.txt_termine.config(state="disabled")
        except Exception as err:
            self.txt_termine.config(state="normal")
            self.txt_termine.delete("1.0", tk.END)
            self.txt_termine.insert(tk.END, f"Fehler beim Aktualisieren der Termine:\n{err}", "hinweis")
            self.txt_termine.config(state="disabled")

        self.root.after(60000, self._aktualisiere_termine)


if __name__ == "__main__":
    app_root = tk.Tk()
    app = ThaiZeitApp(app_root)
    app_root.mainloop()
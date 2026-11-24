# Sensor Data Analyse

Een Python-programma dat sensormetingen simuleert (of inlaadt uit een CSV-bestand), ze analyseert met NumPy en de resultaten laat zien in grafieken met Matplotlib.

## Wat doet het programma?

- **Menu:** kies tussen nieuwe metingen maken of metingen inladen uit een bestaand CSV-bestand.
- **Invoer:** vraagt naar het type sensor, het aantal metingen, de laagste en hoogste meetwaarde en de alarmgrens.
- **Metingen maken:** genereert willekeurige metingen met de `random`-module. Door `random.seed(42)` zijn de resultaten elke keer hetzelfde (reproduceerbaar).
- **Analyse met NumPy:** aantal metingen, gemiddelde, laagste en hoogste waarde, standaardafwijking en het aantal metingen boven de alarmgrens.
- **Alarm:** laat zien welke metingen boven de alarmgrens komen.
- **Opslaan:** slaat de metingen op in `sensor_readings.csv` met de `csv`-module.
- **Grafieken:**
  - `readings_plot.png`: lijngrafiek van de metingen met de alarmgrens als rode lijn
  - `readings_histogram.png`: histogram van de verdeling van de metingen
- **Foutafhandeling:** het programma loopt niet vast bij tekst in plaats van een getal, 0 of een negatief aantal metingen, een laagste waarde die groter is dan de hoogste, of problemen bij het opslaan of inladen van het CSV-bestand.

## Installatie

Installeer de benodigde packages:

```bash
pip install -r requirements.txt
```

## Gebruik

Start het programma:

```bash
python sensor_monitor.py
```

Kies `1` om nieuwe metingen te maken of `2` om een bestaand CSV-bestand in te laden, en beantwoord daarna de vragen.

## Bestanden

| Bestand | Uitleg |
|---|---|
| `sensor_monitor.py` | Het programma |
| `requirements.txt` | Benodigde packages (numpy, matplotlib) |
| `sensor_readings.csv` | Voorbeeld van gegenereerde metingen |
| `readings_plot.png` | Lijngrafiek van de metingen |
| `readings_histogram.png` | Histogram van de metingen |
import random
import csv
import numpy as np
import matplotlib.pyplot as plt


# ----- Invoer van de gebruiker -----

def ask_float(prompt):
    """Blijf vragen tot de gebruiker een geldig getal invoert."""
    while True:
        text = input(prompt)
        try:
            return float(text)
        except ValueError:
            print("Fout: dat is geen getal. Probeer bijvoorbeeld 12.5")


def ask_positive_int(prompt):
    """Blijf vragen tot de gebruiker een heel getal groter dan 0 invoert."""
    while True:
        text = input(prompt)
        try:
            value = int(text)
        except ValueError:
            print("Fout: vul een heel getal in, bijvoorbeeld 50.")
            continue
        if value <= 0:
            print("Fout: gebruik een getal groter dan 0.")
            continue
        return value


def ask_sensor_type():
    """Vraag het type sensor; mag niet leeg zijn."""
    sensor_type = input("Welk type sensor? (bijv. temperatuur, licht): ").strip()
    while sensor_type == "":
        print("Fout: het sensortype mag niet leeg zijn.")
        sensor_type = input("Welk type sensor?: ").strip()
    return sensor_type


def get_user_input():
    """Vraag alle instellingen aan de gebruiker en geef ze terug."""
    sensor_type = ask_sensor_type()
    count = ask_positive_int("Hoeveel metingen wil je maken?: ")

    while True:
        min_value = ask_float("Laagste meetwaarde: ")
        max_value = ask_float("Hoogste meetwaarde: ")
        if min_value < max_value:
            break
        print("Fout: de laagste waarde moet kleiner zijn dan de hoogste. Probeer opnieuw.")

    threshold = ask_float("Vanaf welke waarde moet er een alarm komen?: ")

    return sensor_type, count, min_value, max_value, threshold


# ----- Metingen genereren -----

def generate_sensor_readings(count, min_value, max_value):
    """Maak 'count' willekeurige metingen tussen min_value en max_value."""
    random.seed(42)
    readings = []
    for _ in range(count):
        value = random.uniform(min_value, max_value)
        readings.append(round(value, 2))
    return np.array(readings)


# ----- Analyse met NumPy -----

def calculate_statistics(readings, threshold):
    """Bereken de statistieken en geef ze terug in een dictionary."""
    stats = {
        "count": len(readings),
        "mean": np.mean(readings),
        "min": np.min(readings),
        "max": np.max(readings),
        "std": np.std(readings),
        "above_threshold": int(np.sum(readings > threshold)),
    }
    return stats


def find_outliers(readings, threshold):
    """Geef een lijst van (metingnummer, waarde) voor metingen boven de drempel."""
    outliers = []
    for index, value in enumerate(readings):
        if value > threshold:
            outliers.append((index + 1, value))
    return outliers


def print_statistics(stats, sensor_type, threshold):
    """Laat de statistieken zien."""
    print(f"\n===== Resultaten {sensor_type}sensor =====")
    print(f"Aantal metingen:      {stats['count']}")
    print(f"Gemiddelde:           {stats['mean']:.2f}")
    print(f"Laagste meting:       {stats['min']:.2f}")
    print(f"Hoogste meting:       {stats['max']:.2f}")
    print(f"Standaardafwijking:   {stats['std']:.2f}")
    print(f"Boven alarmgrens ({threshold}): {stats['above_threshold']}")


def print_outliers(outliers, threshold):
    """Laat de metingen zien die boven de drempel komen."""
    if len(outliers) == 0:
        print(f"\nGeen enkele meting komt boven de alarmgrens van {threshold}.")
        return
    print(f"\nLet op! Deze metingen komen boven de alarmgrens van {threshold}:")
    for sample_number, value in outliers:
        print(f"  Meting {sample_number}: {value:.2f}")


# ----- Grafieken -----

def plot_readings(readings, threshold, sensor_type):
    """Lijngrafiek van de metingen met de alarmgrens als horizontale lijn."""
    samples = np.arange(1, len(readings) + 1)
    plt.figure(figsize=(10, 5))
    plt.plot(samples, readings, marker="o", linestyle="-", label="Metingen")
    plt.axhline(y=threshold, color="r", linestyle="--", label=f"Alarmgrens ({threshold})")
    plt.title(f"Metingen van de {sensor_type}sensor")
    plt.xlabel("Metingnummer")
    plt.ylabel(f"Waarde ({sensor_type})")
    plt.grid(True)
    plt.legend()
    plt.savefig("readings_plot.png")


def plot_histogram(readings, threshold, sensor_type):
    """Histogram dat laat zien hoe de metingen verdeeld zijn."""
    plt.figure(figsize=(8, 5))
    plt.hist(readings, bins=10, edgecolor="black", label="Metingen")
    plt.axvline(threshold, color="red", linestyle="--", label=f"Alarmgrens ({threshold})")
    plt.title(f"Verdeling van de {sensor_type}metingen")
    plt.xlabel(f"Waarde ({sensor_type})")
    plt.ylabel("Aantal metingen")
    plt.grid(True)
    plt.legend()
    plt.savefig("readings_histogram.png")


# ----- CSV opslaan en inladen -----

def save_readings(readings, filename):
    """Sla de metingen op in een CSV-bestand. Geeft True terug als het lukt."""
    try:
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Sample Number", "Reading"])
            for index, value in enumerate(readings):
                writer.writerow([index + 1, value])
        print(f"\nDe metingen zijn opgeslagen in {filename}.")
        return True
    except OSError as error:
        print(f"\nFout: het CSV-bestand kon niet worden opgeslagen ({error}).")
        return False


def load_readings(filename):
    """Lees metingen uit een CSV-bestand. Geeft een NumPy-array terug, of None als het mislukt."""
    readings = []
    try:
        with open(filename, "r", newline="") as file:
            reader = csv.reader(file)
            next(reader, None)                     # kopregel overslaan
            for row in reader:
                if len(row) < 2:
                    continue                       # lege regels overslaan
                readings.append(float(row[1]))     # kolom 1 = de meetwaarde
    except FileNotFoundError:
        print(f"Fout: het bestand '{filename}' bestaat niet.")
        return None
    except ValueError:
        print(f"Fout: in '{filename}' staat een waarde die geen getal is.")
        return None

    if len(readings) == 0:
        print(f"Fout: '{filename}' bevat geen metingen.")
        return None

    print(f"{len(readings)} metingen ingeladen uit '{filename}'.")
    return np.array(readings)


# ----- Menu -----

def ask_menu_choice():
    """Laat de gebruiker kiezen tussen nieuwe metingen of een CSV inladen."""
    print("\nWat wil je doen?")
    print("  1 - Nieuwe sensormetingen maken")
    print("  2 - Metingen inladen uit een bestaand CSV-bestand")
    while True:
        choice = input("Kies 1 of 2: ").strip()
        if choice == "1" or choice == "2":
            return choice
        print("Fout: typ 1 of 2.")


# ----- Hoofdprogramma -----

def main():
    print("=== Sensor Data Analyse ===")
    choice = ask_menu_choice()

    if choice == "1":
        sensor_type, count, min_value, max_value, threshold = get_user_input()
        readings = generate_sensor_readings(count, min_value, max_value)
        save_readings(readings, "sensor_readings.csv")
    else:
        readings = None
        while readings is None:
            filename = input("Naam van het CSV-bestand (bijv. sensor_readings.csv): ").strip()
            readings = load_readings(filename)
        sensor_type = ask_sensor_type()
        threshold = ask_float("Vanaf welke waarde moet er een alarm komen?: ")

    stats = calculate_statistics(readings, threshold)
    print_statistics(stats, sensor_type, threshold)

    outliers = find_outliers(readings, threshold)
    print_outliers(outliers, threshold)

    plot_readings(readings, threshold, sensor_type)
    plot_histogram(readings, threshold, sensor_type)
    plt.show()


if __name__ == "__main__":
    main()






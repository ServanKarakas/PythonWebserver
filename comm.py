import serial
import json
import datetime
import time

def add_date_to_json(data):
    timestamp = datetime.datetime.now()
    data["time"] = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    data["date"] = timestamp.strftime("%Y-%m-%d")

def remove_old_data(filename, threshold_minutes=60):
    current_time = datetime.datetime.now()

    with open(filename, 'r') as file:
        lines = file.readlines()

    with open(filename, 'w') as file:
        for line in lines:
            try:
                data = json.loads(line)
                entry_time = datetime.datetime.strptime(data['time'], "%Y-%m-%d %H:%M:%S")
                if (current_time - entry_time).total_seconds() < threshold_minutes * 60:
                    file.write(line)
            except json.JSONDecodeError:
                print('Ungültiges JSON-Format:', line)

if __name__ == '__main__':
    ser = serial.Serial(
        port="COM5",
        baudrate=9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS)

    ser.timeout = 0.1  #Setze Timeout auf 0.1 Sekunde

    print("Verbunden mit: " + ser.portstr)

    try:
        time.sleep(15)
        ser.flushInput()  # Eingangspuffer leeren
        print("bereit für Datenempfang")
        while True:
            raw_line = ser.readline().decode('utf-8').strip()
            print("Raw empfangene Zeile:", raw_line)

            if raw_line == "exit":
                print("Exit-Bedingung erfüllt. Verlasse die Schleife.")
                break

            data = {}
            for part in raw_line.split(','):
                try:
                    key, value = part.strip().split(':')
                    data[key.strip()] = int(value.strip())
                except ValueError:
                    print('Ungültiges Datenformat:', raw_line)

            # Vor dem Hinzufügen neuer Daten entferne alte Daten aus der Datei
            remove_old_data("datalog.json")

            # Daten in die aktuelle JSON-Datei schreiben
            with open("data.json", "w") as current_file:
                json.dump(data, current_file)

            # Daten in die Datenlogger-Datei mit Datum und Zeit schreiben
            with open("datalog.json", "a") as datalogger_file:
                add_date_to_json(data)
                datalogger_file.write("\n")
                json.dump(data, datalogger_file)

    except Exception as e:
        print("Fehler beim Lesen vom seriellen Port:", e)

    finally:
        print("Schließe den seriellen Port")
        ser.close()

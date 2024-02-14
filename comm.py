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

    ser.timeout = 0.1  #set timeout to 0.1 sec

    print("Verbunden mit: " + ser.portstr)

    try:
        time.sleep(15)
        ser.flushInput()  # flushes the imput 
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

            # removes the old data befor adding the new one
            remove_old_data("datalog.json")

            # data gets dumped in data json
            with open("data.json", "w") as current_file:
                json.dump(data, current_file)

            # writes data in datalogger with the time and date
            with open("datalog.json", "a") as datalogger_file:
                add_date_to_json(data)
                datalogger_file.write("\n")
                json.dump(data, datalogger_file)

    except Exception as e:
        print("error trying to read serial port:", e)

    finally:
        print("closing serial port")
        ser.close()

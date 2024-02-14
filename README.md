
# ATmega8 Data Web Server

## Description:
This project involves setting up a Python web server that retrieves data from the ATmega8(or ATmega16) microcontroller and displays it on a web page.

## Requirements:
- Python 3.x
- ATmega8 microcontroller
- Web browser

## Installation:
1. Clone or download the project repository to your local machine.
2. Ensure that Python 3.x is installed on your system.
3. Ensure that flask and pyserial is installed.
4. Connect the ATmega8 microcontroller to your computer and ensure it is properly configured to communicate with Python.

## Usage:
1. Navigate to the project directory on your terminal or command prompt.
2. Run the Python web server script using the following command:
    ```
    python webserver.py
    python restserver.py
    python comm.py
    ```
3. Open your web browser and navigate to the specified address (usually http://localhost:8080) to view the data retrieved from the ATmega8.

## Configuration:
- Modify the `webserver.py` script to adjust settings such as port number, data retrieval methods, and webpage layout as per your requirements.
- Modify the `comm.py´ to ajust the COM serial Port.
- Ensure that the ATmega8 is properly configured to send data to the Python web server.
## Webserver
![grafik](https://github.com/ServanKarakas/PythonWebserver/assets/160028333/ad860f25-3d60-46e1-9f75-84043159ae7d)

## License:
This project is not licensed.

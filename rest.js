// Google Charts initialization
google.charts.load('current', {'packages':['corechart']});

$(document).ready(function() {
    // Regelmäßige Aktualisierung alle 2 Sekunden
    setInterval(function () {
        $.ajax({
            url: "http://127.0.0.1:8081/data",
            type: 'GET',
            crossDomain: true,
            dataType: 'json',
            success: function(data) {
                console.log('Erfolgreiche AJAX-Anfrage:', data);
                $("#Current").text(data.Current);
                $("#Voltage").text(data.Voltage);
            },
            error: function(xhr, status, error) {
                console.error('Fehler bei der AJAX-Anfrage:', status, error);
                console.log('Server-Antwort:', xhr.responseText);
            }
        });
        
    }, 2000);
});

// Funktion, um Daten über AJAX abzurufen und das Diagramm zu zeichnen
function getData() {
    // Aktuelle Zeit abrufen
    var currentTime = new Date();

    // Endzeit berechnen (60 Minuten von der aktuellen Zeit)
    var endTime = new Date(currentTime);
    endTime.setMinutes(currentTime.getMinutes() - 60);

    // Konsolenausgabe für die Überprüfung der Werte, funktioniert eh nicht
    console.log("Current Time:", currentTime);
    console.log("End Time:", endTime);
    //Konsolenabfrage weil nix mehr funktioniert, kann das alles nicht mehr

    console.log("AJAX-Anfrage Parameter: ", { time: 60, endTime: endTime.toISOString() });


    // AJAX-Anfrage mit den neuen Parametern
    $.ajax({
        url: "http://127.0.0.1:8081/datalog?time=100",
        type: 'GET',
        crossDomain: true,
        data: { currentTime: currentTime, endTime: endTime},
        dataType: 'json',
        success: function(response) {
            console.log(response);
            drawChart(response);
        },
        error: function(error) {
            console.error('Fehler bei der AJAX-Anfrage:', error);
        }
    });
}


// Funktion, um das Google-Diagramm zu zeichnen
function drawChart(response) {
    console.log('Empfangene Daten:', response);

    var data = new google.visualization.DataTable();
    data.addColumn('datetime', 'time');
    data.addColumn('number', 'Voltage');

    // Füge die Daten zur Tabelle hinzu
    response.forEach(function(item) {
        var tme = new Date(item.time);
        var voltage = parseFloat(item.Voltage);
        data.addRow([time, voltage]);
    });

    var options = {
        title: 'Voltage Over Time',
        legend: { position: 'bottom' },
        hAxis: {
            format: 'HH:mm', // Zeitformat nach Bedarf anpassen
            title: 'Time'
        },
        vAxis: {
            title: 'Voltage'
        }
    };
    var chart = new google.visualization.LineChart(document.getElementById('curve_chart'));
    chart.draw(data, options);
}

// Google Charts Initialisierungsrückruf
google.charts.setOnLoadCallback(getData);

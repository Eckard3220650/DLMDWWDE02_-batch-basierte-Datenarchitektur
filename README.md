# DLMDWWDE02_-batch-basierte-Datenarchitektur
Dieses Projekt hat das Ziel, eine skalierbare und modulare Dateninfrastruktur zur Verarbeitung des Olympic Historical Dataset (1896-2022) zu entwickeln. Die Architektur integriert verschiedene Tools und Technologien, um eine effiziente Datenaufnahme, -speicherung, -verarbeitung und Systemüberwachung zu ermöglichen.

Projektübersicht
Ziel

    Aufbau eines lokalen Datenverarbeitungssystems mithilfe von Docker-Containern.
    Bereitstellung einer flexiblen und skalierbaren Infrastruktur für Batch- und Stream-Verarbeitung.

Datenfluss
1. Datenaufnahme: Die Rohdaten werden mithilfe von Apache Kafka aus APIs oder CSV-Dateien aufgenommen.
2. Speicherung: Die Daten werden in PostgreSQL gespeichert, das hohe Verfügbarkeit und Sicherheit bietet.
3. Batch-Verarbeitung: Apache Spark transformiert und aggregiert große Datenmengen.
4. ETL-Orchestrierung: Apache Airflow verwaltet und plant die Datenprozesse.
5. Protokollierung und Analyse: Der ELK-Stack (Elasticsearch, Logstash, Kibana) verarbeitet System-Logs.
6. Überwachung: Prometheus erfasst Metriken, die in Grafana visualisiert werden.

Systemanforderungen und Konfiguration

Um das System auszuführen, stellen Sie sicher, dass die folgenden Tools installiert und korrekt konfiguriert sind. Befolgen Sie die Anweisungen, um die erforderlichen Programme herunterzuladen und einzurichten.
Voraussetzungen
Tools

    Python
        Version: Python 3.12 .
        Installation: Python herunterladen
        Zusätzliche Anforderungen:
            Stellen Sie sicher, dass pip installiert ist, um die Python-Abhängigkeiten zu verwalten.
            Fügen Sie den Installationspfad von Python (z. B. C:\Python39) zur PATH-Umgebungsvariable hinzu.

    Java Development Kit (JDK) 11
        Wichtig: Für diese Konfiguration ist Java Version 11 zwingend erforderlich. Andere Versionen sind nicht kompatibel.
        Download: Java 11 herunterladen (https://www.oracle.com/java/technologies/downloads/#java11?er=221886)
        Nach der Installation:
            Setzen Sie die Umgebungsvariable JAVA_HOME auf den Installationspfad von Java (z. B. C:\Program Files\Java\jdk-11).
            Fügen Sie %JAVA_HOME%\bin zu Ihrer PATH-Variable hinzu.

    Hadoop 3.2.1
        Download: Hadoop herunterladen (https://hadoop.apache.org/releases.html)
        Nach der Installation:
            Setzen Sie die Umgebungsvariable HADOOP_HOME auf den Installationspfad von Hadoop (z. B. C:\Users\<IhrBenutzername>\hadoop-3.2.1).
            Fügen Sie %HADOOP_HOME%\bin zu Ihrer PATH-Variable hinzu.

    PostgreSQL
        Download: PostgreSQL herunterladen (https://www.postgresql.org/download/)
        Nach der Installation:
            Fügen Sie den Pfad zum PostgreSQL-Binärverzeichnis (z. B. C:\Program Files\PostgreSQL\17\bin) zu Ihrer PATH-Variable hinzu.

    Docker
        Download: Docker Desktop herunterladen (https://www.docker.com/products/docker-desktop/)
        Nach der Installation:
            Fügen Sie den Pfad zum Docker-Binärverzeichnis (z. B. C:\Program Files\Docker\Docker\resources\bin) zu Ihrer PATH-Variable hinzu.


Funktionalität der .bat-Datei. Doppelklicken Sie auf die .bat-Datei um die Ausführung der Pipeline zu starten.

Die .bat-Datei automatisiert die Ausführung der gesamten Datenpipeline. Sie umfasst die folgenden Schritte:
1. Installation der Abhängigkeiten

    Installiert alle erforderlichen Python-Bibliotheken mit pip, darunter:
        pandas für Datenverarbeitung.
        confluent-kafka für die Integration mit Apache Kafka.
        psycopg2 für die Anbindung an PostgreSQL.
        Weitere Bibliotheken wie pyspark, dotenv und Airflow-Provider.
    Dies stellt sicher, dass alle notwendigen Pakete installiert sind, bevor die Pipeline startet.

2. Prüfung der Voraussetzungen

    Überprüft, ob die folgenden Tools installiert und verfügbar sind:
        Docker: Notwendig für die Containerisierung und den Betrieb der Infrastruktur.
        Python: Stellt sicher, dass Python auf dem System vorhanden ist.

3. Initialisierung der Infrastruktur

    Startet die Docker-Container für die Dateninfrastruktur mit docker-compose up.
    Container wie PostgreSQL, Apache Kafka, Apache Spark, Apache Airflow, Prometheus und Grafana werden initialisiert.

4. Ausführung der Pipeline-Schritte

    Schritt 1: Datenimport
        Führt das Skript Daten_Importieren.py aus, um Rohdaten aus CSV-Dateien zu laden.
    Schritt 2: Daten in Kafka laden
        Führt Daten_in_Kafka_laden.py aus, um die Daten in Apache Kafka zu veröffentlichen.
    Schritt 3: Batch-Verarbeitung
        Führt Batch_Verarbeitung_mit_Apache_Spark.py aus, um die Daten mit Apache Spark zu transformieren und aggregieren.
    Schritt 4: Speicherung in PostgreSQL
        Führt Daten_in_PostgreSQL.py aus, um die verarbeiteten Daten in PostgreSQL zu speichern.

Nach jedem Schritt wird überprüft, ob ein Fehler aufgetreten ist. Falls ein Fehler erkannt wird, wird die Pipeline abgebrochen.
5. Shutdown der Infrastruktur

    Nachdem alle Schritte erfolgreich abgeschlossen sind, werden die Docker-Container mit docker-compose down gestoppt, um Ressourcen freizugeben.

6. Benutzerfreundliche Fehlermeldungen

    Gibt verständliche Fehlermeldungen aus, falls ein Schritt fehlschlägt:
        Zum Beispiel: "Fehler beim Import der Daten" oder "Fehler beim Starten von Docker-Compose".
    Der Benutzer wird informiert, an welchem Punkt die Pipeline gestoppt wurde.

Doppelklicken Sie auf die .bat-Datei um die Ausführung der Pipeline zu starten.

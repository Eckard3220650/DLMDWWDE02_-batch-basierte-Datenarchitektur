REM Install the required Python libraries
pip install pandas
pip install confluent-kafka
pip install psycopg2
pip install dotenv
pip install kaggle
pip install pyspark
pip install apache-airflow
pip install apache-airflow-providers-celery
pip install apache-airflow-providers-docker
pip install apache-airflow-providers-postgres

@echo off
setlocal

echo ### Pipeline gestartet ###

REM Setze Pfade und Variablen
set DOCKER_COMPOSE_FILE=docker-compose.yml
set PYTHON_SCRIPTS_DIR=scripts
set TIMEOUT_SECONDS=10

REM Debugging: Verwendete Pfade ausgeben
echo Docker-Compose Datei: %DOCKER_COMPOSE_FILE%
echo Python-Skript-Verzeichnis: %PYTHON_SCRIPTS_DIR%

REM Docker-Compose starten
echo Docker-Compose wird gestartet...
docker-compose -f %DOCKER_COMPOSE_FILE% up -d
IF %ERRORLEVEL% NEQ 0 (
    echo Fehler beim Starten von Docker-Compose. Pipeline wird abgebrochen.
    goto SHUTDOWN
)

REM Warte auf die Initialisierung der Dienste
echo Warte auf die Initialisierung der Dienste...
timeout /t %TIMEOUT_SECONDS% > nul

REM 1. Daten importieren
echo 1. Daten importieren...
python "%PYTHON_SCRIPTS_DIR%\Daten_Importieren.py"
IF %ERRORLEVEL% NEQ 0 (
    echo Fehler beim Import der Daten. Pipeline wird abgebrochen.
    goto SHUTDOWN
)

REM 2. Daten in Kafka laden
echo 2. Daten in Kafka laden...
python "%PYTHON_SCRIPTS_DIR%\Daten_in_Kafka_laden.py"
IF %ERRORLEVEL% NEQ 0 (
    echo Fehler beim Laden der Daten in Kafka. Pipeline wird abgebrochen.
    goto SHUTDOWN
)

REM 3. Batch-Verarbeitung mit Spark
echo 3. Batch-Verarbeitung mit Spark...
python "%PYTHON_SCRIPTS_DIR%\Batch_Verarbeitung_mit_Apache_Spark.py"
IF %ERRORLEVEL% NEQ 0 (
    echo Fehler bei der Batch-Verarbeitung. Pipeline wird abgebrochen.
    goto SHUTDOWN
)

REM 4. Daten in PostgreSQL speichern
echo 4. Daten in PostgreSQL speichern...
python "%PYTHON_SCRIPTS_DIR%\Daten_in_PostgreSQL.py"
IF %ERRORLEVEL% NEQ 0 (
    echo Fehler beim Speichern der Daten in PostgreSQL. Pipeline wird abgebrochen.
    goto SHUTDOWN
)

REM Erfolgreicher Abschluss
echo ### Pipeline erfolgreich abgeschlossen ###
goto SHUTDOWN

:SHUTDOWN
REM Docker-Compose stoppen
echo Docker-Compose wird gestoppt...
docker-compose -f %DOCKER_COMPOSE_FILE% down
pause


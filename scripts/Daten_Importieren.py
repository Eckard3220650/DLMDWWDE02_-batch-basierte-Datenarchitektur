import os
import kaggle

# Stelle sicher, dass die kaggle.json API Datei existiert
if not os.path.exists(os.path.expanduser("~/.kaggle/kaggle.json")):
    raise FileNotFoundError("Die Kaggle API Datei kaggle.json wurde nicht gefunden. Bitte erstelle sie und speichere sie unter ~/.kaggle/kaggle.json")

# Kaggle Dataset-Name (Olympische Medaillen-Datensatz)
dataset = 'piterfm/olympic-games-medals-19862018'

# Verzeichnis, in das die Daten heruntergeladen werden
download_dir = 'olympic_data'

# Stelle sicher, dass das Verzeichnis existiert
os.makedirs(download_dir, exist_ok=True)

# Lade das Dataset herunter
kaggle.api.dataset_download_files(dataset, path=download_dir, unzip=True)

print(f"Dataset heruntergeladen und entpackt in {download_dir}")

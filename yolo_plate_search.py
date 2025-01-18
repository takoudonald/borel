import cv2
import pytesseract
from ultralytics import YOLO
import requests
from datetime import datetime
import os

# Configuration de Tesseract
# pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'

# Simulateur SMS (Flask)
SIMULATOR_URL = "http://127.0.0.1:5000"

# Chargement du modèle YOLOv8
model = YOLO('yolov8n.pt')  # Utilisation du modèle léger

# Dossier de sauvegarde des images
SAVE_DIR = "images_captures"
os.makedirs(SAVE_DIR, exist_ok=True)

# Fonction pour envoyer un SMS via le simulateur
def envoyer_sms(numero, message):
    payload = {"numero": numero, "message": message}
    response = requests.post(f"{SIMULATOR_URL}/send_sms", json=payload)
    if response.status_code == 200:
        print(f"SMS envoyé : {message}")
    else:
        print("Erreur lors de l'envoi du SMS.")

# Fonction pour lire les SMS entrants via le simulateur
def lire_sms():
    response = requests.get(f"{SIMULATOR_URL}/read_sms")
    if response.status_code == 200:
        messages = response.json()
        print(f"Messages reçus : {messages}")
        return messages
    else:
        print("Erreur lors de la lecture des SMS.")
        return []

# Fonction pour détecter les plaques dans une image
def detecter_plaque(frame):
    results = model(frame)  # YOLOv8 détecte les plaques
    plaques_detectees = []

    for result in results:
        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()  # Coordonnées
            conf = box.conf[0].item()  # Confiance
            cls = int(box.cls[0].item())  # Classe

            if cls == 0 and conf > 0.5:  # Classe 0 (hypothétique) pour une plaque
                plaque_crop = frame[int(y1):int(y2), int(x1):int(x2)]
                texte = pytesseract.image_to_string(plaque_crop, config="--psm 7")
                plaques_detectees.append((texte.strip(), (x1, y1, x2, y2)))
    return plaques_detectees

# Fonction principale
def main():
    print("Démarrage du système...")
    plaque_recherchee = None
    video_path = "video_test.mp4"  # Remplacez par le chemin de votre vidéo
    cap = cv2.VideoCapture(video_path)  # Lecture de la vidéo

    if not cap.isOpened():
        print("Erreur : Impossible d'ouvrir la vidéo.")
        return

    while True:
        # Vérifier les SMS entrants
        messages = lire_sms()
        for message in messages:
            contenu = message.get("message", "")
            if "#" in contenu:  # Format attendu : #PLAQUE
                plaque_recherchee = contenu.split("#")[1].strip()
                print(f"Plaque recherchée mise à jour : {plaque_recherchee}")

        # Lire une image de la vidéo
        ret, frame = cap.read()
        if not ret:
            print("Fin de la vidéo.")
            break

        # Détecter les plaques
        plaques_detectees = detecter_plaque(frame)

        # Sauvegarder l'image si des plaques sont détectées
        if plaques_detectees:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(SAVE_DIR, f"capture_{timestamp}.jpg")
            cv2.imwrite(filepath, frame)
            print(f"Image sauvegardée : {filepath}")

            # Vérifier si une plaque correspond à la recherche
            for plaque, coords in plaques_detectees:
                if plaque_recherchee and plaque_recherchee in plaque:
                    maintenant = datetime.now()
                    heure_date = maintenant.strftime("%Y-%m-%d %H:%M:%S")
                    message = (
                        f"Plaque détectée : {plaque}\n"
                        f"Date/Heure : {heure_date}\n"
                        f"Image : {filepath}"
                    )
                    print(f"Correspondance trouvée ! Envoi du SMS : {message}")
                    envoyer_sms("+11234567890", message)  # Remplacez par le numéro cible

        # Afficher la vidéo pour contrôle (facultatif)
        cv2.imshow("Video Test", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):  # Quitter avec 'q'
            break

    # Libérer les ressources
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nArrêt du programme.")
        cv2.destroyAllWindows()

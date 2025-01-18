import cv2
import numpy as np

# Paramètres de la vidéo
video_name = "video_test.mp4"
frame_width = 640
frame_height = 480
fps = 30
duration = 60  # Durée en secondes

# Création de la vidéo
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(video_name, fourcc, fps, (frame_width, frame_height))

# Plaques d'immatriculation simulées
plaques = ["123-ABC", "456-DEF", "789-GHI", "123-JKL 23-ABC", "456-DEF", "789-GHI", "123-JKL"]
colors = [(255, 255, 255), (200, 200, 200), (100, 100, 255), (255, 100, 100), (200, 200, 200), (100, 100, 255), (255, 100, 100)]

# Générer les frames
for frame_id in range(fps * duration):
    frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

    # Ajouter une voiture simulée
    car_color = colors[frame_id % len(colors)]
    car_position = (50 + (frame_id * 5) % (frame_width - 200), 200)
    car_size = (150, 70)
    cv2.rectangle(frame, car_position, (car_position[0] + car_size[0], car_position[1] + car_size[1]), car_color, -1)

    # Ajouter la plaque d'immatriculation
    plaque_text = plaques[frame_id % len(plaques)]
    plaque_position = (car_position[0] + 20, car_position[1] + 40)
    cv2.putText(frame, plaque_text, plaque_position, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    # Sauvegarder la frame dans la vidéo
    out.write(frame)

# Libérer les ressources
out.release()
print(f"Vidéo de test générée : {video_name}")

import cv2
import mediapipe as mp
import numpy as np
from deepface import DeepFace
import json

# Configuração do MediaPipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

def detectar_faces_e_emocoes(frame):
    """
    Detecta rostos no frame e analisa as emoções.
    """
    try:
        resultados = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        rostos = resultados if isinstance(resultados, list) else [resultados]
        deteccoes = []

        for rosto in rostos:
            emocao = rosto['dominant_emotion']
            box = rosto['region']  # Coordenadas do rosto
            deteccoes.append((box, emocao))
        return deteccoes
    except Exception as e:
        return []

def detectar_anomalias(frame_anterior, frame_atual):
    """Detecta anomalias usando fluxo óptico entre dois frames."""
    if frame_anterior is None:
        return False

    prev_gray = cv2.cvtColor(frame_anterior, cv2.COLOR_BGR2GRAY)
    current_gray = cv2.cvtColor(frame_atual, cv2.COLOR_BGR2GRAY)

    fluxo = cv2.calcOpticalFlowFarneback(
        prev_gray, current_gray, None, 0.5, 3, 15, 3, 5, 1.2, 0
    )
    magnitude, _ = cv2.cartToPolar(fluxo[..., 0], fluxo[..., 1])

    # Detecta anomalias com base em um limite de magnitude
    if np.max(magnitude) > 20:  # Limite para movimentos anômalos
        return True
    return False

def detectar_atividade(frame):
    """
    Detecta atividades com base em pontos-chave do corpo.
    """
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    resultado = pose.process(frame_rgb)

    if resultado.pose_landmarks:
        # Obtenha as coordenadas dos pontos de referência
        hip_left = resultado.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_HIP.value]
        hip_right = resultado.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_HIP.value]
        knee_left = resultado.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_KNEE.value]
        knee_right = resultado.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_KNEE.value]
        ankle_left = resultado.pose_landmarks.landmark[mp_pose.PoseLandmark.LEFT_ANKLE.value]
        ankle_right = resultado.pose_landmarks.landmark[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

        # Calcule a altura do quadril e do joelho
        hip_height = (hip_left.y + hip_right.y) / 2
        knee_height = (knee_left.y + knee_right.y) / 2
        ankle_height = (ankle_left.y + ankle_right.y) / 2

        # Identifique a atividade com base na altura dos quadris, joelhos e tornozelos
        if knee_height > hip_height:
            return "Sentado"
        elif knee_height < hip_height - 0.1 and ankle_height < hip_height - 0.2:
            return "Agachado"
        elif ankle_height < hip_height - 0.1:
            return "Em pé"
        elif knee_height < hip_height and ankle_height > hip_height:
            return "Correndo"
        elif knee_height < hip_height and ankle_height < hip_height:
            return "Andando"
        elif knee_height < hip_height and ankle_height > hip_height + 0.1:
            return "Pulando"
        else:
            return "Deitado"

    return "Desconhecida"


def processar_video(caminho_video):
    """
    Processa o vídeo, detectando faces, emoções, atividades e anomalias.
    """
    cap = cv2.VideoCapture(caminho_video)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_atual = 0
    frame_anterior = None
    atividades = []
    emocoes = []
    anomalias_detectadas = 0
    rostos_detectados = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Processa rostos e emoções
        deteccoes = detectar_faces_e_emocoes(frame)
        rostos_detectados += len(deteccoes)
        for _, emocao in deteccoes:
            emocoes.append(emocao)

        # Processa atividades
        atividade = detectar_atividade(frame)
        atividades.append(atividade)

        # Processa anomalias
        if detectar_anomalias(frame_anterior, frame):
            anomalias_detectadas += 1

        frame_anterior = frame.copy()

        frame_atual += 1
        print(f"Processando frame {frame_atual}/{total_frames}...")

    cap.release()

    # Resumo das atividades e emoções
    resumo = {
        "Total de Frames": total_frames,
        "Total de Rostos Detectados": rostos_detectados,
        "Total de Anomalias Detectadas": anomalias_detectadas,
        "Resumo de Emoções": {e: emocoes.count(e) for e in set(emocoes)},
        "Resumo de Atividades": {a: atividades.count(a) for a in set(atividades)},
    }

    # Salva o relatório
    with open('relatorio.json', 'w', encoding='utf-8') as arquivo:
        json.dump(resumo, arquivo, indent=4, ensure_ascii=False)

    print("Processamento concluído. Resumo salvo em 'relatorio.json'.")

if __name__ == "__main__":
    caminho_video = "videos/video.mp4"  # Caminho do vídeo
    processar_video(caminho_video)

"""
# ── Industrial Safety Detector — Gradio App ─────────────────────
# App local para detección de EPP (cascos, chalecos, personas)
# usando el modelo YOLOv8 entrenado en MAIC-1125.
#
# Uso:
#   python src/app.py
#   Abre http://localhost:7860 en el navegador
"""

import os
import numpy as np
import gradio as gr
from PIL import Image
from ultralytics import YOLO
import supervision as sv

# ── Rutas ────────────────────────────────────────────────────────
# Resuelve la ruta al modelo relativa a este script,
# para que funcione sin importar desde dónde se ejecute
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR   = os.path.dirname(SCRIPT_DIR)
MODEL_PATH = os.path.join(ROOT_DIR, "model_weights", "best.pt")

# ── Clases del modelo ─────────────────────────────────────────────
# Orden exacto definido en configs/data.yaml
CLASS_NAMES = {
    0: "helmet",
    1: "no helmet",
    2: "no vest",
    3: "person",
    4: "vest",
}

# Clases de riesgo (se muestran en rojo en la imagen anotada)
DANGER_CLASSES = {1, 2}  # no helmet, no vest

# ── Colores por clase ─────────────────────────────────────────────
# supervision usa BGR → (B, G, R)
CLASS_COLORS = {
    0: sv.Color(r=0,   g=200, b=0),    # helmet    → verde
    1: sv.Color(r=220, g=0,   b=0),    # no helmet → rojo
    2: sv.Color(r=220, g=0,   b=0),    # no vest   → rojo
    3: sv.Color(r=50,  g=120, b=220),  # person    → azul
    4: sv.Color(r=0,   g=200, b=0),    # vest      → verde
}

# ── Carga del modelo ──────────────────────────────────────────────
# Se carga una única vez al arrancar la app para evitar latencia
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(
        f"[app.py] No se encontró el modelo en: {MODEL_PATH}\n"
        f"Asegúrate de que 'model_weights/best.pt' existe en la raíz del proyecto."
    )

print(f"\033[96mℹ️  Cargando modelo desde: {MODEL_PATH}\033[0m")
model = YOLO(MODEL_PATH)
print("\033[92m✅ Modelo cargado correctamente\033[0m")


# ── Función de detección ──────────────────────────────────────────
# Recibe una imagen PIL, corre inferencia y devuelve:
#   - imagen PIL anotada con bounding boxes
#   - texto con el resumen de detecciones
def detect(image: Image.Image) -> tuple[Image.Image, str]:
    if image is None:
        return None, "⚠️  No se recibió ninguna imagen."

    # Inferencia
    results = model.predict(image, verbose=False)[0]

    # Convertir a formato supervision
    detections = sv.Detections.from_ultralytics(results)

    if len(detections) == 0:
        return image, "ℹ️  No se detectaron objetos en la imagen."

    # ── Anotar imagen ─────────────────────────────────────────────
    # Usamos un anotador por cada clase para aplicar colores individuales
    image_np = np.array(image)
    annotated = image_np.copy()

    # Crear mapa de colores por detección
    colors_per_detection = [
        CLASS_COLORS.get(int(cls), sv.Color.WHITE)
        for cls in detections.class_id
    ]

    # Dibujar bounding boxes con color por detección
    for i, (box, cls_id, conf) in enumerate(zip(
        detections.xyxy,
        detections.class_id,
        detections.confidence
    )):
        color = CLASS_COLORS.get(int(cls_id), sv.Color(r=255, g=255, b=255))
        x1, y1, x2, y2 = map(int, box)
        label = f"{CLASS_NAMES.get(int(cls_id), '?')} {conf:.0%}"

        # Box
        cv_color = (color.b, color.g, color.r)  # OpenCV usa BGR
        import cv2
        cv2.rectangle(annotated, (x1, y1), (x2, y2), cv_color, 2)

        # Label background
        (text_w, text_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.55, 1)
        cv2.rectangle(annotated, (x1, y1 - text_h - 8), (x1 + text_w + 4, y1), cv_color, -1)
        cv2.putText(annotated, label, (x1 + 2, y1 - 4),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (255, 255, 255), 1)

    annotated_image = Image.fromarray(annotated)

    # ── Resumen de detecciones ────────────────────────────────────
    lines = ["Detecciones encontradas:\n"]
    danger_found = False

    for cls_id, conf in zip(detections.class_id, detections.confidence):
        cls_id = int(cls_id)
        name = CLASS_NAMES.get(cls_id, f"clase_{cls_id}")
        is_danger = cls_id in DANGER_CLASSES
        icon = "🔴" if is_danger else "🟢" if cls_id in {0, 4} else "🔵"
        lines.append(f"  {icon}  {name:<12}  confianza: {conf:.1%}")
        if is_danger:
            danger_found = True

    if danger_found:
        lines.append("\n⚠️  ADVERTENCIA: Se detectaron incumplimientos de EPP.")
        lines.append("   Este resultado es solo orientativo. Requiere supervisión humana.")
    else:
        lines.append("\n✅ No se detectaron incumplimientos de EPP.")

    summary = "\n".join(lines)
    return annotated_image, summary


# ── Interfaz Gradio ───────────────────────────────────────────────
# Define la UI: imagen de entrada, imagen anotada y texto de resultados
with gr.Blocks(title="MAIC-1125 — Detector de Seguridad Industrial") as demo:

    gr.Markdown("""
    # 🦺 Detector de Seguridad Industrial
    **MAIC-1125** — Detección de EPP: cascos, chalecos y personas

    > ⚠️ **Advertencia:** Este modelo es una herramienta de screening preliminar.
    > Produce falsos negativos. No debe usarse como único verificador en decisiones de seguridad vital.
    """)

    with gr.Row():
        with gr.Column():
            input_image = gr.Image(
                type="pil",
                label="Imagen de entrada",
                sources=["upload", "webcam", "clipboard"],
            )
            detect_btn = gr.Button("🔍 Detectar", variant="primary")

        with gr.Column():
            output_image = gr.Image(
                type="pil",
                label="Resultado anotado",
            )
            output_text = gr.Textbox(
                label="Resumen de detecciones",
                lines=10,
            )

    detect_btn.click(
        fn=detect,
        inputs=[input_image],
        outputs=[output_image, output_text],
    )

    gr.Markdown("""
    ---
    **Clases detectadas:** `helmet` · `no helmet` · `no vest` · `person` · `vest`

    🟢 Verde = cumplimiento EPP &nbsp;&nbsp; 🔴 Rojo = incumplimiento EPP &nbsp;&nbsp; 🔵 Azul = persona
    """)


# ── Arranque ──────────────────────────────────────────────────────
if __name__ == "__main__":
    print("\033[92m✅ Iniciando app en http://localhost:7860\033[0m")
    demo.launch(server_name="0.0.0.0", server_port=7860)

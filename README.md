> ⚠️ **ADVERTENCIA IMPORTANTE:** Este modelo es una herramienta asistiva solo para screening preliminar.
> Produce falsos negativos. **NO debe usarse como único verificador en decisiones de seguridad vital.**
> Su uso debe complementarse siempre con supervisión humana y protocolos de seguridad establecidos.

---

# MAIC-1125 — Detección de EPP en Sitios Industriales

Modelo YOLOv8 ajustado para detectar el uso (y ausencia) de Equipos de Protección Personal (EPP)
en entornos de construcción e industria — cascos, chalecos y personas.

---

## 🏗️ Problema AECO y Criterios de Éxito

**Problema:** En sitios de construcción, la ausencia de EPP (casco, chaleco) es una de las
principales causas de accidentes graves. La verificación manual es costosa, inconsistente y
no escala. Se necesita una herramienta de screening automático para apoyar la supervisión.

**Criterios de éxito (PoC universitario):**
- Detectar correctamente cascos y chalecos con mAP50 > 0.60 en validación
- Identificar ausencia de EPP como señal de alerta (aunque con menor precisión en esta versión)
- Servir como base reproducible para iteraciones futuras con más datos

---

## 🏷️ Clases Detectadas y Reglas de Etiquetado

| ID | Clase | Descripción | Regla de etiquetado |
|----|-------|-------------|---------------------|
| 0 | `helmet` | Casco de seguridad puesto | Casco visible y en posición correcta sobre la cabeza |
| 1 | `no helmet` | Sin casco | Persona visible sin casco; cabeza claramente expuesta |
| 2 | `no vest` | Sin chaleco | Persona sin chaleco de alta visibilidad |
| 3 | `person` | Persona (genérica) | Cuerpo humano detectado, sin evaluar EPP |
| 4 | `vest` | Chaleco puesto | Chaleco reflectante visible sobre el torso |

**Notas de etiquetado:**
- Se etiquetan solo objetos con visibilidad ≥ 50% (sin oclusión severa)
- No se aplica blur de rostros (contexto académico; distancias de captura minimizan PII identificable)
- Fuentes: imágenes de Unsplash + imágenes generadas con IA — licencia CC BY 4.0

---

## 📦 Dataset

| Campo | Valor |
|-------|-------|
| Fuente | Roboflow Universe |
| URL | https://universe.roboflow.com/juans-workspace-wp60g/maic-1125_m4t3/dataset/2 |
| Versión | 2 |
| Licencia | CC BY 4.0 |
| Train | 76 imágenes |
| Validación | 15 imágenes |
| Split | ~80 / 20 (sin set de test separado en esta versión) |
| Clases | 5 |

---

## 🚀 Cómo Usar el Detector

Hay dos formas de usar el modelo: **localmente** (recomendado para pruebas rápidas)
o en **Google Colab** (para re-entrenamiento o sin Python instalado).

---

### Opción 1 — App Local (Gradio) ⭐ Recomendado

Interfaz web que corre en tu máquina. No necesitas Colab ni cuenta de Google.

**Requisitos:** Python 3.9+ y `pip`

```bash
# 1. Clonar el repositorio
git clone https://github.com/<tu-usuario>/MAIC-1125_Site-Detection_v2.git
cd MAIC-1125_Site-Detection_v2

# 2. Arrancar la app (instala dependencias automáticamente)
# Windows:
run.bat

# Mac / Linux:
bash run.sh

# 3. Abrir en el navegador
# http://localhost:7860
```

La app permite subir una imagen (o usar la webcam) y devuelve:
- Imagen anotada con bounding boxes coloreados
- Resumen con clase y % de confianza por detección

🟢 Verde = EPP presente · 🔴 Rojo = EPP ausente · 🔵 Azul = persona

---

### Opción 2 — Google Colab

Para re-entrenar el modelo o probarlo sin instalar nada localmente.

#### Pasos de reproducción

```python
# Paso 1 — Instalar dependencias
%pip install -q "ultralytics>=8.4.0" supervision roboflow

# Paso 2 — Descargar dataset desde Roboflow
from roboflow import Roboflow
rf = Roboflow(api_key="TU_API_KEY")
project = rf.workspace("juans-workspace-wp60g").project("maic-1125_m4t3")
dataset = project.version(2).download("yolov8")

# Paso 3 — Entrenar
!yolo task=detect mode=train \
    model=yolo26m.pt \
    data={dataset.location}/data.yaml \
    epochs=20 \
    imgsz=640 \
    plots=True

# Paso 4 — Validar
!yolo task=detect mode=val \
    model=runs/detect/train/weights/best.pt \
    data={dataset.location}/data.yaml

# Paso 5 — Inferencia sobre una imagen
from ultralytics import YOLO
model = YOLO("runs/detect/train/weights/best.pt")
results = model.predict("tu_imagen.jpg", verbose=False)[0]
print(results.boxes.xyxy)   # coordenadas
print(results.boxes.conf)   # confianza
print(results.boxes.cls)    # clase
```

El notebook completo está en [`notebooks/Reproducibility_test.ipynb`](notebooks/Reproducibility_test.ipynb).

---

## 📊 Resultados de Validación

Evaluación sobre el set de validación (15 imágenes, 204 instancias).

### Métricas Globales

| Métrica | Valor |
|---------|-------|
| Precision (P) | **0.594** |
| Recall (R) | **0.541** |
| mAP50 | **0.596** |
| mAP50-95 | **0.452** |

### Métricas por Clase

| Clase | Instancias | P | R | mAP50 | mAP50-95 |
|-------|-----------|---|---|-------|----------|
| helmet | 63 | 0.889 | 0.794 | 0.889 | 0.609 |
| no helmet | 8 | 0.000 | 0.000 | 0.046 | 0.022 |
| no vest | 11 | 0.600 | 0.636 | 0.634 | 0.502 |
| person | 78 | 0.839 | 0.705 | 0.787 | 0.652 |
| vest | 44 | 0.639 | 0.568 | 0.626 | 0.476 |

### Conclusiones Clave

1. **Detección de `helmet` es robusta** (mAP50 = 0.889): la clase más representada en el dataset
   funciona bien y puede usarse como señal de cumplimiento confiable.

2. **`no helmet` falla críticamente** (mAP50 = 0.046): solo 8 instancias de entrenamiento son
   insuficientes. Esta clase requiere un esfuerzo de recolección de datos específico antes de
   poder usarse en producción. **No confiar en la ausencia de alertas como garantía de cumplimiento.**

3. **El modelo generaliza razonablemente para un PoC con ~90 imágenes**, pero el dataset pequeño
   limita la robustez ante variaciones de iluminación, ángulo y distancia. Escalar a 500+ imágenes
   por clase es el próximo paso crítico.

---

## ✅ Checklist de Reproducibilidad

| Parámetro | Valor |
|-----------|-------|
| Dataset | [maic-1125_m4t3 v2](https://universe.roboflow.com/juans-workspace-wp60g/maic-1125_m4t3/dataset/2) |
| Licencia dataset | CC BY 4.0 |
| Variante del modelo | `yolo26m` (YOLOv8 Medium) |
| Epochs | 20 |
| Batch size | default (ultralytics auto) |
| imgsz | 640 |
| ultralytics | `8.4.19` (verificado) |
| PyTorch | `2.10.0+cpu` |
| Python | `3.12.12` |
| Pesos entrenados | `model_weights/best.pt` (incluidos en el repo) |

**Fragmento de instalación reproducible:**
```bash
pip install "ultralytics>=8.4.0" supervision gradio opencv-python Pillow numpy
```

---

## 🔁 Nota de Reproducibilidad

Última ejecución verificada del pipeline de entrenamiento:

| Campo | Valor |
|-------|-------|
| Fecha | 2026-03-04 |
| Hora | 12:20 – 12:32 (~12 min) |
| Entorno | Google Colab — CPU (Intel Xeon @ 2.20GHz, sin GPU) |
| Modelo de verificación | YOLO26n (nano), 5 epochs |
| Resultado | Pipeline completo ejecutado sin errores |
| Plots generados | `confusion_matrix.png` ✅ · `results.png` ✅ · `PR_curve.png` ✗ (normal con pocos epochs) |

> **Importante:** Esta ejecución usa YOLO26n/5 epochs solo para verificar el flujo.
> Los pesos de producción (`model_weights/best.pt`) corresponden a YOLO26m con 20 epochs (mAP50 = 0.596).
> Si no tienes GPU disponible en Colab, el entrenamiento de verificación tarda ~12 min en CPU.

---

## 📁 Estructura del Proyecto

```
MAIC-1125_Site-Detection_v2/
├── notebooks/
│   ├── Reproducibility_test.ipynb         # Notebook de verificación del pipeline (Colab)
│   └── Training_pipeline_roboflow.ipynb   # Notebook original exportado de Roboflow (referencia)
├── src/
│   └── app.py              # App Gradio para inferencia local
├── configs/
│   └── data.yaml           # Configuración del dataset (clases, rutas)
├── docs/
│   ├── README.md           # Este archivo
│   ├── error_analysis.md   # Análisis de fallos (FP, FN, mejoras)
│   └── governance_checklist.md            # Checklist de ética y gobernanza
├── results/
│   ├── curves/             # Curvas de entrenamiento (confusion_matrix, PR, results)
│   └── evidence/           # Capturas de anotaciones y predicciones
├── model_weights/
│   ├── best.pt             # Pesos del mejor modelo entrenado
│   └── last.pt             # Pesos del último checkpoint
├── requirements.txt        # Dependencias para uso local
├── run.bat                 # Arranque rápido en Windows
└── run.sh                  # Arranque rápido en Mac/Linux
```

---

## ⚠️ Limitaciones

- La clase `no helmet` tiene rendimiento muy bajo — no usar para decisiones de seguridad críticas
- Dataset pequeño (~91 imágenes total) — propenso a falsos negativos en condiciones no vistas
- No probado en video en tiempo real
- Diseñado como PoC universitario — **no apto para producción sin iteración adicional**

---

## 📝 Changelog

Ver [CHANGELOG.md](CHANGELOG.md) *(pendiente de crear)*

# Evidencias del Modelo

## Contenido esperado

### `annotation_examples/`
3–5 capturas de imágenes del dataset con sus anotaciones originales (bounding boxes de Roboflow).

### `val_predictions/`
10 capturas de predicciones del modelo sobre el set de validación.
Generadas con `best.pt` (YOLO26m, 20 epochs).

### `new_predictions/`
5 capturas de predicciones sobre imágenes nuevas (no vistas durante entrenamiento).

---

> **Cómo agregar capturas:** Corre inferencia en Colab o con la app Gradio local (`run.bat`),
> toma capturas de pantalla y agrégalas a la carpeta correspondiente.

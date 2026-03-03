# YOLO26 para Detección de Seguridad Industrial (MAIC-1125)

Este proyecto implementa un modelo YOLO26 (YOLOv8) ajustado para la detección de objetos relacionados con la seguridad en entornos industriales, centrándose en cascos, chalecos, personas y la ausencia de estos elementos.

## Estructura del Proyecto
- `model_weights/`: Contiene los pesos del modelo entrenado (`best.pt`, `last.pt`).
- `configs/`: Contiene el archivo de configuración del dataset (`data.yaml`).
- `docs/`: Almacena la documentación del proyecto, incluyendo este `README.md`.

## Cómo Usar el Modelo

Para utilizar el modelo entrenado para inferencia, siga los siguientes pasos:

1.  **Cargar el modelo:**
    ```python
    from ultralytics import YOLO
    import os

    HOME = '/content' # Asegúrate de que HOME apunte al directorio base
    model_path = os.path.join(HOME, 'model_weights', 'best.pt')
    model = YOLO(model_path)
    ```

2.  **Preparar la imagen para inferencia:**
    Asegúrese de tener una imagen en la que desee realizar la detección. Puede usar `PIL` para cargarla.
    ```python
    from PIL import Image
    # Reemplace con la ruta de su imagen
    image_path = '/content/dog-2.jpeg' # Ejemplo de imagen
    image = Image.open(image_path)
    ```

3.  **Realizar la inferencia:**
    ```python
    results = model.predict(image, verbose=False)[0]
    # Los resultados contienen los cuadros delimitadores, clases y confianzas
    print(results.boxes.xyxy) # Coordenadas de los cuadros
    print(results.boxes.conf) # Confianza de la detección
    print(results.boxes.cls)  # Clases detectadas
    ```

4.  **Visualizar los resultados (opcional, requiere `supervision`):**
    ```python
    import supervision as sv

    detections = sv.Detections.from_ultralytics(results)

    # Función de anotación (puede adaptar la función `annotate` de este notebook)
    # def annotate(image: Image.Image, detections: sv.Detections) -> Image.Image:
    #    ...

    # annotated_image = annotate(image, detections)
    # annotated_image.show()
    ```

## Ejemplo de Inferencia con CLI
También puede ejecutar la inferencia directamente desde la línea de comandos (CLI) si tiene `ultralytics` instalado.

```bash
# Asegúrate de que `HOME` esté correctamente configurado en tu entorno de CLI
!yolo task=detect mode=predict model=/content/model_weights/best.pt source="/path/to/your/image.jpg" save=True
```

## Limitaciones del Modelo

Es importante destacar que, durante la fase de validación, el modelo mostró un rendimiento particularmente bajo para la detección de la clase **'no helmet' (sin casco)**. Los resultados de validación indicaron un **mAP50 de 0.0457** para esta clase, lo que sugiere que el modelo tiene dificultades significativas para identificar correctamente a las personas que no llevan casco.

Esto puede deberse a la escasez de ejemplos de entrenamiento para esta clase, la variabilidad en las condiciones de iluminación, o la similitud visual con otras clases o fondos.

## Posibles Mejoras Futuras

Para mejorar el rendimiento del modelo, especialmente en la detección de 'no helmet', se sugieren las siguientes acciones:

*   **Recopilación de más datos:** Aumentar significativamente el número de imágenes de entrenamiento que contengan personas sin casco, abarcando diversas condiciones y poses.
*   **Aumento de datos (Data Augmentation):** Aplicar técnicas de aumento de datos más agresivas específicas para las clases con bajo rendimiento.
*   **Revisión del etiquetado:** Asegurarse de que las etiquetas de 'no helmet' sean precisas y consistentes.
*   **Balanceo de clases:** Implementar estrategias para mitigar el desbalance de clases en el dataset, si existe.
*   **Ajuste de hiperparámetros:** Experimentar con diferentes configuraciones de entrenamiento (e.g., learning rate, épocas, tamaño de batch) para optimizar el rendimiento general y de clases específicas.
*   **Exploración de arquitecturas:** Considerar la posibilidad de probar otras arquitecturas de modelos o variantes de YOLO que puedan ser más robustas para estas detecciones difíciles.

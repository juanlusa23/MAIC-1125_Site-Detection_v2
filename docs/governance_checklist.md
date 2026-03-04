# Checklist de Gobernanza AECO - MAIC-1125_Site-Detection

## 1. Procedencia de los Datos
* **Fuente:** Combinación de imágenes de alta resolución provenientes de la plataforma **Unsplash** (licencia libre) e imágenes generadas mediante **Inteligencia Artificial** para aumentar la variabilidad del dataset.
* **Fecha de recolección:** Random / Diversas (se buscaron diferentes condiciones lumínicas y climáticas para robustecer el modelo).
* **Propietario:** El autor del repositorio es el dueño de la curación y generación del dataset final.

## 2. Tratamiento de PII (Privacidad)
* **Caras / Matrículas:** Existen rostros presentes en las imágenes debido a la naturaleza de la detección de elementos de seguridad (EPP).
* **Estrategia de protección:** Las caras no son plenamente identificables debido a la resolución y distancia de las tomas. Al ser un **proyecto universitario de investigación**, no se ha aplicado desenfoque (blur) para no interferir en la precisión de la detección de cascos, pero se restringe su uso a fines académicos.

## 3. Declaración de Riesgo
* **Falso Negativo de Alto Impacto:** Si el modelo omite la ausencia de un casco, un trabajador podría ingresar a una zona de riesgo sin protección, derivando en un **accidente laboral grave o fatal**.
* **Falso Positivo de Alto Impacto:** Si el modelo detecta un casco inexistente, se generaría una falsa sensación de seguridad, permitiendo operaciones en condiciones no aptas.

## 4. Humano en el Bucle (Human in the Loop)
* **Proceso de revisión:** Al ser un **estudio universitario**, el sistema funciona como una Prueba de Concepto (PoC). En un entorno real, las detecciones deberían ser validadas por un Monitor de Seguridad o Prevencionista de Riesgos antes de emitir una sanción o bloqueo de acceso.

## 5. Licencia
* **Tipo:** **MIT License**. El código y los pesos del modelo son abiertos para fines educativos y de mejora por la comunidad académica.
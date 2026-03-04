# Checklist de Gobernanza — MAIC-1125 Site Detection

---

## 1. Procedencia de los Datos

- **Fuente:** Imágenes de Unsplash (licencia libre) + imágenes generadas con IA para aumentar variabilidad
- **Fecha de recolección:** Diversas (distintas condiciones lumínicas y climáticas)
- **Propietario del dataset curado:** Autor del repositorio
- **Dataset publicado en:** [Roboflow Universe — maic-1125_m4t3 v2](https://universe.roboflow.com/juans-workspace-wp60g/maic-1125_m4t3/dataset/2)
- **Licencia del dataset:** CC BY 4.0

---

## 2. Privacidad y Consentimiento

- [x] Se verificó que las imágenes de Unsplash permiten uso libre sin atribución obligatoria
- [x] Las imágenes generadas por IA no contienen personas reales identificables
- [ ] Blur de rostros aplicado — **NO aplicado** (justificación: resolución/distancia minimizan identificabilidad; uso restringido a fines académicos)
- [x] Dataset no contiene datos sensibles adicionales (nombres, documentos, ubicaciones precisas)

**Minimización de datos:** Solo se recopilaron imágenes necesarias para la tarea de detección de EPP. No se almacena información personal de los trabajadores fotografiados.

---

## 3. Declaración de Limitaciones — Cuándo NO usar este modelo

- ❌ **No usar** como único sistema de verificación en decisiones de acceso o seguridad laboral
- ❌ **No usar** en condiciones de baja iluminación o cámaras de baja resolución (< 480p)
- ❌ **No usar** para la clase `no helmet` en decisiones críticas — mAP50 = 0.046 (falla severamente)
- ❌ **No usar** en producción sin supervisión humana activa
- ❌ **No usar** fuera de entornos industriales similares al dataset de entrenamiento
- ✅ **Uso apropiado:** Screening preliminar asistivo, alertas tempranas sujetas a revisión humana, investigación académica

---

## 4. Nota de Riesgos — Falsos Negativos vs Falsos Positivos

| Tipo de error | Escenario | Consecuencia potencial | Severidad |
|---|---|---|---|
| **Falso Negativo** | Trabajador sin casco no detectado | Ingresa a zona de riesgo sin protección → accidente grave o fatal | 🔴 Crítica |
| **Falso Negativo** | Trabajador sin chaleco no detectado | No se activa alerta → exposición a riesgo de visibilidad | 🟠 Alta |
| **Falso Positivo** | Casco detectado donde no hay | Falsa sensación de cumplimiento → operación en condiciones no aptas | 🟠 Alta |
| **Falso Positivo** | Persona detectada en fondo | Alertas innecesarias → fatiga del operador, reducción de atención | 🟡 Media |

> **Conclusión de riesgo:** Los falsos negativos de `no helmet` son el riesgo más crítico del sistema actual. El modelo **no debe usarse como barrera de seguridad** hasta que esta clase alcance mAP50 > 0.70.

---

## 5. Humano en el Bucle

- **Rol requerido:** Monitor de Seguridad o Prevencionista de Riesgos debe validar toda alerta antes de emitir sanción o bloqueo de acceso
- **Contexto actual:** PoC universitario — no apto para producción autónoma
- **Proceso recomendado en producción:** Detección automática → revisión humana → acción

---

## 6. Licencias

### Código y Pesos del Modelo
**MIT License** — libre para uso educativo, investigación y mejora comunitaria.

```
MIT License
Copyright (c) 2026 MAIC-1125 Project Authors
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files, to use, copy, modify,
merge, publish, distribute, sublicense, and/or sell copies of the Software,
subject to the condition that the above copyright notice is included in all copies.
```

### Dataset
- **Licencia:** CC BY 4.0 (Creative Commons Attribution 4.0)
- **Fuente:** Imágenes de Unsplash (dominio público / licencia Unsplash) + imágenes generadas con IA
- **Atribución requerida:** Citar el dataset de Roboflow Universe al usar en publicaciones académicas
- **Restricción:** No usar las imágenes con rostros para identificación de personas

---

## 7. Checklist Final

- [x] Fuente y licencia del dataset documentadas
- [x] Riesgos de falsos negativos declarados
- [x] Limitaciones de uso claramente especificadas
- [x] Supervisión humana requerida documentada
- [x] Licencia MIT declarada para código y pesos
- [x] Derechos del dataset (CC BY 4.0) especificados
- [ ] Blur de rostros — pendiente para versión de producción
- [ ] Auditoría de sesgo por clase completada — pendiente (ver `error_analysis.md`)

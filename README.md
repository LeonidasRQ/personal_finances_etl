# Cashflow Excel Automation

Este es un script en Python que automatiza la adición de registros a una hoja de Excel tipo cashflow.  
Permite agregar múltiples filas en una sola ejecución, respetando:

- El formato (estilos, fuentes, bordes) de la última fila.
- La fórmula del balance acumulado.
- Las validaciones de datos (listas desplegables).
- Reglas automáticas según tipo de flujo (Ingreso/Egreso).

---

## 🚀 Requisitos

- Python 3.10+ (instalado vía [Scoop](https://scoop.sh) o manual).
- Virtual environment (venv).

---

## ⚙️ Instalación

1. Clona o copia este repositorio.

2. Crea y activa un entorno virtual:

   ```bash
   python -m venv venv
   ```

   En Windows PowerShell:

   ```powershell
   .\venv\Scripts\activate
   ```

3. Instala las dependencias:

   ```bash
   pip install -r requirements.txt
   ```

---

## 📝 Configuración

- Asegúrate de tener tu archivo de Excel `copia_finanzas.xlsx` en el mismo directorio (o ajusta el path en `append_to_cashflow.py`).
- Configura las entradas que quieras insertar editando el arreglo `entries` en el script.

---

## 🚀 Ejecución

Con el entorno virtual activo, ejecuta:

```bash
python append_to_cashflow.py
```

---

## ✅ Estado del proyecto

✅ Inserta múltiples registros en una sola ejecución.

✅ Mantiene el estilo, validaciones y cálculos.

🚀 Planeado: leer datos desde CSV o preguntar datos interactivos.

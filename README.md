# UsageTrackerAssistant

**UsageTrackerAssistant** es un bot diseñado para monitorear y registrar la actividad en la PC, así como para interactuar con ChatGPT para responder preguntas del usuario. Combina capacidades de seguimiento del sistema con la asistencia de un modelo de lenguaje avanzado.

## Funcionalidades

- **Monitoreo del Sistema**:
  - Registra información sobre los procesos en ejecución.
  - Guarda un historial de teclas presionadas.
  - Registra los movimientos y clics del ratón.

- **Almacenamiento de Datos**:
  - Archivos diarios en formato de texto (`process_history.txt`, `key_history.txt`, `mouse_history.txt`) almacenados en subcarpetas por fecha.

- **Descarga de Historial**:
  - Permite al usuario visualizar el historial almacenado para una fecha específica.

- **Interacción con ChatGPT**:
  - Permite al usuario hacer preguntas a ChatGPT y recibir respuestas.

## Requisitos

- Python 3.x
- Bibliotecas:
  - `psutil`
  - `pynput`
  - `openai`

## Instalación

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/tu_usuario/usage-tracker-assistant.git

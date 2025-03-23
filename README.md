# Sólo 5 (Just5)

ENG | ESP

## TL;DR

Solo5 es una aplicación que quiere ayudar a organizar y priorizar lo más importante de cada día teniendo en cuenta las fechas de entrega y dificultad para evitar sobrecargas de trabajo, enfocarse en solo cinco tareas significativas al día.

1. ¿por que?
2. Características principales
3. instalación
4. uso, primeros pasos
5. futuro

## ¿Por qué otra maldita lista de tareas?

Como parte de mi aprendizaje en Python, quería reforzar mi comprensión de algoritmos mientras le daba un giro a algo que ya se ha hecho hasta el cansancio.

## Características principales

- **Escribe de forma natural**: Escribe como te nazca, la aplicación interpretará la información para priorizarlo.
- **Procesamiento 100% local**: No utiliza servicios externos ni inteligencia artificial. Todo se ejecuta en tu máquina.
- **Multilenguaje**: Soporta cualquier idioma con solo agregar un archivo JSON de configuración, inicialmente en español e inglés. (Si realizas una traducción, compártela <3 )
- **Altamente configurable**: Personaliza los comandos, estructura de datos y la forma en que la aplicación interpreta lo que escribes.
- **Gestión flexible de tareas**: Agrega, edita, marca como completadas y organiza tareas de manera sencilla.
- **Planificación y reprogramación**: Revisa tareas futuras, reorganiza prioridades y extiende la planificación diaria.

## Instalación

### Requisitos

- Python 3.7 o superior.

- Terminal compatible con secuencias de escape ANSI (la mayoría de las terminales modernas lo son).

### Pasos para instalar

1. Clona el repositorio:

```bash
git clone https://github.com/tu-usuario/solo5.git
cd solo5
```

2. Ejecuta la aplicación:

```bash
./solo5
```

3. ejecuta el configurador:

```
> config
```

Por defecto, Solo5 viene en inglés y con el paquete para español. Si deseas cambiar por un idioma diferente, ve a al directorio ./data/config/lang/ y cambia los archivos correspondientes dentro del directorio regex y ui. Luego, inicia config y especifica el nuevo idioma (el nombre del archivo sin la extensión)

## Uso

La interfase ha sido pensada y desarrollada para ser lo mas sencilla e intuitiva de manejar.

### Línea de comandos

la linea de comandos está estructurada para mostrar la siguiente información:

```
contexto > comando actual > accion a realizar > tareas que serán afectadas
```

#### contexto

Es en qué lista estamos trabajando y las tareas que tenemos disponibles para manipular.

- Global, todas las tareas activas a la fecha
- Hoy, es un subset de Global con las tareas del día
- Terminadas, es una lista diferente con todas las tareas realizadas rusante los ultimos 30 días

EL contexto puede afectar el comportamiento de algunas acciones, por ejemplo, al agregar cuando se está en Hoy, ademas de crear la tarea, la agrega a Hoy, aunque supere las 5 acciones, o, acciones como Done o Update no se pueden ejecutar en Terminadas.

#### Comando actual

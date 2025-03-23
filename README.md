# Sólo 5 (Just5)

[ENG](#tldr-english) | [ESP](#tldr-español)

## TL;DR (english)

Just5 is an application designed to help you organize and prioritize the most important tasks of each day, considering deadlines and difficulty, to avoid workload overload and focus on just five meaningful tasks per day.

Based on this principle, commands were designed to align with natural speech and writing. A text interpretation structure was also created to recognize common ways of stating dates, whether absolute or relative, and store them as parameters. Additionally, it considers difficulty and the immovability of a deadline to determine the urgency level and position it in the queue before it becomes a problem.

## Contents

1. [Why another task list?](#why-another-task-list)
2. [Key Features](#key-features)
3. [Installation](#installation)
4. [Use](#use)
5. [Future](#future)

## Why another task list?

I wanted to reinforce my understanding of some algorithms while learning Python. Why not think about how to improve something that has already been done countless times?

## Key Features

- **Write naturally**: Write as it comes naturally to you, and the application will interpret the information to prioritize it.
- **100% local processing**: No external services or artificial intelligence. Everything runs on your machine.
- **Multilanguage support**: Supports any language by simply adding a JSON configuration file, initially available in Spanish and English. (If you translate it, please share! <3)
- **Highly configurable**: Customize commands, application behavior, and how it interprets what you write.
- **Flexible task management**: Add, edit, mark as completed, and organize tasks easily.

## Installation

### Requirements

- Python 3.7 or higher.
- A terminal compatible with ANSI escape sequences (most modern terminals are).

### Installation Steps

1. Clone the repository:

```bash
curl -L -o solo5.zip https://github.com/dothedada/solo5/archive/refs/heads/main.zip
unzip solo5.zip && mv solo5-main solo5
cd solo5
```

2. Run the application:

```
./solo5
```

3. Run the configurator and answer each question:

```
> config
```

By default, Just5 comes in English with a Spanish language pack. If you want to switch to a different language, go to ./data/config/lang/ and modify the files inside the regex and ui directories. Then, restart the configuration and specify the new language (use the filename without the extension).

## Use

The interface was designed to be as simple and intuitive as possible.
Command Line Interface

The command line is structured to display the following information:

```
context > current command > action to perform > Number of affected tasks >
```

#### Context

This refers to the list currently being worked on and the available tasks for manipulation.

- **Global**: All active tasks to date.
- **Today**: A subset of Global with the day's tasks.
- **Completed**: A separate list of all tasks completed in the last 30 days.

Context affects some actions. For example, adding a task in "Today" not only creates the task but also adds it to "Today," even if it exceeds five tasks. Actions like `done` or `update` cannot be performed in "Completed."

You can switch contexts by typing the name of the desired context: Global, Today, Completed.

#### Current Command

The command line always displays the command that will be executed on the selected tasks. The command and its abbreviation are shown.

##### List of Commands

\[v\]iew -> View the task list in the current context  
\[a\]dd -> Add one or more tasks  
\[upd\]ate -> Update a selected task (only one at a time)  
\[d\]one -> Mark a task as completed (cannot be undone)  
\[del\]ete -> Delete a task (cannot be undone)  
\[make\] -> Generate a list of up to 5 tasks for today
\[extra\] -> Once the day's tasks are completed, add more if needed  
\[tmrw\] -> Show pending tasks scheduled for the next day  
\[s\]earch -> Find a task based on characters in its description  
\[c\]lear -> Clear the list of tasks affected by an action  
\[s\]ave -> Save the current state of all contexts  
\[e\]xit -> Exit the current action, or if no action is in progress, close the application  
\[purge\] -> Remove all completed tasks from Global and Today, and delete tasks completed over 30 days ago  
\[fix\] -> Recalculate due dates in case of errors  
\[config\]ure -> Start the configuration process  
\[h\]elp -> Open the help document  

#### Action to Perform

Displays the action required from the user to proceed. The flow is always: Search -> Select -> Confirm.

- **Search**: Based on the entered characters, searches for tasks within the current context.
- **Select**: Displays search results where tasks can be selected using their numbers. Multiple selections can be made using commas or ranges (e.g., `1, 3, 7-9` selects tasks 1, 3, 7, 8, and 9).
- **Confirm**: Confirms the action. Options: Yes (execute action), No (repeat action), Cancel (return to action selection). Confirmation can be skipped globally by enabling YOLO/CarpeDiem mode in settings.

#### Affected Tasks

Displays the number of currently selected tasks that will be affected by the action.

### Writing a Task

Just5 aims to be as seamless as possible, interpreting natural date formats, whether absolute (calendar-based) or relative. A task’s priority can be increased using `*` or explicitly stating it is "undelayable."

It also recognizes difficulty on a scale of 1 to 5, either in natural language (e.g., "somewhat difficult") or parameterized (e.g., `!4`). While project management isn't fully implemented yet, tasks can be assigned to a project using `@project_name`. This will eventually allow project-specific contexts.

**Example:**

```
Global > [a]dd > Write the app manual before next Friday, it's easy but undelayable
```

Interpreted as:
(assuming today is Saturday, March 22, 2025)

```json
{
    "lang": "en",
    "task": "Write the app manual before next Friday, it's easy but undelayable",
    "done": false,
    "creation_date": "22-03-2025",
    "due_date": "28-03-2025",
    "done_date": "",
    "difficulty": 2,
    "undelayable": true
}
```

Multiple tasks can be added in a single action using `//`:

```
Global > [a]dd > Task one // Task two // Task three
```

This creates three independent tasks.

## Future

- [ ] Create a context for each project.  
- [ ] Determine the number and difficulty of daily tasks based on the user’s specified energy level (Linear programming).  
- [ ] Develop a wrapper to allow Just5 to run as a one-liner in the command line.  
- [ ] Create a special output format for integration with other programs that provide a graphical interface.  

## TL;DR (español)

Solo5 es una aplicación diseñada para ayudarte a organizar y priorizar las tareas más importantes de cada día, teniendo en cuenta las fechas de entrega y la dificultad, con el objetivo de evitar la sobrecarga de trabajo y enfocarte en solo cinco tareas significativas al día.

Partiendo de este principio, se diseñaron los comandos para que coincidieran con el habla y la escritura natural de las personas. También se creó una estructura de interpretación de textos que toma formas frecuentes de enunciar fechas, ya sea de forma absoluta o relativa, y las almacena como parámetros. Además, considera la dificultad y la inamovilidad de una fecha para determinar el nivel de urgencia y posicionarla en la cola antes de que se convierta en un problema.

## Contenidos

1. [¿Por qué otra lista de tareas?](#por-qué-otra-lista-de-tareas)
2. [Características](#características)
3. [Instalación](#instalación)
4. [Uso](#uso)
5. [Futuro](#futuro)

## ¿Por qué otra lista de tareas?

Quería reforzar mi comprensión de algunos algoritmos mientras aprendía python, ¿por qué no permitise pensar cómo podría hacerse mejor algo que ya se ha hecho hasta el cansancio?.

## Características principales

- **Escribe de forma natural**: Escribe como te nazca, la aplicación interpretará la información para priorizarla.
- **Procesamiento 100% local**: No utiliza servicios externos ni inteligencia artificial. Todo se ejecuta en tu máquina.
- **Multilenguaje**: Soporta cualquier idioma con solo agregar un archivo JSON de configuración, inicialmente en español e inglés. (Si realizas una traducción, ¡compártela! <3)
- **Altamente configurable**: Personaliza los comandos, cómo funciona la aplicación y la forma en que interpreta lo que escribes.
- **Gestión flexible de tareas**: Agrega, edita, marca como completadas y organiza tareas de manera sencilla.

## Instalación

### Requisitos

- Python 3.7 o superior.

- Terminal compatible con secuencias de escape ANSI (la mayoría de las terminales modernas lo son).

### Pasos para instalar

1. Clona el repositorio:

```bash
curl -L -o solo5.zip https://github.com/dothedada/solo5/archive/refs/heads/main.zip
unzip solo5.zip && mv solo5-main solo5
cd solo5
```

2. Ejecuta la aplicación:

```bash
./solo5
```

3. ejecuta el configurador y responde cada pregunta:

```
Global> config
```

Por defecto, Solo5 viene en inglés y con el paquete de lenguaje para español. Si deseas cambiar por un idioma diferente, ve a al directorio ./data/config/lang/ y cambia los archivos correspondientes dentro del directorio regex y ui. Luego, inicia config y especifica el nuevo idioma (el nombre del archivo sin la extensión)

## Uso

La interfase ha sido pensada y desarrollada para ser lo mas sencilla e intuitiva de manejar.

### Línea de comandos

la linea de comandos está estructurada para mostrar la siguiente información:

```
Contexto> Comando Actual> Accion a Realizar> Tareas que Serían Afectadas>
```

#### contexto

Es la lista en la que estamos trabajando y las tareas que tenemos disponibles para manipular.

- Global: Todas las tareas activas a la fecha.
- Hoy: Un subconjunto de Global con las tareas del día.
- Terminadas: Una lista diferente con todas las tareas realizadas en los últimos 30 días.

El contexto puede afectar el comportamiento de algunas acciones. Por ejemplo, al agregar una tarea cuando se está en "Hoy", además de crear la tarea, la agrega a "Hoy", aunque supere las cinco tareas. Acciones como done o update no se pueden ejecutar en "Terminadas".

Es posible cambiar de contexto escribiendo el nombre del contexto al que queremos ir: Global, Hoy, Terminadas.

#### Comando actual

En la línea de comandos siempre se verá el comando que se va a ejecutar sobre las tareas que serán afectadas. En la línea de comandos se muestra el comando y su abreviatura.

##### lista de comandos

\[v\]er -> Ver la lista de tareas en el contexto
\[a\]gregar -> Agregar una o mas tareas, para agregar varias
\[act\]ualizar -> Actualiza la tarea seleccionada, sólo se puede actualizar una tarea a la vez
\[r\]ealizada -> Marca la tarea como realizada o terminada, no se puede deshacer esta acción.
\[borrar\] -> Borra la tarea, no se puede deshacer esta acción.
\[hacer\] -> Genera una lista de hasta 5 tareas para hoy
\[extra\] -> Una vez realizadas las tareas del día, puedes adicionar más tareas al día.
\[m\]añana -> Muestra las tareas pendientes que serían programadas para el próximo día.
\[b\]uscar -> Busca una tarea a partir de los caracteres que tenga la tarea, para luego ejecutar en ella alguno de los comandos posibles
\[l\]impiar -> borra lista de tareas que srían afectadas por una acción
\[g\]uardar -> Guarda el estado actual de todos los Contextos
\[s\]alir -> Sale de la accion actual, y en caso de no estar en ninguna accion, cierra la aplicación.
\[purgar\] -> Borra todas las tareas realizadas de Global y Hoy, además borra las taréas que fueron realizadas hace más de 30 días.
\[arreglar\] -> Vuelve a calcular las fechas de vencimiento en caso de vencimiento.
\[config\]urar -> Inicia la secuencia de configuración.
\[ayuda\] -> Abre el documento de ayuda.

#### Acción a realizar

Muestra la acción que se requiere del usuario para pasar al siguiente paso del flujo. El flujo siempre es: Buscar -> Seleccionar -> Confirmar.

- **Buscar**: A partir de la secuencia de caracteres ingresada por el usuario, busca todas las tareas en el contexto que la contengan.
- **Seleccionar**: Se muestra el resultado de la búsqueda, donde se deben ingresar las tareas que se van a editar empleando el número que las acompaña. Para seleccionar varias, sepáralas por comas o establece rangos con un guión. Ej: 1, 3, 7-9 selecciona las tareas 1, 3, 7, 8 y 9.
- **Confirmar**: Realiza una confirmación de la tarea a realizar. Sí: Realiza la acción sobre las tareas seleccionadas. No: Repite el ciclo de la acción. Cancelar: Devuelve a la selección de la acción a realizar. La confirmación puede omitirse globalmente al activar el modo YOLO/CarpeDiem en la configuración.

#### Tareas que serían afectadas

Muestra la cantidad de tareas que se encuentran actualmente seleccionadas y que serían afectadas por la acción a realizar.

### Escribir una tarea

El propósito de Solo5 es ser lo más invisible posible, por lo que interpreta la forma natural en que se escriben las fechas, ya sea de forma absoluta (calendario) o relativa a partir de la ubicación actual en el tiempo. Es posible aumentar el peso de la fecha de una tarea agregando un * o diciendo explícitamente que es "inaplazable".

También interpreta la dificultad en una escala del 1 al 5, ya sea en lenguaje natural (por ejemplo: "algo difícil") o parametrizado (por ejemplo: !4). Aunque todavía no se ha implementado el manejo de proyectos, se puede asignar una tarea a un proyecto en particular al agregar @mi_proyecto. Esto, en un futuro, servirá para crear contextos propios de cada proyecto.

**ejemplo:**

```
Global > [a]ñadir > Realizar el manual de la aplicacion antes del próximo viernes, es fácil pero inamovible
```

esto será interpretado de la siguiente forma:
(supongamos que hoy es sábado 22 de marzo de 2025)

```json
{
    "lang": "es",
    "task": "Realizar el manual de la aplicacion antes del próximo viernes, es fácil pero inamovible",
    "done": false,
    "creation_date": "22-03-2025",
    "due_date": "28-03-2025",
    "done_date": "",
    "dificulty": 2,
    "undelayable": true
}
```

Se pueden agregar varias tareas en una sola acción al usar "//"

```
Global> [a]ñadir> tarea uno // tarea dos // tarea tres
```

esto crea tres tareas independientes

## Futuro

- [ ] Crear un contexto para cada proyecto.
- [ ] determinar la cantidad y dificultad de tareas para el día en función del nivel de energía especificado por la persona. (Linear programming)
- [ ] Crear el wrapper para poder usar Solo5 como onliner en la línea de comandos
- [ ] crear un output especial para vincular con otros programas que puedan proveer una interfase gráfica

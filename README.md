# Sólo 5 (Just5)

This is a todo list in terminal that helps you to prioritize your tasks and prevent burnout.

## Why another f*cking To-Do list?

As part of my Python learning journey, I wanted to strengthen my understanding of algorithms—especially linear programming—while adding a unique twist to something that has been done to exhaustion.

## Flow

### add

1. prompt in terminal
2. parse regular text to build a token
3.

## to-do of the to-do

- [-] Infrastructure design
- [-] Task Token class
        - Basic task properties
- [-] Task class
  - Inherit from token and adds priority
  - update task, print
- [-] Input parser
  - Regex parade
  - ~NLP for parsing the input and create the token for the tasks object
- [-] the regex factory
- [-] THE F*CKING date parser
- [-] Task heap
  - priorization euristics
- [-] ToDo manager class
  - invoke task methods (Update, mark done, mark not done)
  - delete task
  - arrange tasks
  - search tasks
  - import - export task batches
- [] in manager, set taks for today ->
      - get 5 by priority
      - based on energy,
      - put asside the able ones to delay
      - add the next in line with the appropiate dificulty
- [-] CSV manager
  - Create, read, write task in CSV
- [] Interfase printer
  - set day
  - check (day, next day, all)
  - search task for: done,update, remove
  - add task
  - mark done
  - edit task
  - remove task
- [] Make documentation

## Parsing date structure

(- from -)  
from        -> establece inicio de cálculo. de, este, de este, el
day         -> numero del día de calendario
today_rel   -> hoy, mañana, pasado mañana
weekday     -> nombre del día de la semana("lunes", "martes", ...)
month_num   -> numero del mes en el calendario
month_name  -> nombre del mes en el calendario
year        -> año (opcional, asume actual/siguiente)
date        -> fecha absoluta sin calulos adicionales
(- modifier -)
modifier    -> de, de este, dentro de, próximo, siguiente
amount      -> cantidad numérica para incremento, si no int o none es 1
unit_day    -> dias
unit_week   -> semana
unit_month  -> mes
unit_year   -> año

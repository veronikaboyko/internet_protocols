# Сканер TCP и UDP портов

Эта программа выполняет сканирование указанного диапазона портов на заданном хосте и определяет, какие порты открыты.

## Входные данные

> python tcp_udp_scanner.py *\<host\> \<start_port\>\<end_port\>*

Здесь
* *\<host\>* - целевой хост, на котором будет выполняться сканирование портов (ip адрес или доменное имя)
* *\<start_port\>* и *\<end_port\>* определяют диапазон портов, которые будут сканироваться (*\<start_port\>* <= *\<end_port\>*)

## Пример использования

### Успешный запуск

<img width="568" alt="Снимок экрана 2023-05-27 в 03 38 16" src="https://github.com/veronikaboyko/tracer/assets/91218615/8873e586-fe3b-4234-bbdb-4e8b5cddd7a6">

<img width="565" alt="Снимок экрана 2023-05-27 в 04 00 31" src="https://github.com/veronikaboyko/tracer/assets/91218615/6e9db369-db2d-43ff-b388-acbed809717c">

<img width="567" alt="Снимок экрана 2023-05-27 в 04 10 11" src="https://github.com/veronikaboyko/tracer/assets/91218615/30f58e5e-c14d-4a2d-b96e-e9c5a53cf753">

### Обработка некорректных входных данных

<img width="567" alt="Снимок экрана 2023-05-27 в 04 18 53" src="https://github.com/veronikaboyko/tracer/assets/91218615/3ed74b38-590e-4862-805d-362bd92edc89">

<img width="567" alt="Снимок экрана 2023-05-27 в 04 19 21" src="https://github.com/veronikaboyko/tracer/assets/91218615/55e53918-62ec-4bef-8a61-580320c4208c">

<img width="569" alt="Снимок экрана 2023-05-27 в 04 06 57" src="https://github.com/veronikaboyko/tracer/assets/91218615/7a41c98b-ea71-4afb-a938-3c61e1eeb3b4">

### help

<img width="566" alt="Снимок экрана 2023-05-27 в 04 08 53" src="https://github.com/veronikaboyko/tracer/assets/91218615/91ec29c7-7aca-418e-9b91-2d5b4a720c86">

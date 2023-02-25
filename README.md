# Web-приложение для предсказания теплопроводности и упругих модулей кристаллических материалов

На основе данных о свойствах элементов, входящих в состав соединения, таких как: 

- положение элемента в Периодической системе Менделеева,
- его масса, 
- ковалентный радиус, 
- электроотрицательность и т. д. 

формируется дескриптор, уникальный для каждого соединения. 

Предварительно данный дескриптор был рассчитан для ~5000 соединений, данные по свойствам которых заимствовались из открытой базы данных [AFLOWlib](https://aflow.org/search/). На этой основе были обучены регрессионные модели в рамках метода градиентного бустинга.
Web-приложение рассчитывает дескриптор для задаваемого состава, что позволяет предсказать его свойства с помощью обученных моделей. 


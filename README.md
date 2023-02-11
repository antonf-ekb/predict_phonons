<h2> API для предсказания теплопроводности и упругих модулей кристаллических материалов</h2>
<p>На основе данных о свойствах элементов, входящих в состав соединения, таких как как: положение элемента в Периодической системе Менделеева, его масса, ковалентный радиус, электроотрицательность и т. д. формируется дескриптор, уникальный для каждого соединения. 
Предварительно данный дескриптор был рассчитан для ~5000 соединений, данные по свойствам которых заимствовались из открытой базы данных AFLOWlib [https://aflow.org/search/]. На этой основе были обучены регрессионные модели в рамках метода градиентного бустинга.
API рассчитывает дескриптор для задаваемого вами состава, что позволяет предсказать его свойства с помощью обученных моделей. 
</p>
<h3> Использование API</h3>
Запрос осуществляется через отправку POST-запроса методу /predict.
Пример осуществления запроса для соединения Mn2CoCrP2 с помощью requests:

<code>
import json
from urllib.request import urlopen
params = {
    "cmpd": "Mn2CoCrP2"
}
query_url = "http://localhost:8000/predict/" #insert the name of your server instead of localhost:8000
response = requests.post(query_url, json=params)
entry=response.json()

</code>

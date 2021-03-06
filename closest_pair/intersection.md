## Тест на пересечение треугольника и отрезка.

Пусть триугольик и отрезок задаются точками `(a, b, c)` и `(A, B)` соответственно.

Пусть:
```
s1 = orient3d(A, a, b, B)
s2 = orient3d(A, a, c, B)
s3 = orient3d(A, b, c, B)
```

Если не все `si == 0`, тогда треугольник и отрезок не компланарны.
Если при этом `si` разных знаков - пересечения нет, если же `si` 
одинаковых знаков (либо некоторые обнуляются) - пересечение есть 
(пока только с пряой, содержащей отрезок).

Далее, в зависимости от количесва нулевых значений среди `si` получаем:
 - 0 - пересечение не на границе треугольника
 - 1 - пересечение по ребру
 - 2 - пересечение по верщине

Далее, чтобы узнать пересекается ли сам отрезок с треугольников, 
нужно выяснить находятся ли его концы по разные стороны плоскости треугольника.
Посмотрим н знаки `orient3d(A, a, b, c)` и `orient3d(B, a, b, c)` если они разные
(или хотя бы один из них == 0) то пересечение с отрезком есть, иначе - нет.


В случае, если все `si == 0`, пусть d - точка, не лежащая на плоскости
треугольника. Построим тетраэдр (a, b, c, d) и запустим тест на перечение
с остальными его гранями. Они заведомо не компланарны отрезку, поэтому
такой рекурсивный вызов допустим.

Если все результаты вызова отрицательны - пересечения с (a ,b, c) нет.
В противном случае задача сводится к 2 тестам:
 - пересечение `(A, B)` с одним из сегментов `(a, b), (b, c), (c, a)` - 
 разобрано на семинаре.
 - отрезок полностью лежит внутри треугольника. Чтобы это проверить, 
 запустим ещё раз тест для треугольника `(a, b, c)` и отрезков `(A, d)`
 и `(B, d)`. Если в обоих случаях есть пересечение не на границе - 
 отрезок полностью лежит внутри треугольника.
 
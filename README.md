# Направление Кибербезопасности
Данный репозиторий предназначен для сдачи работ по учебной практики.
## Как отправлять отчеты

1. Склонируйте этот репозиторий к себе на компьютер и перейдите в него:
```html
$ git clone <your-repository-url>
$ cd <your-repository-name>
```
2. Сделайте ветку из мастера с соответствующим именем:
```html
$ git checkout master      	# перейти на master ветку
$ git pull                 	# вытащить все последние изменения
$ cd <your-directory>       # перейти в нужную директорию (при необходимости)
```
3. Разместите коды своей работы в папке в корне репозитория. Например, структура папок может выглядеть так:
 * MySweetlyReport
    * <ваше решение>
4. Сохраните изменения и отправьте их на сервер:
```html
$ git add <solution-files>
$ git commit -m <your-message>
$ git push
```
Например, если в качестве решения вы добавил в папку MySweetlyReport файлы src/main.cpp, src/lib.h, src/lib.cpp и Makefile, то для их добавления нужно выполнить:
```html
$ cd MySweetlyReport
$ git add src/main.cpp src/lib.h src/lib.cpp Makefile
```
Если вы посылаете ветку в первый раз, необходимо явно указать, что отправление идёт в ваш репозиторий:
```html
$ git push -u origin <your-assignment-branch>
```
5. Сделайте Pull Request из созданной вами ветки в ветку master с названием "Отчет, <фамилия> <имя>", (например, "Отчет, Иванов Иван"). О том, как сделать реквест, написано [здесь](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/creating-a-pull-request).
6. При наличии замечаний повторите шаги 4 и 5, новый request делать не надо.

<strong>Не делайте мердж пулл-реквестов в мастер! <strong>

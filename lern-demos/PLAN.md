# План: интерактивные демки по материалам 64 модулей

Охват: 64 курса.
Полная инвентаризация тем по каждому модулю: `INVENTORY.md`.

## Зачем

Слайды объясняют алгоритм через инвариант и формулу. Человек понимает алгоритм, когда видит, как меняется состояние. Разрыв между этими двумя вещами и есть причина, по которой 6 ГБ PDF лежат мёртвым грузом.

Демка закрывает разрыв, если выполняет три условия:

1. Есть состояние, которое меняется по шагам, и это состояние видно целиком.
2. Пользователь может подставить свой ввод и сломать алгоритм.
3. Можно отмотать назад и посмотреть тот же шаг ещё раз.

Если что-то из этого не выполняется, получается картинка, а не демка. Картинку уже нарисовали в слайдах.

## Технические конвенции

- **Один HTML-файл на демку.** Vanilla JS, SVG или Canvas, никаких зависимостей и сборки. Файл открывается двойным кликом, работает офлайн, отправляется в мессенджере.
- **Интерфейс на английском.** Термины из курса даём в скобках по-немецки: `Topological Sort (Topologische Sortierung)`. Кто угодно сможет открыть.
- **Обязательный минимум UI:** кнопки `Step` / `Back` / `Play` / `Reset`, ползунок скорости, поле ввода своих данных, счётчик шага вида `Step 7 / 23`, строка-объяснение текущего шага обычным языком.
- **Разметка страницы:** слева ввод и управление, в центре визуализация, справа или снизу состояние структур данных (стек, таблица, очередь). Панель «что сейчас произошло» одной строкой под визуализацией.
- **Никакого localStorage.** Всё состояние в памяти, чтобы файл вёл себя одинаково везде.
- **Файлы:** `demos/<module-slug>/<demo-name>.html`. Рядом `README.md` в две строки: что показывает и на каком листке из курса это было.
- **Оценка трудозатрат** ниже: S = вечер (2-4 ч), M = день (6-10 ч), L = несколько дней (20+ ч).

## Приоритеты

**Tier S (делать первыми).** Тема тяжёлая, объяснить словами почти нельзя, а анимация решает вопрос за минуту. Плюс материал в папках полный.

| # | Демка | Модуль | Трудозатраты |
|---|---|---|---|
| 1 | Mini-Compiler Explorer: source → tokens → parse tree → AST → stack code → VM | uebersetzerbau-ss25/ss26 | L (прототип готов) |
| 2 | NFA → DFA converter: subset construction по шагам + минимизация | gti-ss22, gti-ss24 | M |
| 3 | Tomasulo / Scoreboarding simulator по такту | rechnerarchitektur-ss23 | L |
| 4 | Graph algorithms playground: BFS, Dijkstra, Bellman-Ford, Kruskal, Prim на одном редактируемом графе | dap2-ss21 | M |
| 5 | Dynamic programming table explorer: Rucksack, LCS, Partition | dap2-ss21 | M |
| 6 | Petri net simulator: маркировка, срабатывание переходов, дедлок | mnp-ss23/ss24, eingebettete-systeme | M |
| 7 | Real-time scheduling: RM, EDF, Gantt + пропущенные дедлайны | eingebettete-systeme-ws22-23 | M |
| 8 | SQL engine в браузере на Präsidenten-DB + план запроса | informationssysteme-ss22/ss23 | L |

**Tier A.** Хорошая тема, материал есть, но либо проще, либо уже существуют похожие открытые визуализаторы.

Cache simulator (RA), CPU pipeline с hazards (RA/RS), RISC-V assembler + пошаговое выполнение (rechnerstrukturen), Resolution prover и таблицы истинности (logik), Kripke-модели и бисимуляция (logik), CFG parse tree + Pumping-Lemma игра (gti), Turing machine с лентой (gti), k-Means / DBSCAN / spectral clustering (gdw, eidv), PageRank итерациями (gdw), Decision tree builder с энтропией (gdw), SVM с ядрами и margin (gdw), Voronoi через sweep line Fortune (eidv), Sugiyama layered graph drawing (eidv), Reingold-Tilford tree layout (eidv), Distance-vector routing с count-to-infinity (rvs), Subnetting calculator (rvs), Mealy-автомат протокола (rvs), Simplex геометрически (mao), Discrete-event simulation queue (mao), ER → реляционная схема → нормальные формы (informationssysteme, bis), ETL пайплайн и звёздная схема (data-warehousing), MapReduce word count по фазам (data-warehousing, gdw), Lambda-редукция и ленивые вычисления (funktionale-programmierung), Process scheduler и семафоры (betriebssysteme), BPMN симулятор токенов (bpm), Fitts' Law и эксперимент по HCI (mmi).

**Tier B.** Материал тонкий (2-20 файлов, часто только листки без слайдов) или тема плохо ложится на анимацию. Идеи есть, но начинать не с них: softwarekonstruktion (диаграммы рефакторинга, design patterns), sfl, webtechnologien-2, big-data-analytics, thesis-projects-ml, fachprojekt-*, proseminar-enterprise-computing, wahrscheinlichkeitsrechnung, mathematik-fuer-informatik-1, dap1.

**Tier C (не делать).** Организационные и не-визуальные курсы: stipendien, praesentationstechnik, boss-pruefung-*, dap1-klausur-2021, datenmanagement-ss22, informationsmanagement-ws23-24, aktuelle-themen-graphische-dv-ss25, blockchain-digitale-waehrungen (2 файла), bilanzierung, marketing-modul2, elektronische-geschaeftsprozesse.

Для Tier C есть смысл сделать одно другое: сводный HTML-указатель по всем 64 папкам, чтобы находить нужный PDF за секунды. Это S и полезнее любой демки по этим курсам.

---

# Каталог по темам

Формат: тема из курса → что за демка → что видно на экране → чему учит → сложность.

## 1. Компиляторы и языки

### uebersetzerbau-ss25, uebersetzerbau-ss26
В папках 11 глав слайдов (`01 Einführung` … `11 Optimierung und Programmanalyse`) плюс 6 листков с решениями и 17 записей лекций в ppsx.

**1.1 Mini-Compiler Explorer** (L, Tier S, прототип собран)
Пользователь пишет 10 строк на игрушечном языке. Пять панелей показывают одну и ту же программу на пяти уровнях: поток токенов с подсветкой позиции в исходнике, дерево разбора, AST, таблица символов с типами, код стековой машины. Дальше VM выполняет код по инструкциям, стек и переменные видны.
Учит главному факту курса: компилятор это конвейер преобразований представления, и каждая фаза выбрасывает часть информации. Ошибка типа ловится не там, где написана, а на конкретной фазе, и это видно.

**1.2 LL(1) vs LR(0) table builder** (M)
Ввод: грамматика в текстовом виде. Считает FIRST/FOLLOW, строит таблицу разбора, показывает конфликты и почему грамматика не LL(1). Рядом LR(0)-автомат состояний.
Это ровно то, что в курсе просят считать руками в `04 Top-Down-Parsing` и `05 Bottom-Up-Parsing`.

**1.3 Peephole и constant folding** (S)
Берём код из 1.1, показываем оптимизации главы 11 как правила переписывания: до, правило, после. Пользователь включает и выключает отдельные оптимизации.

### funktionale-programmierung-ss26
14 лекций (заголовки в PDF не извлеклись), Haskell, литература Doberkat и «Modellieren und Implementieren in Haskell», Übungen 9-12, Midterm 2026.

**1.4 Lambda / Haskell reduction stepper** (M)
Выражение редуцируется по шагам, редекс подсвечен, справа переключатель ленивой и энергичной стратегии на одном и том же выражении. Классический пример: бесконечный список и `take 5`.
Показывает, почему в Haskell работает то, что в Java повесило бы программу.

## 2. Теория вычислений и логика

### gti-ss22, gti-ss24 (gti-ss23 только листки)
Полные скрипты по главам: RE, DFA/NFA, REG, Minimierung, PumpAlgs, CFG, Normalformen, PDA, Pumping для CFL, Syntaxanalyse, Modelle, Church-Turing, Unentscheidbarkeit, PCP, PTime, NP, NPC. Плюс 12 листков с решениями и 26 туториалов.

**2.1 NFA → DFA converter** (M, Tier S)
Пользователь рисует NFA мышкой (клик = состояние, drag = переход). Subset construction идёт по шагам: видно, какое множество состояний становится новым состоянием DFA и почему. Дальше минимизация через таблицу различимых пар. В конце: тестовое слово прогоняется по обоим автоматам параллельно.
Это самое ценное в курсе. Subset construction на бумаге понимается со третьего раза, на экране с первого.

**2.2 Pumping-Lemma game** (M)
Игра на два хода: программа выбирает язык, пользователь заявляет длину накачки, программа даёт слово, пользователь ищет разбиение, программа накачивает и показывает, что слово вышло из языка. Роли можно менять.
Пампинг-лемма это игра с кванторами, и в формате игры она перестаёт быть загадкой.

**2.3 Turing machine с лентой** (S)
Таблица переходов слева, лента с головкой в центре, история конфигураций снизу. Готовые примеры из курса плюс редактор.

**2.4 NP-reduction visualizer** (M)
3-SAT → Clique → Vertex Cover. Слева формула, справа граф, который из неё построен. Пользователь тыкает в присваивание переменных и видит, как в графе появляется клика.
Курс просит доказывать редукции; здесь редукция становится конструкцией, которую можно потрогать.

### logik-ws21-22
14 глав: Aussagenlogik (синтаксис, семантика, нормальные формы, SAT, теорема о полноте), Modallogik (Kripke, бисимуляции), Prädikatenlogik (структуры, резолюция, Prolog). 6 листков с решениями, 15 туториалов.

**2.5 SAT solver stepper (DPLL)** (M)
Формула в CNF, дерево поиска строится по шагам: unit propagation, pure literal, split, backtrack. Видно, какая ветка отсекается и почему.

**2.6 Resolution prover** (M)
Ввод: множество клауз. Программа строит дерево резолюции до пустой клаузы. Для предикатной логики добавляется унификация с подстановками. Это главы 11-12.

**2.7 Kripke model explorer** (M)
Граф миров, формула модальной логики, подсветка миров, где она истинна. Второй граф рядом, кнопка «проверить бисимуляцию» и построение бисимуляционного отношения по шагам. Главы 5-7.

## 3. Алгоритмы и структуры данных

### dap2-ss21 (самый содержательный модуль по алгоритмам)
Divide & Conquer, MergeSort, бинарный поиск, QuickSort с Partition, нижняя граница сортировки, умножение целых, Mastertheorem, умножение матриц, convex hull, greedy и Interval Scheduling, Scheduling с дедлайнами, DP (Fibonacci, Partition, Rucksack, LCS), структуры данных (массив, DLL, словарь, бинарные деревья, AVL, B-Bäume), графы (BFS, SSSP, Dijkstra, Bellman-Ford, Kruskal, Prim). 6 домашних листков, 9 ergaenzung, туториалы по индукции и DP, три экзамена.
Листки за ss22-ss25 (blatt/ex/pblatt, часть с решениями) дают дополнительные задачи к тем же темам.

**3.1 Graph algorithms playground** (M, Tier S)
Один редактируемый граф, переключатель алгоритма: BFS, Dijkstra, Bellman-Ford, Kruskal, Prim. Приоритетная очередь или список рёбер показаны рядом как реальная структура. Есть кнопка «поставить отрицательный вес», после которой Dijkstra выдаёт неправильный ответ, а Bellman-Ford правильный.
Тот момент, когда Dijkstra ломается, объясняет разницу между алгоритмами лучше любого доказательства.

**3.2 DP table explorer** (M, Tier S)
Rucksack, LCS и Partition в одной демке. Таблица заполняется по клеткам, при наведении на клетку подсвечиваются те клетки, из которых она посчитана. Обратный проход показывает восстановление решения. Рядом счётчик: сколько вызовов сделала наивная рекурсия и сколько сделала таблица.
Это тема отдельного туториала в курсе (`tutorium-dynamische-programmierung.pdf`).

**3.3 Sorting race + lower bound** (S)
MergeSort, QuickSort, HeapSort на одном массиве одновременно, счётчик сравнений и обменов у каждого. Отдельная вкладка: дерево решений для n = 3 и подсчёт листьев, откуда берётся граница n log n.

**3.4 BST / AVL / B-Tree insert-delete** (M)
Вставка и удаление с показом вращений в AVL и расщепления узлов в B-дереве. Слева высота и число узлов, чтобы видеть, зачем балансировка.

**3.5 Convex hull (Graham scan)** (S)
Точки ставятся мышкой, сканирование идёт по шагам, поворот в каждой тройке показан знаком детерминанта.

**3.6 Master theorem calculator** (S)
Ввод: a, b, f(n). Показывает, какой случай теоремы применим, и рисует дерево рекурсии с суммой работы по уровням.

### dap1-ws20-21
Слайды без извлекаемых заголовков, но по Zusatzaufgaben видно темы: DLL (doppelt verkettete Listen) и BST. 12 Übungsblätter, 5 Praktikumsblätter, Java.

**3.7 Linked list surgery** (S)
Двусвязный список, операции вставки и удаления пошагово со всеми указателями. Кнопка «сделать это в неправильном порядке» показывает потерянный узел и висячий указатель. Ровно ошибки из практикума.

## 4. Архитектура и системное

### rechnerarchitektur-ss23 (49 файлов, самый полный из трёх)
Pipelines, Advanced Pipelining, Branch Prediction, ILP и Instruction Scheduling, Scoreboarding, Tomasulo и спекулятивное выполнение, закон Амдала, Multithreading, Caches, Memory, Multicore, GPU, сети, энергия и температура, DNN-обзор, Spectre и Meltdown. 12 немецких листков и 13 английских, шаблоны для ручного трассирования `tomasulo_vorlage_neu.pdf` и `scoreboarding.pdf`, Probeklausur.

**4.1 Tomasulo / Scoreboarding simulator** (L, Tier S)
Ровно та таблица, которую в курсе заполняют ручкой: такты по горизонтали, инструкции по вертикали, столбцы Issue / Read Operands / Execute complete / Write result. Плюс живое состояние: reservation stations, register status, Common Data Bus. Переключатель между scoreboarding и Tomasulo на одной программе, чтобы видеть разницу.
Это первый кандидат после компилятора: заменяет самое нудное задание курса и показывает, зачем вообще нужен Tomasulo.

**4.2 Pipeline hazard visualizer** (M)
5-стадийный пайплайн, программа из 6-8 инструкций, видно data hazard, forwarding, stall и flush после неверно предсказанной ветки. Переключатели: forwarding on/off, branch prediction always-taken / 1-bit / 2-bit.

**4.3 Cache simulator** (M)
Поток адресов (свой или сгенерированный), настройки: размер, ассоциативность, размер линии, политика замещения. Видно попадания и промахи, тип промаха (cold / conflict / capacity), итоговый hit rate. График hit rate от ассоциативности строится сам.

**4.4 Amdahl / Gustafson calculator** (S)
Ползунок доли параллельного кода и числа ядер, кривая ускорения. Показывает, почему 100 ядер не дают 100x.

**4.5 Spectre explainer** (M)
Упрощённая модель: спекулятивная загрузка, обученный предиктор, кэш как канал утечки. Пошагово видно, как читается байт, который «никогда не читался». Прямо по слайду `spectre.pdf` («code that never ran»).

### rechnerstrukturen-ws20-21, rechnerstrukturen-ws21-22
Два больших скрипта (первая часть и ISA), справочник RISC-V, 13 листков, Probeklausur.

**4.6 RISC-V assembler + step VM** (M)
Ассемблер в машинный код, потом пошаговое выполнение: регистры, память, PC. Рядом сама 32-битная кодировка инструкции по полям (opcode, rd, funct3, rs1, rs2). Справочник `riscv_referenz.pdf` даёт готовый набор команд.

**4.7 Number representation lab** (S)
Two's complement, IEEE 754 по битам: пользователь щёлкает биты, значение пересчитывается. Показывает, откуда берётся `0.1 + 0.2 != 0.3`.

### betriebssysteme-ss22
Einführung in C, Prozesse verwalten, Thread-Synchronisation, задания A0-A2 на C.

**4.8 Scheduler comparison** (M)
FCFS, SJF, Round Robin, приоритеты на одном наборе процессов. Gantt-диаграмма, среднее время ожидания и оборота. Ползунок квантa времени для RR.

**4.9 Semaphore playground** (M)
Producer-consumer и dining philosophers. Потоки как дорожки, критическая секция подсвечена. Кнопка «убрать один семафор» приводит к состоянию гонки или дедлоку, и цикл ожидания рисуется на графе.

### eingebettete-systeme-ws22-23
Petri Nets, Discrete Event Models, models of computation, HW-части, RTOS, Resource Access Protocols, WCET, Real-Time Calculus, aperiodic и periodic scheduling, multiprocessor, IoT random access, ILP.

**4.10 Real-time scheduling simulator** (M, Tier S)
Набор периодических задач (период, WCET, дедлайн). Rate Monotonic и EDF на одной Gantt-диаграмме, пропущенные дедлайны красным. Рядом считается utilization и граница Liu-Layland, видно, почему RM ломается при загрузке выше границы, а EDF нет.

**4.11 Priority inversion и protocols** (M)
Три задачи и один мьютекс: сначала классическая инверсия приоритетов, потом Priority Inheritance и Priority Ceiling на тех же данных. Это глава Resource Access Protocols.

**4.12 Petri net simulator** (M, Tier S, общая с MNP)
Места, переходы, маркировка. Клик по переходу срабатывает, если разрешён. Автоматический поиск дедлока и построение дерева достижимости.

## 5. Параллельность и модели процессов

### modellierung-nebenlaeufiger-prozesse-ss23, ss24
15 лекций, литература Agha/Thati «An Algebraic Theory of Actors», 13 листков, два проекта, экзамен. Заголовки слайдов в PDF не извлеклись, поэтому идеи ниже опираются на литературу и название курса.

**5.1 Actor model playground** (M)
Акторы как узлы с почтовыми ящиками, сообщения летят по рёбрам. Порядок доставки перемешивается, и видно, как одна и та же программа даёт разный результат. Кнопка «сделать доставку упорядоченной».

**5.2 CCS / process algebra stepper** (M)
Два процесса, таблица возможных переходов, интерливинг как дерево. Проверка эквивалентности через бисимуляцию (пересекается с 2.7).

## 6. Сети

### rechnernetze-verteilte-systeme-ws22-23 (61 файл, полный курс)
Слои 1-6 по частям, mobile Netze, Datensicherheit, экскурс про Mealy-автоматы для описания протоколов. Heimaufgaben: Mealy-автомат, distance-vector, subnetting, анализ веб-страницы. 14 Tafelübungen с решениями.

**6.1 Distance-vector routing** (M)
Граф маршрутизаторов, таблицы у каждого, обмен векторами по шагам. Кнопка «оборвать линк» запускает count-to-infinity, и видно, как split horizon это лечит. Это Heimaufgabe 3 и Aufgabe 8.3.

**6.2 Subnetting trainer** (S)
Задача генерируется, пользователь считает, программа проверяет и показывает битовую раскладку адреса и маски. Прямая замена ручной части Heimaufgabe 3.

**6.3 Protocol as Mealy machine** (S)
TCP-хендшейк или простой стоп-и-жди как Mealy-автомат: состояние, вход, выход. Прямо формат экскурса из курса.

**6.4 TCP congestion control** (M)
Slow start, congestion avoidance, fast retransmit. График окна во времени, кнопка «потерять пакет».

**6.5 Layer trace** (M)
Один HTTP-запрос обрастает заголовками при спуске по стеку и раздевается при подъёме. Пакет как вложенные прямоугольники.

## 7. Базы данных и хранилища

### informationssysteme-ss22, informationssysteme-ss23
Relational model, SQL basics, SQL, Datenbankentwurf/ER, нормализация, transaction management, XML. 14 листков, отдельный SQL-Skript, учебная база Präsidenten-DB (`SchemaPresidentDB_a4.pdf`, таблицы Admin / Pres / Hobby / Vp).

**7.1 SQL playground на Präsidenten-DB** (L, Tier S)
Схема из курса зашита в файл как массивы объектов, движок SQL написан на JS (SELECT, WHERE, JOIN, GROUP BY, HAVING, ORDER BY, подзапросы). Три панели: запрос, результат, дерево плана выполнения с промежуточными таблицами после каждого оператора.
Понимание SQL ломается именно на порядке выполнения (FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY). Если этот порядок видно, вопросов больше нет.

**7.2 ER → relational schema → normal forms** (M)
Пользователь рисует ER-диаграмму, программа генерирует таблицы, потом проверяет 1NF/2NF/3NF/BCNF на введённых функциональных зависимостях и показывает декомпозицию с шагами.

**7.3 Transaction scheduler** (M)
Две-три транзакции, операции перетаскиваются в общее расписание. Программа определяет аномалию (dirty read, lost update, phantom), строит граф конфликтов и проверяет сериализуемость. Дальше 2PL и уровни изоляции.

### data-warehousing-ss23, data-warehousing-ss24
introduction, overview, modelling, planning, implementing, ETL, MapReduce. 6-7 assignments.

**7.4 Star schema и OLAP cube** (M)
Факты и измерения, куб с операциями slice, dice, roll-up, drill-down. Одна и та же цифра пересчитывается при смене гранулярности.

**7.5 ETL pipeline builder** (M)
Грязный CSV на входе, блоки extract / clean / transform / load соединяются, после каждого блока видно, как изменились данные и сколько строк отвалилось.

**7.6 MapReduce word count** (S)
Три фазы (map, shuffle, reduce) на маленьком тексте, каждый воркер отдельной дорожкой. Видно, что shuffle это сортировка по ключу и в чём тут узкое место.

## 8. Data Science и ML

### grundlagen-datenwissenschaft-ws22-23, ws23-24
Introduction to Data Science, Scaling Computations, PageRank, Frequent Itemset Mining и association rules, Clustering, Search, Decision Trees, SVM, Evaluating Classifiers, Artificial Neural Networks, bias/variance, CRISP-DM, Optimierung. 10 листков в ws22-23, файл `big.txt`.

**8.1 Clustering sandbox** (M)
Точки ставятся мышкой или генерируются. k-Means по итерациям (центроиды двигаются), DBSCAN с ползунками eps и minPts, спектральная кластеризация. На одном и том же наборе видно, где k-Means проигрывает (два полумесяца).

**8.2 PageRank iterations** (S)
Граф страниц, вектор ранга пересчитывается по шагам, размер узла меняется. Ползунок damping factor, кнопка «сделать висячий узел» показывает, зачем нужен телепорт.

**8.3 Decision tree builder** (M)
Датасет в таблице, программа считает энтропию и information gain по каждому признаку, пользователь выбирает разбиение сам и сравнивает со жадным выбором. Ползунок глубины показывает переобучение на тестовой выборке.

**8.4 SVM margin explorer** (M)
Точки двух классов, разделяющая полоса, опорные векторы подсвечены. Ползунок C, переключатель ядра (linear, poly, RBF). Видно, как RBF заворачивает границу.

**8.5 Bias-variance workbench** (S)
Полиномиальная регрессия, ползунок степени, две кривые ошибки (train и test) в реальном времени. Слайд `Bias Varianz` из курса.

**8.6 Neural net from scratch** (M)
Маленькая сеть, forward и backward проход по шагам с показом градиентов на каждом весе. Задача XOR, чтобы было видно, зачем скрытый слой.

**8.7 Apriori / FP-growth** (S)
Корзины покупок, генерация кандидатов по уровням, отсечение по support, правила с confidence и lift.

### big-data-analytics-ws23-24
12 exercises с решениями, данные `players_22.csv` и `penguins.csv`, слайды по главам.

**8.8 Sampling and sketches** (M)
Reservoir sampling, HyperLogLog, Bloom filter, Count-Min Sketch на потоке из `players_22.csv`. Видно, как точность растёт с памятью. Тема, которую без демки понять почти нельзя.

### fachprojekt-dokumentenanalyse, fachprojekt-ki-brettspiele (ss25, ws24-25)
Мало материала (1-2 файла), но темы понятны из названий.

**8.9 Minimax / MCTS on Connect Four** (M)
Дерево поиска рисуется по шагам, альфа-бета отсечение подсвечено, счётчик посещённых узлов с отсечением и без. Для MCTS: четыре фазы и рост дерева.

## 9. Визуализация и HCI

### datenvisualisierung-ss24, datenvisualisierung-ss25 (по 31-43 файла)
Einführung, Visualisierungspipelines, Graphische Datenanalyse, Graphen, Räumliche Daten, Zeitabhängige Daten, Versuchsplanung, Data Mining, Medizinische Datenvisualisierung и Vektorfeldvisualisierung. Литература: Fortune 1987 (Voronoi sweep line), Reingold-Tilford 1981, Sugiyama 1981, Crescenzi 1992, von Luxburg (spectral clustering), Battista Graph Drawing. Данные: `epilepsy.csv`, `blutdruck.csv/txt`. 7 листков.

**9.1 Fortune sweep line + Voronoi** (M)
Точки, движущаяся линия развёртки, beach line из параболических арок, события site и circle. Готовится Delaunay-триангуляция как двойственный граф. Прямо по статье Fortune из папки.

**9.2 Sugiyama layered layout** (M)
Граф проходит четыре фазы: удаление циклов, назначение слоёв, минимизация пересечений, назначение координат. После каждой фазы видно результат и число пересечений. Статья Sugiyama 1981 и Martí/Laguna 2001 лежат в папке.

**9.3 Reingold-Tilford tree layout** (S)
Дерево раскладывается по алгоритму из статьи, видно контуры поддеревьев и сдвиги. Рядом наивная раскладка для сравнения.

**9.4 Vector field visualization** (M)
Поле на сетке, переключатель: стрелки, hedgehog, streamlines, LIC. Показывает, почему стрелки врут на плотных полях. Главы I и J.

**9.5 Marching squares / isolines** (S)
Скалярное поле, ползунок порога, 16 случаев марширующих квадратов подсвечиваются на сетке.

**9.6 Time series explorer на epilepsy.csv** (S)
Реальные данные из папки: сырой сигнал, скользящее среднее, FFT-спектр, спектрограмма. Глава F плюс DFT-апплет, который упоминается в материалах.

### mensch-maschine-interaktion-ws23-24, ws24-25, ws25-26 (по 41-43 файла)

**9.7 Fitts' Law experiment** (S)
Демка сама проводит эксперимент: пользователь кликает по целям разного размера и расстояния, программа собирает время, строит регрессию и выводит a и b. Затем предсказывает время для новой цели.
Редкий случай, когда демка не иллюстрирует теорию, а порождает данные, подтверждающие её.

**9.8 Interaction design failures** (S)
Набор намеренно плохих виджетов рядом с исправленными версиями: mode error, отсутствие обратной связи, плохой affordance. Проверка принципов Nielsen и Norman на живых элементах.

## 10. Оптимизация и симуляция

### modellgestuetzte-analyse-optimierung-ss25 (37 файлов)
Konzepte ereignisdiskreter Simulation, генерация случайных чисел, моделирование входных данных, оценка прогонов, Simulationssoftware, границы симуляции, валидация, введение в оптимизацию, линейная оптимизация, целочисленная и комбинаторная, динамическая оптимизация. Практика в AnyLogic и Octave, 9 листков.

**10.1 Discrete-event simulation of a queue** (M)
M/M/1 очередь: календарь событий слева, состояние системы в центре, статистика справа. Ползунки λ и μ, видно взрыв очереди при λ → μ. Главы 2 и 5.

**10.2 Random number quality lab** (S)
LCG с плохими и хорошими параметрами, тесты: гистограмма, спектральный тест (пары точек), автокорреляция. Классическая решётка RANDU видна сразу. Глава 3.

**10.3 Simplex geometrically** (M)
LP с двумя переменными: многоугольник допустимых решений, симплекс идёт по вершинам, целевая функция как двигающаяся прямая. Рядом та же задача в табличной форме симплекс-метода. Главы 10-11.

**10.4 Branch and bound** (M)
Целочисленная задача: дерево ветвлений, LP-релаксация в каждом узле, отсечение по границе. Видно, сколько узлов сэкономила граница.

## 11. Software Engineering и Web

### softwarekonstruktion-ss22, ws23-24, ws24-25, ws25-26 (10-18 файлов каждый)

**11.1 Design pattern playground** (M)
Observer, Strategy, Decorator: UML-схема сверху, живой пример снизу. Кнопка «добавить требование» показывает, сколько кода придётся править с паттерном и без.

**11.2 Refactoring diff viewer** (S)
Плохой код слева, шаги рефакторинга справа, метрики (цикломатическая сложность, длина метода) пересчитываются на каждом шаге.

### webtechnologien-2-ss22 (11 файлов)

**11.3 Render pipeline и reflow** (S)
DOM → CSSOM → layout → paint → composite. Пользователь меняет свойство, программа показывает, какие фазы пересчитываются. Объясняет разницу между `left` и `transform`.

## 12. Математика и статистика

### mathematik-fuer-informatik-1-ws20-21, wahrscheinlichkeitsrechnung-statistik-ws22-23

**12.1 Linear algebra visualizer** (M)
Матрица 2x2 как преобразование плоскости, ползунки на элементах, сетка деформируется. Собственные векторы подсвечены как направления, которые не поворачиваются. Определитель как площадь.

**12.2 Distribution and CLT lab** (S)
Выбор распределения, ползунок размера выборки, гистограмма средних сходится к нормальной. Рядом доверительный интервал и его покрытие при повторных выборках.

**12.3 Hypothesis test sandbox** (S)
Две выборки, t-тест, ползунки размера эффекта и n. Видно, как p-value зависит от n, и что такое ошибки первого и второго рода. Плюс демонстрация p-hacking через множественные тесты.

## 13. Бизнес-информатика

Материал большой (betriebliche-informationssysteme-ws25-26: 43 файла со всеми лекциями; business-process-management-ws23-24; bilanzierung-ss26: 36 файлов), но под пошаговую анимацию ложится хуже. Две идеи, которые всё-таки работают:

**13.1 BPMN token simulator** (M)
Диаграмма процесса, токены двигаются по потоку, gateway'и разветвляют. Ползунки времён обработки, считается время цикла и находится узкое место. Это Quantitative Analysis из bpm-ws23-24.

**13.2 Double-entry bookkeeping trainer** (S)
Хозяйственная операция текстом, пользователь выбирает счёта дебета и кредита, T-счета обновляются, из них собирается баланс. Проверка, что баланс сходится. Bilanzierung, Buchführung I-III.

---

# Roadmap

**Спринт 1 (готово частично).** Mini-Compiler Explorer как эталон: задаёт общий шаблон UI, который потом копируется в остальные демки.

**Спринт 2.** NFA→DFA (2.1) и Graph playground (3.1). Две самые универсальные темы, годятся для показа кому угодно.

**Спринт 3.** Tomasulo (4.1) и SQL playground (7.1). Самые трудоёмкие, но и самая большая отдача: оба заменяют нудные ручные задания.

**Спринт 4.** Petri net (4.12) + Real-time scheduling (4.10) + DP table (3.2).

**Спринт 5.** Визуальный блок: Fortune Voronoi (9.1), Sugiyama (9.2), Clustering sandbox (8.1). Эти три хорошо смотрятся вместе как «алгоритмы, которые рисуют».

Дальше по интересу. После третьего спринта имеет смысл сделать один индексный `index.html` со ссылками на все демки, сгруппированными по курсам.

# Что я не рекомендую делать

- Демки по курсам, где в папке 1-3 файла (blockchain-digitale-waehrungen, datenmanagement-ss22, fachprojekt-*, aktuelle-themen-graphische-dv). Материала не хватает даже на корректную постановку задачи.
- Ещё один визуализатор сортировок как первый проект. Их сотни, и тема слишком лёгкая, чтобы кого-то удивить. В плане она есть (3.3), но только вместе с нижней границей, что и делает её небанальной.
- Собирать всё в React-монорепо до того, как будет 5-6 работающих демок. Один файл на демку сейчас важнее красоты: он открывается у любого человека без объяснений.

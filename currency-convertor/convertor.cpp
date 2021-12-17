#include <iostream>
#include <cstring>
#include <cctype>

using namespace std;

string toUppercase(string str){

    char charArr [str.length()];

    for (int i = 0; i < str.length(); i++) {
        charArr[i] = str.at(i);
    }

    for (int i = 0; i < strlen(charArr); ++i) {
        charArr[i] = toupper(charArr[i]);
    }

    return charArr;


    /*
     * Функция strcpy() используется для копирования содержимого str2 в str1.
     * Аргумент str2 должен быть указателем на строку, оканчивающуюся нулем.
     * Функция strcpy() возвращает указатель на str1. Если строки str1 и str2 перекрываются,
     * то поведение функции strcpy() не определено.
     */
//    strcpy(charArr, str.c_str());
    /*
     * c_str()
     * Формирует массив строк в стиле си. И возвращает указатель на него.
     * Допустим, некоторая функция в качестве параметра принимает указатель на массив чаров:
     * void Foo(const char* content);
     * То есть, в неё можно передать строку только в виде c-ctyle указателя
     * А у тебя есть строка записанная в стринге:
     * std::string str="привет мир";
     * И тебе нужно передать эту строку в твою функцию:
     * Foo(str); //нельзя. функция не умеет работать со стрингами
     * но так как функция не умеет работать со стрингами, а только с указателями,
     * то единственный способ сделать это - функция c_str()
     * Foo(str.c_str() ); //можно.
     * Функция c_str() присутствует только для совместимости с с-style кодом.
     * И в собственном c++ style коде, её лучше избегать настолько, насколько это возможно,
     * дабы не плодить "суржик" (смесь двух стилей в одном исходном коде)
     */

    /*
     * Функция strlen() возвращает длину строки, оканчивающейся нулевым символом,
     * на которую указывает str. При определении длины строки нулевой символ не учитывается.
     */
//    for (int position = 0; position < strlen(charArr); position++) {
        /*
         *Макрос putcnar() записывает символ, находящийся в младшем байте ch, в файл stdout.
         * Функционально он эквивалентен putc(ch, sdout). Поскольку во время обращения к функции
         * аргументы символьного типа приводятся к целому типу, можно использовать символьные
         * переменные как аргументы putchar().
         */
        /*
         * Функция toupper() позволяет преобразовать строчные букв в прописные.
         */
//        putchar();
//        charArr[position] = toupper(charArr[position]);
//        charArr[position] = toupper(charArr[position]);
    //}

    return str;
}

int main(){
    string  currencies [] =
            {
                    "eur", "usd", "pln", "uah", "rub", "gbp"
            };

    for(const string& currency : currencies){
        cout << toUppercase(currency) + " ";
    }
    return 0;
}



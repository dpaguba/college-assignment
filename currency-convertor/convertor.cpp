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
        charArr[i] = (char) toupper(charArr[i]);
    }

    return charArr;
}

void displayCurrency(){
    string  currencies [] =
            {
                    "eur", "usd", "pln", "uah", "rub", "gbp"
            };

    for(const string& currency : currencies){
        cout << toUppercase(currency) + " ";
    }
    cout << "\n";
    cout << "Choose the currency to convert from: ";
}

void calculate(){
    string from, to;
    cin >> from;
    cout << "Choose the currency to convert to: ";
    cin >> to;
}

int main(){
    displayCurrency();
    calculate();
    return 0;
}

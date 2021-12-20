#include <iostream>
#include <cctype>
#include <iomanip>

using namespace std;

// Declaration of all currencies, that are available in convertor
string  currencies [] =
        {
                "eur", "usd", "pln", "uah", "rub", "gbp"
        };

// function greets the user
void greet(){
    cout << "Hi! I'm glad to see you using our currency convertor!" << endl;
}

// function makes all letters capitalized
string toUppercase(string str){
    char charArr [str.length()];

    for (int i = 0; i < str.length(); i++) {
        charArr[i] = (char) toupper(str.at(i));
    }
    return charArr;
}

// function makes all letters lowercase
string toLowercase(string str){
    char charArr [str.length()];

    for (int i = 0; i < str.length(); i++) {
        charArr[i] =  (char) tolower(str.at(i));
    }
    return charArr;
}

// function displays all currencies and asks for currency to sell
void displayCurrency(){
    cout << "\nFollowing currencies are available:" << endl;
    for(const string& currency : currencies){
        cout << toUppercase(currency) + " ";
    }
    cout << "\nChoose the currency to convert from: ";
}

// function checks, if the entered string is in the list of currencies
bool checkFrom(string f ){
    for(const string& currency : currencies){
        if (toLowercase(f) == currency){
            return true;
        }
    }
    return false;
}

// function checks, if the entered string is in the list of currencies
bool checkTo(string t){
    for(const string& currency : currencies){
        if (toLowercase(t) == currency){
            return true;
        }
    }
    return false;
}

// function checks, that the currencies to be exchanged are different
bool checkFromTo (string f, string t){
    return !(t == f);
}

// function does all stuff with exchanging
void calculate(){
    string from, to;
    double rate = 0;
    double number;

    cin >> from;
    cout << "Choose the currency to convert to: ";
    cin >> to;
    cout << "Enter your money: ";
    cin >> number;

    from = toLowercase(from);
    to = toLowercase(to);

    if (checkFrom(from) && checkTo(to) && checkFromTo(from, to)){
        if (from == "eur"){
            if (to == "usd"){
                rate = 1.12;
            }else if (to == "pln"){
                rate = 4.63;
            }else if(to == "uah"){
                rate = 30.85;
            }else if (to == "rub"){
                rate = 83.37;
            }else if (to == "gbp"){
                rate = 0.85;
            }
        }else if (from == "usd"){
            if (to == "eur"){
                rate = 0.89;
            }else if (to == "pln"){
                rate = 4.12;
            }else if(to == "uah"){
                rate = 27.44;
            }else if (to == "rub"){
                rate = 74.17;
            }else if (to == "gbp") {
                rate = 0.75;
            }
        }else if (from == "pln"){
            if (to == "eur"){
                rate = 0.22;
            }else if (to == "usd"){
                rate = 0.24;
            }else if(to == "uah"){
                rate = 6.66;
            }else if (to == "rub"){
                rate = 18.0;
            }else if (to == "gbp"){
                rate = 0.18;
            }
        }else if (from == "uah"){
            if (to == "eur"){
                rate = 0.032;
            }else if (to == "usd"){
                rate = 0.036;
            }else if(to == "pln"){
                rate = 0.15;
            }else if (to == "rub"){
                rate = 2.7;
            }else if (to == "gbp"){
                rate = 0.028;
            }
        }else if (from == "rub"){
            if (to == "eur"){
                rate = 0.012;
            }else if (to == "usd"){
                rate = 0.013;
            }else if(to == "pln"){
                rate = 0.056;
            }else if (to == "uah"){
                rate = 0.37;
            }else if (to == "gbp"){
                rate = 0.01;
            }
        }else if (from == "gbp"){
            if (to == "eur"){
                rate = 1.18;
            }else if (to == "usd"){
                rate = 1.32;
            }else if(to == "pln"){
                rate = 5.46;
            }else if (to == "uah"){
                rate = 36.35;
            }else if (to == "rub"){
                rate = 98.25;
            }
        }
        cout << fixed << setprecision(2) << number * rate << endl;
    }else{
        cout << "Invalid input" << endl;
    }
}

// Convertor
void convert(){
    string answer = "yes";
    while (answer == "yes"){
        displayCurrency();
        calculate();

        cout << "Do you want to change something else? Please answer yes or no!" << endl;
        cin >> answer;
        while (answer == "yes") {
            displayCurrency();
            calculate();
            cout << "Do you want to change something else? Please answer yes or no!" << endl;
            cin >> answer;
            answer = toLowercase(answer);
        }
    }
}

int main(){
    greet();
    convert();
    return 0;
}

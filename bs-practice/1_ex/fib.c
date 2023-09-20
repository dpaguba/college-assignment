#include <stdio.h>

int calc_fib(int num){
    if(num <= 1){
        return num;
    }else{
        return calc_fib(num - 1) + calc_fib(num - 2);
    }
}

int main(){
    int num;
    printf("Enter a number: ");
    scanf("%d", &num);
    if(num > 0){
        int res = calc_fib(num);
        printf("res: %d\n", res);
    }
    else{
        printf("ERROR: Do not enter negative numbers");
    }
    
}
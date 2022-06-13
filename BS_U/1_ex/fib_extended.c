#include <stdio.h>
#include <stdlib.h>

int calc_fib(int num){
    if(num <= 1){
        return num;
    }else{
        return calc_fib(num - 1) + calc_fib(num - 2);
    }
}

// atoi converts char [] to int
// argc is number of passed arguments
// argv[] contains arguments. argv[0] contains programname

int main(int argc, char *argv[]){

    if(argc < 2){
        printf("ERROR: No Parameter defiend\n");
    }else{

        int num = atoi(argv[1]);
        // printf("%d", num);

        if(num > 0){
            int res = calc_fib(num);
            printf("res: %d\n", res);
        }else{
            printf("ERROR: Do not enter negative numbers");
        }
    }
    
}
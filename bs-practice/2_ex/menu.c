#include "stdio.h"
#include "stdlib.h"
#include "string.h"
#include "unistd.h"
#include <sys/wait.h>

const char *menu[4] = {"-l", "-a", "-t", "exit"};

void displayMenu(){
    for(int i = 0; i < 4; i++){
        printf("%d. %s\n", i + 1, menu[i]);
    }
}

const char* getParameter(int position){
    return menu[position - 1];
}

int askForNumber(){
    int position;
    printf("Auswahl: ");
    scanf("%d", &position);
    printf("Es wurde %s gewaehlt.\n", menu[position - 1]);
    return position;
}




int main(){
    int stop = 0;
    while (0 == stop){
        displayMenu();
        int position = askForNumber();

        pid_t pid, pid_c;
        pid = fork();
        if(pid == 0){
            if(position > 4 || position < 1){
                printf("ERROR: You have to enter number in range from 1 to 4!\nTry again!\n");
            }else if(position < 4){
                execlp("ls", "ls", getParameter(position), (char *)NULL);
            }else{
                execlp("exit", "exit", (char *)NULL); 
            }
            exit(0);

        }else{
            // save pid of child process
            pid_c = wait(NULL);

            if(position != 4){
                printf("Child pid: %d\n", pid_c);
            }

        }

        // stop the loop
        if(position == 4){
            stop = 1;
        }
        
    }


}
# Modified 2025-08-11 10:24:29
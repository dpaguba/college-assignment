#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

/**
 * The selectable arguments, with the exit entry last.
 */
static const char *const ENTRIES[] = {"-l", "-a", "-t", "exit"};
static const int ENTRY_COUNT = 4;

/**
 * Print the numbered menu.
 */
static void show_menu(void)
{
    for (int index = 0; index < ENTRY_COUNT; index++) {
        printf("%d. %s\n", index + 1, ENTRIES[index]);
    }
}

/**
 * Read a menu choice, returning the entry index or -1 on bad input.
 *
 * A non-numeric input leaves the offending characters in the buffer, so they
 * are discarded before returning. Without that the next read fails the same
 * way and the program spins.
 */
static int read_choice(void)
{
    int choice;

    printf("Auswahl: ");
    if (scanf("%d", &choice) != 1) {
        int discarded;
        while ((discarded = getchar()) != '\n' && discarded != EOF) {
            continue;
        }
        return -1;
    }

    if (choice < 1 || choice > ENTRY_COUNT) {
        return -1;
    }

    return choice - 1;
}

/**
 * Run ls with one argument in a child process and wait for it.
 *
 * fork returns twice: zero in the child, the child's pid in the parent. The
 * child replaces itself with ls through execlp, which returns only on failure,
 * so the code after it is the error path and nothing else.
 *
 * The parent waits, which is what keeps the child from becoming a zombie and
 * what makes the menu reappear only after ls has finished.
 */
static int run_ls(const char *argument)
{
    pid_t child = fork();

    if (child < 0) {
        perror("fork");
        return -1;
    }

    if (child == 0) {
        execlp("ls", "ls", argument, (char *)NULL);
        perror("execlp");
        _exit(EXIT_FAILURE);
    }

    int status;
    if (waitpid(child, &status, 0) < 0) {
        perror("waitpid");
        return -1;
    }

    printf("PID von ls: %d\n", (int)child);

    if (WIFEXITED(status) && WEXITSTATUS(status) != 0) {
        fprintf(stderr, "ls exited with status %d\n", WEXITSTATUS(status));
    }

    return 0;
}

int main(void)
{
    for (;;) {
        show_menu();

        int choice = read_choice();
        if (choice < 0) {
            fprintf(stderr, "Ungueltige Eingabe\n");
            continue;
        }

        printf("Es wurde %s gewaehlt\n", ENTRIES[choice]);

        if (choice == ENTRY_COUNT - 1) {
            return EXIT_SUCCESS;
        }

        if (run_ls(ENTRIES[choice]) != 0) {
            return EXIT_FAILURE;
        }
    }
}

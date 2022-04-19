#include <errno.h>
#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define ANZ_GAESTE 12
#define ANZ_SERVICEK 4
#define ANZ_UMRUEHREN 5
#define TROEDEL_DAUER 1

/**
 * The guests one member of staff is responsible for.
 *
 * The argument has to outlive pthread_create, which returns before the thread
 * runs. An array in main provides that; a local in a loop body would not, and
 * the thread would read a stack frame that no longer exists.
 */
struct bedienliste {
    int nummer;
    int gaeste[ANZ_GAESTE];
    int anzahl;
};

static int bediente_gaeste = 0;

/**
 * Fill in which guests belong to one member of staff.
 *
 * The staff number is passed in rather than derived from pthread_self, because
 * a pthread_t is opaque and unordered: it is unique and it is not a small
 * integer, so it cannot index anything.
 */
static void bedienliste_fuer(struct bedienliste *liste, int nummer)
{
    liste->nummer = nummer;
    liste->anzahl = 0;

    for (int gast = nummer; gast < ANZ_GAESTE; gast += ANZ_SERVICEK) {
        liste->gaeste[liste->anzahl++] = gast;
    }
}

/**
 * Waste a little time before starting work.
 */
static void troedeln(void)
{
    struct timespec pause = {.tv_sec = 0, .tv_nsec = TROEDEL_DAUER * 1000000L};
    nanosleep(&pause, NULL);
}

/**
 * Cook for one guest by stirring a fixed number of times.
 */
static void kochen(int gast)
{
    for (int runde = 0; runde < ANZ_UMRUEHREN; runde++) {
        printf("Gast %d: Umruehren %d\n", gast, runde + 1);
    }
}

/**
 * The work of one member of staff.
 *
 * The counter is shared and unguarded, which is the point of this part of the
 * assignment: reading it, adding one and writing it back is three operations,
 * and another thread can run between them.
 */
static void *bedienen(void *argument)
{
    struct bedienliste *liste = argument;

    troedeln();

    for (int index = 0; index < liste->anzahl; index++) {
        kochen(liste->gaeste[index]);
        int gelesen = bediente_gaeste;
        bediente_gaeste = gelesen + 1;
    }

    return NULL;
}

int main(void)
{
    pthread_t threads[ANZ_SERVICEK];
    struct bedienliste listen[ANZ_SERVICEK];

    for (int nummer = 0; nummer < ANZ_SERVICEK; nummer++) {
        bedienliste_fuer(&listen[nummer], nummer);

        int fehler = pthread_create(&threads[nummer], NULL, bedienen, &listen[nummer]);
        if (fehler != 0) {
            fprintf(stderr, "pthread_create: %s\n", strerror(fehler));
            return EXIT_FAILURE;
        }
    }

    for (int nummer = 0; nummer < ANZ_SERVICEK; nummer++) {
        int fehler = pthread_join(threads[nummer], NULL);
        if (fehler != 0) {
            fprintf(stderr, "pthread_join: %s\n", strerror(fehler));
            return EXIT_FAILURE;
        }
    }

    printf("Bediente Gaeste: %d von %d\n", bediente_gaeste, ANZ_GAESTE);
    return EXIT_SUCCESS;
}

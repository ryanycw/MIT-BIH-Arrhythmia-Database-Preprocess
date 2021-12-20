#include <stdio.h>
#include <wfdb/wfdb.h>

int main(argc, argv)
int argc;
char *argv[];
{

    int osigfopen(WFDB_Siginfo *siarray, unsigned int nsig);

    WFDB_Siginfo s[2]; int i, nsig;
    /*
        S related signal need to be 
    */
    if (osigfopen(s, nsig) < nsig) exit(1);
    for (i = 0; i < nsig; i++)
        printf("signal %d will be written into ‘%s’\n", i, s[i].fname);
}
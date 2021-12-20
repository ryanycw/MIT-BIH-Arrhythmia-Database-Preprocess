#include <stdio.h>
#include <wfdb/wfdb.h>

int main(argc, argv)
int argc;
char *argv[];
{
    WFDB_Siginfo s[2]; int i, nsig;
    nsig = osigopen("8l", s, 2);
    for (i = 0; i < nsig; i++)
    printf("signal %d will be written into ‘%s’\n", i, s[i].fname);
}

#include <stdio.h>
#include <wfdb/wfdb.h>

int main()
{
    WFDB_Sample v[2];
    WFDB_Siginfo s[2];

    if (isigopen("100s", s, 1) < 1) exit(1);

    for (int i = 0; i < 10; i++) {
	if (getvec(v) < 0)
	    break;
	printf("%d\t%d\n", v[0], v[1]);
    }
    exit(0);
}
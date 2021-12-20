#include <stdio.h> 
#include <wfdb/wfdb.h>

int main() {
    WFDB_Anninfo a; 
    WFDB_Annotation annot;
    WFDB_Frequency f = (WFDB_Frequency)0;

    a.name = "atr"; 
    a.stat = WFDB_READ; 

    if (annopen("100s", &a, 1) < 0) exit(1);
    if (f <= (WFDB_Frequency)0) f = sampfreq("100s");
    printf("Frequency: %f\n",f);


    setiafreq(0, f);
    printf("Result: %f\n",getiafreq(0));

    setiafreq(0, 260);
    printf("Result: %f\n",getiafreq(0));

    //while (getann(0, &annot) == 0)
    //    printf("%s %s\n", mstimstr(annot.time), annstr(annot.anntyp)); exit(0);
}
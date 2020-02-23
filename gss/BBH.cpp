#include <iostream>
#include <string>
#include <fstream>
#include <cstring>

using namespace std;

int main(int NUMARGS, char* ARGS[]) {
    int ARGNUM = 1;
    while (ARGNUM < NUMARGS) {
        cout << "file " << ARGS[ARGNUM] << ":" << endl;
        ifstream INFILE(ARGS[ARGNUM]);
        if (INFILE.is_open()) {
            string LINE;
            while (getline(INFILE, LINE)) {
                char *ARRAY[3];
                int i = 0;
                char* LINE_array = strdup(LINE.c_str());
                ARRAY[i] = strtok(LINE_array,"\t");
                //cout << LINE.c_str() << endl;
                while(ARRAY[i]!=nullptr){
                    ARRAY[++i] = strtok(nullptr,"\t");
                }
                cout << ARRAY[0] << "\t" << ARRAY[1] << "\t" << ARRAY[2] << endl;
            }
        }
        INFILE.close();
        ARGNUM ++;
    }
    return 0;
}

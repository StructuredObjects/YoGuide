#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/stat.h>
#include <unistd.h>

struct Item
{
    char    *name;
    int     id;
    char    *url;
    char    *price;
    char    *update;
};

char *readFile(const char *filepath/*, char *dest*/);

int main()
{
    char *items_db = readFile("items.txt");
    char *lines = malloc(strlen(items_db));

    char *temp;
    int arr_i = 0;
    for(int i = 0; i <= strlen(items_db); i++)
    {
        realloc(&lines[arr_i], strlen(&lines[arr_i])+strlen(&items_db[i]));
        strcat(&lines[arr_i], &items_db[i]);

        if(items_db[i] == '\n') {
            arr_i++;
            printf("end");
            exit(0);
        }
    }

    free(items_db);
    free(lines);
}

char *readFile(const char *filepath/*, char *dest*/)
{
	long fd_size;
	FILE *fd = fopen(filepath, "r");
	if(fd == NULL) return "";

	// retrieve total character count in file
	fseek(fd, 0, SEEK_END);
	fd_size = ftell(fd);
	fseek(fd, 0, SEEK_SET);

	// retrieve file data
	char *filedata = malloc(sizeof(char *) + fd_size);
	fread(filedata, 1, fd_size, fd);

	fclose(fd);
	return filedata;
}
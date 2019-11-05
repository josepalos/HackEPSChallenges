#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <ctype.h>
#include <limits.h>

void parse_sets_file(const char * filename, int chasen);

int main(int argc, char* argv[]){
	clock_t start, end;
	double cpu_time;
	int chase;
	char* filename;

	if (argc < 3){
		fprintf(stderr, "USAGE: %s <chase_value> <sets_file>\n", argv[0]);
		return 1;
	}
	
	chase = atol(argv[1]);
	filename = argv[2];

	printf("Parsing sets...\n");
	start = clock();
	parse_sets_file(filename, chase);
	end = clock();
	cpu_time = ((double) (end - start)) / CLOCKS_PER_SEC;

	printf("\n");
	printf("Parsing time: %f\n", cpu_time);
}

int get_next_int(FILE *fp, int * next_digit){
	int current_value;
	int found = -1;
	char current_c;

	current_value = 0;
	do{
		current_c = (char) fgetc(fp);
		if(!isdigit(current_c)){
			break;
		}
		found = 0;
		current_value = current_value * 10 + (current_c - '0');
	}while(1);
	*next_digit = current_value;

	return found;
}

void seek_to_vector_start(FILE *fp){
	char current_c;
	// Read until vector starts
	do{
		current_c = (char) fgetc(fp);
	}while(current_c != EOF && current_c != '[');
}

int parse_set(FILE *fp, int chasen){
	int current_value;
	int found_value;
	int distance;
	int min_distance = INT_MAX;

	seek_to_vector_start(fp);

	// Read integers from vector
	current_value = 0;
	while(get_next_int(fp, &current_value) != -1){
		distance = abs(current_value - chasen);
		if(distance < min_distance){
			min_distance = distance;
			found_value = current_value;
		}
	}
	return found_value;
}

void parse_sets_file(const char * filename, int chase){
	int v1, v2;
	FILE *fp = fopen(filename, "r");
	if(fp == NULL){
		fprintf(stderr, "ERROR parsing file");
		exit(1);
	}

	v1 = parse_set(fp, chase);
	v2 = parse_set(fp, chase);

	printf("Value pair is (%d, %d)\n", v1, v2);

	fclose(fp);
}

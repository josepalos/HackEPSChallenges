#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_ELEMENTS_TO_PRINT 10
#define INITIAL_CAPACITY 10
#define MIN(x, y) (((x) < (y)) ? (x) : (y))

typedef struct {
	int * values;
	size_t length;
	size_t capacity;
} Array;

void load_sets(const char * filename, Array * a, Array * b);
void push(Array *arr, int value);
void print_array(Array arr);
int chase_value(Array array, int value);

int main(int argc, char* argv[]){
	clock_t start, end;
	double load_cpu_time, chase_cpu_time;
	Array a;
	Array b;
	int chase;
	char* filename;

	if (argc < 3){
		fprintf(stderr, "USAGE: %s <chase_value> <sets_file>\n", argv[0]);
		return 1;
	}
	
	chase = atol(argv[1]);
	filename = argv[2];

	printf("Loading sets...\n");
	start = clock();
	load_sets(filename, &a, &b);
	end = clock();
	load_cpu_time = ((double) (end - start)) / CLOCKS_PER_SEC;

	printf("Loaded\n");

	print_array(a);
	print_array(b);

	int v1, v2;
	printf("Start chasing value %d...\n", chase);
	start = clock();

	v1 = chase_value(a, chase);
	free(a.values);

	v2 = chase_value(b, chase);
	free(b.values);

	end = clock();
	chase_cpu_time = ((double) (end - start)) / CLOCKS_PER_SEC;

	printf("\n");
	printf("Loading time: %f\n", load_cpu_time);
	printf("Chasing time: %f\n", chase_cpu_time);
	printf("Total time: %f\n", load_cpu_time + chase_cpu_time);
	printf("Pair is (%d, %d)\n", v1, v2);

}

void print_array(Array arr){
	int max_elements = MIN(MAX_ELEMENTS_TO_PRINT, arr.length);
	for(int i=0; i < max_elements; i++){
		printf("%d ", arr.values[i]);
	}
	if (max_elements == MAX_ELEMENTS_TO_PRINT)
		printf(" ... (truncated %d elements)", (int) (arr.length - max_elements));
	printf("\n");
}

void push(Array *arr, int value){
	if (arr->length >= arr->capacity){
		int* new_arr;
		arr->capacity *= 2;
		new_arr = (int*) realloc(arr->values, arr->capacity * sizeof(arr->values[0]));
		if (!new_arr){
			fprintf(stderr, "ERROR\n");
		}else{
			arr->values = new_arr;
		}
	}

	arr->values[arr->length] = value;
	arr->length += 1;
}

void parse_set(FILE *fp, Array * arr){
	char current_c;
	int current_value;

	arr->values = (int*) malloc(INITIAL_CAPACITY * sizeof(int));
	arr->length = 0;
	arr->capacity = INITIAL_CAPACITY;

	// Read until vector starts
	do{
		current_c = (char) fgetc(fp);
	}while(current_c != EOF && current_c != '[');

	// Read integers from vector
	current_value = 0;
	while(current_c != EOF){
		current_c = (char) fgetc(fp);
		
		if (current_c == ','){
			push(arr, current_value);
			current_value = 0;
		} else if (current_c == EOF || current_c == ']'){
			push(arr, current_value);
			current_value = 0;
			break;
		} else {
			current_value = current_value * 10 + (current_c - '0');
		}
	}
}

void load_sets(const char * filename, Array * a, Array * b){
	FILE *fp = fopen(filename, "r");
	if(fp == NULL){
		fprintf(stderr, "ERROR!");
		exit(1);
	}

	parse_set(fp, a);
	parse_set(fp, b);

	fclose(fp);
}

void merge(int* values, int start, int middle, int end){
	int tmp1_len = middle - start + 1;
	int tmp2_len = end - middle;
	int *tmp1 = (int*) malloc(tmp1_len * sizeof(int));
	int *tmp2 = (int*) malloc(tmp2_len * sizeof(int));
	int i, j, current;
	i = j = 0;
	current = start;

	memcpy(tmp1, values + start,  (tmp1_len) * sizeof(int));
	memcpy(tmp2, values + middle + 1, (tmp2_len) * sizeof(int));

	while(i < tmp1_len && j < tmp2_len){
		if(tmp1[i] <= tmp2[j]){
			values[current] = tmp1[i];
			i++;
		}else{
			values[current] = tmp2[j];
			j++;
		}
		current++;
	}

	// Copy remaining elements
	while(i < tmp1_len){
		values[current] = tmp1[i];
		i++;
		current++;
	}
	free(tmp1);
	while(j < tmp2_len){
		values[current] = tmp2[j];
		j++;
		current++;
	}
	free(tmp2);
}

void merge_sort(int* values, int start, int end){
	if (start < end){
		int middle = start + (end - start) / 2;

		merge_sort(values, start, middle);
		merge_sort(values, middle+1, end);

		merge(values, start, middle, end);
	}
}

int binary_search(int* values, int length, int value){
	int start = 0;
	int end = length;
	int middle;
	int middle_value;

	while(start < end){
		middle = (start + (end - start) / 2);
		middle_value = values[middle];
		if (middle_value == value){
			return middle;
		}else if(middle_value < value){
			start = middle + 1;	
		}else{
			end = middle;
		}
	}
    if(middle_value < value)
		return middle + 1;
	else
		return middle;
}

int chase_value(Array array, int value){
	int pos;
	int lower, upper;
	clock_t start, end;
	double cpu_time;
	
	start = clock();
	merge_sort(array.values, 0, array.length-1);
	end = clock();
	cpu_time = ((double) (end - start)) / CLOCKS_PER_SEC;
	printf("Sorting values took %f seconds\n", cpu_time);

	printf("Values sorted:\n");
	print_array(array);

	start = clock();
	pos = binary_search(array.values, array.length, value);
	end = clock();
	cpu_time = ((double) (end - start)) / CLOCKS_PER_SEC;

	printf("Search took %f seconds\n", cpu_time);
	printf("Chasen value (%d) should be at position %d\n", value, pos);
	
	if (pos == 0){
		return array.values[pos];
	} else {
		lower = array.values[pos - 1];
		upper = array.values[pos];
		if (abs(lower - value) < abs(upper - value)){
			return lower;
		}else{
			return upper;
		}
	}
}

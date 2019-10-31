#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#define MAX_ELEMENTS_TO_PRINT 10
#define INITIAL_CAPACITY 10
#define MIN(x, y) (((x) < (y)) ? (x) : (y))

typedef struct {
	int value;
	int vector_id;
} VectorValue;

typedef struct {
	VectorValue *values;
	size_t length;
	size_t capacity;
} Array;

void load_sets(const char * filename, Array * a, Array * b);
void push(Array *arr, VectorValue value);
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

	printf("Loading sets...");
	start = clock();
	load_sets(filename, &a, &b);
	end = clock();
	load_cpu_time = ((double) (end - start)) / CLOCKS_PER_SEC;

	printf("Loaded\n");

	print_array(a);
	print_array(b);

	int v1, v2;
	printf("Start chasing...\n");
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
		printf("%d ", arr.values[i].value);
	}
	if (max_elements == MAX_ELEMENTS_TO_PRINT)
		printf(" ... (truncated %d elements)", arr.length - max_elements);
	printf("\n");
}

void push(Array *arr, VectorValue value){
	if (arr->length >= arr->capacity){
		VectorValue* new_arr;
		arr->capacity *= 2;
		new_arr = (VectorValue*) realloc(arr->values, arr->capacity * sizeof(arr->values[0]));
		if (!new_arr){
			fprintf(stderr, "ERROR\n");
		}else{
			arr->values = new_arr;
		}
	}

	arr->values[arr->length] = value;
	arr->length += 1;
}

void load_sets(const char * filename, Array * a, Array * b){
	FILE *fp = fopen(filename, "r");
	if(fp == NULL){
		fprintf(stderr, "ERROR!");
		exit(1);
	}

	char current_c;
	VectorValue current_value;
    a->values = (VectorValue*) malloc(INITIAL_CAPACITY * sizeof(VectorValue));
	a->length = 0;
	a->capacity = INITIAL_CAPACITY;

    b->values = (VectorValue*) malloc(INITIAL_CAPACITY * sizeof(VectorValue));
	b->length = 0;
	b->capacity = INITIAL_CAPACITY;

	// Read until vector start
	do{
		current_c = (char) fgetc(fp);
	}while(current_c != EOF && current_c != '[');

	// Read integers for A
	current_value.value = 0;
	current_value.vector_id = 0;
	while(current_c != EOF){
		current_c = (char) fgetc(fp);
		if (current_c == ','){
			push(a, current_value);
			current_value.value = 0;
		} else if (current_c == EOF || current_c == ']'){
			push(a, current_value);
			current_value.value = 0;
			break;
		} else{
			current_value.value = current_value.value * 10 + (current_c - '0');
		}
	}

	// Read until vector start
	do{
		current_c = (char) fgetc(fp);
	}while(current_c != EOF && current_c != '[');

	// Read integers for B
	current_value.value = 0;
	current_value.vector_id = 1;
	while(current_c != EOF){
		current_c = (char) fgetc(fp);
		if (current_c == ','){
			push(b, current_value);
			current_value.value = 0;
		} else if (current_c == EOF || current_c == ']'){
			push(b, current_value);
			current_value.value = 0;
			break;
		} else{
			current_value.value = current_value.value * 10 + (current_c - '0');
		}
	}

	fclose(fp);
}

void merge(VectorValue *values, int start, int middle, int end){
	int tmp1_len = middle - start + 1;
	int tmp2_len = end - middle;
	VectorValue *tmp1 = (VectorValue*) malloc(tmp1_len * sizeof(VectorValue));
	VectorValue *tmp2 = (VectorValue*) malloc(tmp2_len * sizeof(VectorValue));
	int i, j, current;
	i = j = 0;
	current = start;

	memcpy(tmp1, values + start,  (tmp1_len) * sizeof(VectorValue));
	memcpy(tmp2, values + middle + 1, (tmp2_len) * sizeof(VectorValue));

	while(i < tmp1_len && j < tmp2_len){
		if(tmp1[i].value <= tmp2[j].value){
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

void merge_sort(VectorValue* values, int start, int end){
	if (start < end){
		int middle = start + (end - start) / 2;

		merge_sort(values, start, middle);
		merge_sort(values, middle+1, end);

		merge(values, start, middle, end);
	}
}

int binary_search(VectorValue *values, int length, int value){
	int start = 0;
	int end = length;
	int middle;
	int middle_value;

	while(start < end){
		middle = (start + (end - start) / 2);
		middle_value = values[middle].value;
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
	VectorValue current_value;

	merge_sort(array.values, 0, array.length-1);

	printf("Values sorted:\n");
	print_array(array);

	pos = binary_search(array.values, array.length, value);
	printf("Chasen value (%d) should be at position %d\n", value, pos);
	
	if (pos == 0){
		return array.values[pos].value;
	}else if (0 < pos && pos < array.length){
		lower = array.values[pos - 1].value;
		upper = array.values[pos].value;
		if (abs(lower - value) < abs(upper - value)){
			return lower;
		}else{
			return upper;
		}
	}
}

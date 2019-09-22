#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <string.h>
#include <stdlib.h>
#include <pthread.h>
#include <sys/time.h>
//#include </usr/local/include/libpq-fe.h>

#define default_char_array_size 500
#define number_of_threads 1

int file_size = 700017;

//lpq

/*Stores the information of a vcf line reggarding to the snp*/
typedef struct {
    char *id;
    char *ref;
    char *alt;
    char *format;
    char *pos;
} VCFFields;

/*Stores the indexes of the important information*/
typedef struct {
    int id;
    int ref;
    int alt;
    int format;
    int pos;
} VCFMap;

typedef struct {
    char *id;
} Individual;

typedef struct {
    int index[2]; /*Position 0 stores the index of GT and position 1 the index of DP*/
} FormatFieldMap;

typedef struct {
    char *genotype;
    char *depth;
} IndividualInformation;

typedef struct {
    VCFMap *vcf_map;
    char **line;
    char *population_id;
    Individual *list_of_individuals;
    int n_of_individuals;
    int n_of_lines;
    int id;
} Argument;

void GenerateInsertPopulation(char population_id[], char description[], FILE *f) {
    char query[default_char_array_size];

    strcpy(query, population_id);
    strcat(query, ",");
    strcat(query, description);
    strcat(query, "\n");

    fputs(query, f);

}

void GenerateInsertIndividual(char individual_id[], char population_id[], char description[], char phenotype[], FILE *f) {
    char query[default_char_array_size];

    strcpy(query, individual_id);
    strcat(query, ",");
    strcat(query, description);
    strcat(query, ",");
    strcat(query, phenotype);
    strcat(query, ",");
    strcat(query, population_id);
    strcat(query, "\n");

    fputs(query, f);
}

void GenerateInsertVariations(VCFFields *vcf_fields, IndividualInformation *individual_information, char *population_id, int n_of_individuals, FILE *fV) {
    char query[default_char_array_size];

    strcpy(query, vcf_fields->id);
    strcat(query, ",");
    strcat(query, vcf_fields->pos);
    strcat(query, ",");
    strcat(query, (vcf_fields->ref));
    strcat(query, ",");
    strcat(query, (vcf_fields->alt));
    strcat(query, ",.,");
    strcat(query, population_id);

    fputs(query, fV);
    fputs(",\"{", fV);
    fputs(individual_information[0].genotype, fV);
    int i;
    for (i = 1; i < n_of_individuals; i++) {
        fputs(",", fV);
        fputs(individual_information[i].genotype, fV);
    }
    fputs("}\"\n", fV);

}

void MapFormatField(char *format_field, FormatFieldMap *format_field_map) {
    char token[] = {":"}, *word, *last;
    int i = 0;
    format_field_map->index[0] = -1;
    format_field_map->index[1] = -1;
    for (word = strtok_r(format_field, token, &last); word; word = strtok_r(NULL, token, &last), i++) {
        if (strcmp(word, "GT") == 0) {
            format_field_map->index[0] = i;
        } else if (strcmp(word, "DP") == 0) {
            format_field_map->index[1] = i;
        }
    }
}

void ProcessHeaderLine(VCFMap *vcf_map, char *line, Individual **list_of_individuals, int *size_list_of_individuals) {
    int i = 0;
    char token[] = {"\t"};
    char *word, *last;
    for (word = strtok_r(line, token, &last); word; word = strtok_r(NULL, token, &last), i++) {
        if (strcmp(word, "FORMAT") == 0) {
            vcf_map->format = i;
            break;
        }

        if (strcmp(word, "ID") == 0) {
            vcf_map->id = i;
            continue;
        }

        if (strcmp(word, "REF") == 0) {
            vcf_map->ref = i;
            continue;
        }

        if (strcmp(word, "ALT") == 0) {
            vcf_map->alt = i;
            continue;
        }

        if (strcmp(word, "POS") == 0) {
            vcf_map->pos = i;
            continue;
        }
    }

    word = strtok_r(NULL, token, &last);
    i = 0;
    *list_of_individuals = (Individual*) malloc(sizeof (Individual));
    int size = 1;
    char *new_word;

    while (word) {
        if (i == size) {
            size = 2 * i;
            *list_of_individuals = (Individual*) realloc(*list_of_individuals, size * sizeof (Individual));

        }
        (*list_of_individuals)[i].id = word;
        i++;
        word = strtok_r(NULL, token, &last);
    }
    i--;
    /*Correct list_of_individuals' size*/
    *list_of_individuals = (Individual*) realloc(*list_of_individuals, i * sizeof (Individual));
    *size_list_of_individuals = i;
}

void ProcessIndividualInformation(char *individual_field, IndividualInformation *individuals_information, FormatFieldMap *format_field_map) {
    char token[] = {":"}, *word, *last;
    int i = 0;

    for (word = strtok_r(individual_field, token, &last); word; word = strtok_r(NULL, token, &last), i++) {
        if (i == format_field_map->index[0]) {
            individuals_information->genotype = word;
        } else if (i == format_field_map->index[1])
            individuals_information->depth = word;
    }
}

void ProcessLine(VCFMap *vcf_map, VCFFields *vcf_fields, char *line, IndividualInformation *individuals_information, FormatFieldMap *format_field_map) {
    char *word, *last;
    char token[] = {"\t"};
    int i = 0;
    /*Process SNP information*/
    for (word = strtok_r(line, token, &last); word; word = strtok_r(NULL, token, &last), i++) {

        if (vcf_map->id == i)
            vcf_fields->id = word;

        else if (vcf_map->ref == i)
            vcf_fields->ref = word;

        else if (vcf_map->alt == i)
            vcf_fields->alt = word;

        else if (vcf_map->format == i){
            vcf_fields->format = word;
            break;
          }

        else if (vcf_map->pos == i)
            vcf_fields->pos = word;
    }


    /*Get individuals information*/
    i = 0;
    MapFormatField(vcf_fields->format, format_field_map);
    for (word = strtok_r(NULL, token, &last); word; word = strtok_r(NULL, token, &last), i++) {
        ProcessIndividualInformation(word, (individuals_information + i), format_field_map);
    }
}

void *ProcessSnp(void *args) {
    Argument *argument = (Argument*) args;

    char fVName[default_char_array_size];

    strcpy(fVName, "/home/bruno/Documents/Unifesp/ICBD/csv_files/Variations");
    strcat(fVName, ".csv");

    FILE *fV = fopen(fVName, "ab+");

    IndividualInformation *individuals_information = (IndividualInformation*) malloc(sizeof (IndividualInformation) * argument->n_of_individuals);
    FormatFieldMap *format_field_map = (FormatFieldMap*) malloc(sizeof (FormatFieldMap) * (argument->n_of_lines));
    VCFFields *vcf_fields = (VCFFields*) malloc(sizeof (VCFFields) * (argument->n_of_lines));

    for (int i = 0; i < argument->n_of_lines; i++){
        ProcessLine(argument->vcf_map, &vcf_fields[i], argument->line[i], individuals_information, &format_field_map[i]);
        GenerateInsertVariations(&vcf_fields[i], individuals_information, argument->population_id, argument->n_of_individuals, fV);

        free(argument->line[i]);
    }

    fclose(fV);

    free(individuals_information);
    free(format_field_map);
    free(vcf_fields);

    return NULL;
}

void ReadFile(char *fileName, VCFMap *vcf_map, Individual **list_of_individuals, char *population_id) {

    size_t header_size = 100;
    char *header = (char*) malloc(header_size * sizeof (char));

    FILE *fp = fopen(fileName, "r");

    /*pass through header lines*/
    while (getline(&header, &header_size, fp) > 0)
        if (header[1] != '#')
            break;

    char token[] = {"\t"}, *word;
    char *lasts;

    int n_of_individuals;

    ProcessHeaderLine(vcf_map, header, list_of_individuals, &n_of_individuals);
    int i;

    FILE *f = fopen("/home/bruno/Documents/Unifesp/ICBD/csv_files/inserts_individual.csv", "ab+");

    for (i = 0; i < n_of_individuals; i++) {
        GenerateInsertIndividual((*list_of_individuals)[i].id, population_id, ".", ".", f);
    }

    fclose(f);

    char **snp_lines = (char**) malloc(sizeof (char*) * file_size);
    size_t buffer_size = 100;
    char *buffer = (char*) malloc(buffer_size * sizeof (char));
    /*Read all lines of the file*/
    i = 0;

    while (getline(&buffer, &buffer_size, fp) > 0) {
        snp_lines[i] = buffer;
        buffer = (char*) malloc(buffer_size * sizeof (char));
        i++;
    }


    free(buffer);

    file_size = i;


    pthread_t *threads = (pthread_t*) malloc(sizeof(pthread_t)*number_of_threads);

    Argument *argument = (Argument*) malloc(sizeof(Argument)*number_of_threads);

    for (i = 0; i < number_of_threads; i++) {

        argument[i].line = (snp_lines + (int) (i * (int) file_size / number_of_threads));
        argument[i].list_of_individuals = *list_of_individuals;
        argument[i].n_of_individuals = n_of_individuals;
        argument[i].n_of_lines = (int) (file_size) / number_of_threads;
        argument[i].population_id = population_id;
        argument[i].vcf_map = vcf_map;
        argument[i].id = i + 1;

        pthread_create(&threads[i], NULL, ProcessSnp, (void *) (argument + i));

    }

    for (i = 0; i < number_of_threads; i++)
        pthread_join(threads[i], NULL);

    free(threads);
    free(argument);
}

int main(int argc, char *argv[]) {


    char file_path[] = {"/home/bruno/Documents/Unifesp/ICBD/vcf_files/HDRA-G6-4-RDP1-RDP2-NIAS.AGCT.vcf"};
    VCFMap vcf_map;

    Individual *list_of_individuals;
    char population_id[] = {"rice1"};
    char population_description[] = {"rice"};

    FILE *f = fopen("/home/bruno/Documents/Unifesp/ICBD/csv_files/inserts_population.csv", "ab+");
    GenerateInsertPopulation(population_id, population_description, f);
    fclose(f);

    ReadFile(file_path, &vcf_map, &list_of_individuals, population_id);

}

#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <string.h>
#include <string>
#include <stdlib.h>
#include <sys/time.h>
#include <regex>

#define default_char_array_size 500
#define number_of_threads 1

int file_size = 700017;

/*Stores the information of a vcf line reggarding to the snp*/
typedef struct {
    char *id;
    char *ref;
    char *alt;
    char *format;
    char *pos;
    char *chrom;
} VCFFields;

/*Stores the indexes of the important information*/
typedef struct {
    int id;
    int ref;
    int alt;
    int format;
    int pos;
    int chrom;
} VCFMap;

typedef struct {
    int id;
    char *individual_identification;
    char *genotype;
    char *depth;
} Individual;

typedef struct {
    int index[2]; /*Position 0 stores the index of GT and position 1 the index of DP*/
} FormatFieldMap;

void GenerateInsertPopulation(char population_id[], char description[], FILE *f) {
    char *query = (char*) malloc(sizeof(char) * default_char_array_size);

    strcpy(query, population_id);
    strcat(query, ",");
    strcat(query, description);
    strcat(query, "\n");

    fputs(query, f);

    free(query);

}

void GenerateInsertIndividual(int id, char individual_id[], char population_id[], char description[], char phenotype[], FILE *f) {
    char *query = (char*) malloc(sizeof(char) * default_char_array_size);

    strcpy(query, std::to_string(id).c_str());
    strcat(query, ",");
    strcat(query, individual_id);
    strcat(query, ",");
    strcat(query, description);
    strcat(query, ",");
    strcat(query, phenotype);
    strcat(query, ",");
    strcat(query, population_id);
    strcat(query, "\n");
    fputs(query, f);
    free(query);
}
variation_line_fields
void GenerateInsertVariations(int variation_id, VCFFields *vcf_fields, char *population_id, int n_of_individuals, FILE *fV, Individual *individuals) {
    char *query = (char*) malloc(sizeof(char) * default_char_array_size);

    strcpy(query, std::to_string(variation_id).c_str());
    strcat(query, ",");
    strcat(query, vcf_fields->chrom);
    strcat(query, ",");
    strcat(query, vcf_fields->id);
    strcat(query, ",");
    strcat(query, vcf_fields->pos);
    strcat(query, ",");
    strcat(query, (vcf_fields->ref));
    strcat(query, ",");
    strcat(query, (vcf_fields->alt));
    strcat(query, ",.,");
    strcat(query, population_id);
    strcat(query, "\n");
    fputs(query, fV);
    free(query);
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

void ProcessHeaderLine(VCFMap *vcf_map, char *line, Individual **individuals, int *size_list_of_individuals) {
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

        if (strcmp(word, "#CHROM") == 0) {
            vcf_map->chrom = i;
            continue;
        }
    }

    word = strtok_r(NULL, token, &last);
    i = 0;
    *individuals = (Individual*) malloc(sizeof (Individual));
    int size = 1;
    char *new_word;

    while (word) {
        if (i == size) {
            size *= 2;
            *individuals = (Individual*) realloc(*individuals, size * sizeof (Individual));

        }
        (*individuals)[i].id = i+1;
        (*individuals)[i].individual_identification = word;
        i++;
        word = strtok_r(NULL, token, &last);
    }
    i--;
    /*Correct list_of_individuals' size*/
    *individuals = (Individual*) realloc(*individuals, i * sizeof (Individual));
    *size_list_of_individuals = i;
}

void ProcessIndividualInformation(char *individual_field, Individual *individual, FormatFieldMap *format_field_map) {
    char token[] = {":"}, *word, *last;
    int i = 0;

    for (word = strtok_r(individual_field, token, &last); word; word = strtok_r(NULL, token, &last), i++) {
        if (i == format_field_map->index[0]) {
            individual->genotype = word;
        } else if (i == format_field_map->index[1])
            individual->depth = word;
    }
}

void ProcessLine(VCFMap *vcf_map, VCFFields *vcf_fields, char *line, Individual *individuals, FormatFieldMap *format_field_map) {
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

        else if (vcf_map->chrom == i)
            vcf_fields->chrom = word;
    }


    /*Get individuals information*/
    i = 0;
    MapFormatField(vcf_fields->format, format_field_map);
    for (word = strtok_r(NULL, token, &last); word; word = strtok_r(NULL, token, &last), i++) {
        ProcessIndividualInformation(word, (individuals + i), format_field_map);
    }
}

void ProcessSnp(char **snp_lines, Individual *individuals, int n_of_individuals, char *population_id, VCFMap *vcf_map) {

    char fVName[default_char_array_size];

    strcpy(fVName, "/home/bruno/Documentos/unifesp/tcc/arquivos/postgreSQL/variation_table_input.csv");

    FILE *fV = fopen(fVName, "w+");
    FormatFieldMap *format_field_map = (FormatFieldMap*) malloc(sizeof (FormatFieldMap) * file_size);
    VCFFields *vcf_fields = (VCFFields*) malloc(sizeof(VCFFields) * file_size);

    for (int i = 0; i < file_size; i++){
        ProcessLine(vcf_map, &vcf_fields[i], snp_lines[i], individuals, &format_field_map[i]);
        GenerateInsertVariations(i + 1, &vcf_fields[i], population_id, n_of_individuals, fV, individuals);
        free(snp_lines[i]);
    }


    fclose(fV);

    free(format_field_map);
    free(vcf_fields);

    return;
}

void ReadFile(char *fileName, VCFMap *vcf_map, Individual **individuals, char *population_id) {

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

    ProcessHeaderLine(vcf_map, header, individuals, &n_of_individuals);
    int i;

    FILE *f = fopen("/home/bruno/Documentos/unifesp/tcc/arquivos/postgreSQL/individual_table_input.csv", "ab+");

    for (i = 0; i < n_of_individuals; i++) {
        GenerateInsertIndividual((*individuals)[i].id, (*individuals)[i].individual_identification, population_id, ".", ".", f);
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
    fclose(fp);
    file_size = i;

    ProcessSnp(snp_lines, *individuals, n_of_individuals, population_id, vcf_map);
}

int main(int argc, char *argv[]) {
  //HDRA-G6-4-RDP1-RDP2-NIAS.AGCT

    char file_path[] = {"/home/bruno/Documentos/unifesp/tcc/arquivos/commons/HDRA-G6-4-RDP1-RDP2-NIAS.AGCT.vcf"};
    VCFMap vcf_map;

    Individual *list_of_individuals;
    char population_id[] = {"rice1"};
    char population_description[] = {"rice"};

    FILE *f = fopen("/home/bruno/Documentos/unifesp/tcc/arquivos/postgreSQL/population_table_input.csv", "ab+");
    GenerateInsertPopulation(population_id, population_description, f);
    fclose(f);

    ReadFile(file_path, &vcf_map, &list_of_individuals, population_id);

}

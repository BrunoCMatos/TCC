#include <stdio.h>
#include <unistd.h>
#include <sys/wait.h>
#include <string.h>
#include <stdlib.h>
#include </usr/local/include/omp.h>
#include </usr/local/include/libpq-fe.h>

#define default_char_array_size 200

int file_size = 80;

//lpq
/*Stores the information of a vcf line reggarding to the snp*/
typedef struct {
    char *id;
    char *ref;
    char *alt;
    char *format;
    char *chrom;
} VCFFields;

/*Stores the indexes of the important information*/
typedef struct {
    int id;
    int ref;
    int alt;
    int format;
    int chrom;
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

 PGconn *conn;
 PGresult *res;

void GenerateInsertPopulation(char population_id[], char description[]) {
    char query[default_char_array_size];

    strcpy(query, "INSERT INTO POPULATION VALUES ('");
    strcat(query, population_id);
    strcat(query, "', '");
    strcat(query, description);
    strcat(query, "')");

    res = PQexec(conn, query);
    if (PQresultStatus(res) != PGRES_COMMAND_OK)
    {
        fprintf(stderr, "INSERT command failed: %s", PQerrorMessage(conn));
    }
    PQclear(res);

}

void GenerateInsertIndividual(char individual_id[], char population_id[], char description[], char phenotype[]) {
    char query[default_char_array_size];

    strcpy(query, "INSERT INTO INDIVIDUAL VALUES ('");
    strcat(query, individual_id);
    strcat(query, "', '");
    strcat(query, description);
    strcat(query, "', '");
    strcat(query, phenotype);
    strcat(query, "', '");
    strcat(query, population_id);
    strcat(query, "')");

    res = PQexec(conn, query);
    if (PQresultStatus(res) != PGRES_COMMAND_OK)
    {
        fprintf(stderr, "INSERT command failed: %s", PQerrorMessage(conn));
    }
    PQclear(res);

}

void GenerateInsertGenotype(char individual_id[], char population_id[], char variation_id[], char genotype[], char depth[]) {
    char query[default_char_array_size];

    strcpy(query, "INSERT INTO GENOTYPE VALUES ('");
    strcat(query, population_id);
    strcat(query, "','");
    strcat(query, individual_id);
    strcat(query, "', '");
    strcat(query, variation_id);
    strcat(query, "', '");
    strcat(query, genotype);
    strcat(query, "', '");
    strcat(query, depth);
    strcat(query, "')");

    res = PQexec(conn, query);
    if (PQresultStatus(res) != PGRES_COMMAND_OK)
    {
        fprintf(stderr, "INSERT command failed: %s", PQerrorMessage(conn));
    }
    PQclear(res);

}

void GenerateInsertVariations(VCFFields *vcf_fields, IndividualInformation *individual_information, char *population_id, Individual *individuals, int n_of_individuals) {
    char query[default_char_array_size];


    strcpy(query, "INSERT INTO VARIATION VALUES ('");
    strcat(query, vcf_fields->id);
    strcat(query, "', '");
    strcat(query, (vcf_fields->ref));
    strcat(query, "', '");
    strcat(query, (vcf_fields->alt));
    strcat(query, "', '");
    strcat(query, " ");
    strcat(query, "', '");
    strcat(query, population_id);
    strcat(query, "')");

    res = PQexec(conn, query);
    if (PQresultStatus(res) != PGRES_COMMAND_OK)
    {
        fprintf(stderr, "INSERT command failed: %s", PQerrorMessage(conn));
    }
    PQclear(res);

    int i;
    for (i = 0; i < n_of_individuals; i++) {
        //if (individual_information[i].depth != NULL)
        //  GenerateInsertGenotype(individuals[i].id, population_id, vcf_fields->id, individual_information[i].genotype, individual_information[i].depth);
        //else
        GenerateInsertGenotype(individuals[i].id, population_id, vcf_fields->id, individual_information[i].genotype, ".");
    }

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

        if (strcmp(word, "CHROM") == 0) {
            vcf_map->chrom = i;
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

        if (vcf_map->id == i) {
            vcf_fields->id = word;
        } else if (vcf_map->ref == i)
            vcf_fields->ref = word;

        else if (vcf_map->alt == i)
            vcf_fields->alt = word;

        else if (vcf_map->format == i) {
            vcf_fields->format = word;
            break;
        } else if (vcf_map->chrom == i)
            vcf_fields->chrom = word;

    }

    /*Get individuals information*/
    i = 0;
    MapFormatField(vcf_fields->format, format_field_map);
    for (word = strtok_r(NULL, token, &last); word; word = strtok_r(NULL, token, &last), i++) {
        ProcessIndividualInformation(word, (individuals_information + i), format_field_map);
    }

}

void ReadFile(char *fileName, VCFMap *vcf_map, VCFFields *vcf_fields, Individual **list_of_individuals, IndividualInformation **individuals_information, FormatFieldMap *format_field_map, char *population_id) {

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

    for (i = 0; i < n_of_individuals; i++) {
        GenerateInsertIndividual((*list_of_individuals)[i].id, population_id, " ", " ");
    }

    *individuals_information = (IndividualInformation*) malloc(sizeof (IndividualInformation) * n_of_individuals);

    char **snp_lines = (char**) malloc(sizeof(char*) * file_size);
    size_t buffer_size = 100;
    char *buffer = (char*) malloc(buffer_size * sizeof (char));
    /*Read all lines of the file*/
    i = 0;

    while (getline(&buffer, &buffer_size, fp) > 0){
        snp_lines[i] = buffer;
        buffer = (char*) malloc(buffer_size * sizeof (char));
        i++;
    }

    free(buffer);

    file_size = i - 1;

#pragma omp parallel for
    for (i = 0; i <= file_size; i++) {
        ProcessLine(vcf_map, vcf_fields, snp_lines[i], *individuals_information, format_field_map);
        GenerateInsertVariations(vcf_fields, *individuals_information, population_id, *list_of_individuals, n_of_individuals);
        free(snp_lines[i]);
    }


}

int main(int argc, char *argv[]) {
    const char *conninfo;
    conninfo = "host='localhost' dbname='BIODATA' user='carmonia' password='CarmoniaPower'";

    conn = PQconnectdb(conninfo);

    /*Check to see that the backend connection was successfully made */
    if (PQstatus(conn) != CONNECTION_OK) {
        fprintf(stderr, "Connection to database failed: %s", PQerrorMessage(conn));
    }

    res = PQexec(conn, "BEGIN");
    if (PQresultStatus(res) != PGRES_COMMAND_OK)
    {
        fprintf(stderr, "BEGIN command failed: %s", PQerrorMessage(conn));
        PQclear(res);
    }
    PQclear(res);

    char file_path[] = {"/Users/carmonia/Documents/saida3.vcf"};
    VCFMap vcf_map;
    VCFFields vcf_fields;
    Individual *list_of_individuals;
    IndividualInformation *individuals_information;
    FormatFieldMap format_field_map;
    char population_id[] = {"rice1"};
    char population_description[] = {"rice"};

    GenerateInsertPopulation(population_id, population_description);

    ReadFile(file_path, &vcf_map, &vcf_fields, &list_of_individuals, &individuals_information, &format_field_map, population_id);

    res = PQexec(conn, "END");
    PQclear(res);

    /* close the connection to the database and cleanup */
    PQfinish(conn);

}

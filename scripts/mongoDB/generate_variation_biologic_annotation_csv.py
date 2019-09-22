import threading
from pymongo import MongoClient

try:
    conn = MongoClient()
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

db = conn.snps
collection = db.variation

def separate_annotation_by_chromosome(file_path):
    annotation_by_chromosome = {}
    with open(file_path, "r") as file:
        file_lines = file.readlines()
        current_chrom = 1
        for i in range(12):
            annotation_by_chromosome[i + 1] = []
        for line in file_lines[1:]:
            line_fields = line.split('\t')
            chrom = line_fields[0].split('r')[1]
            if chrom.isdigit():
                chrom = int(chrom)
            else:
                break
            start_position = int(line_fields[3])
            end_position = int(line_fields[4])
            annotation = ""
            for x in line_fields[9].split("'"):
                annotation += " %s" % x
            if(current_chrom != chrom):
                current_chrom += 1
            annotation_by_chromosome[chrom].append([start_position, end_position, annotation])

    return annotation_by_chromosome

def fill_json(variation, annotations):
    string_annotations = "["
    for annotation in annotations:
        string_annotations += "\"%s\"," % str(annotation[2])
    string_annotations = string_annotations.replace("\n", "")
    string_annotations = string_annotations[:-1] + "]"
    variation_annotation_json = {
        "id" : variation[0],
        "chrom" : variation[1]
    }
    if len(string_annotations) > 1:
        variation_annotation_json ["variation_identification"] = variation[2]
        variation_annotation_json["pos"] = variation[3]
        variation_annotation_json["reference_allele"] = variation[4]
        variation_annotation_json["alternative_allele"] = variation[5]
        variation_annotation_json["annotations"] = string_annotations
    else:
        variation_annotation_json["variation_identification"] = variation[2]
        variation_annotation_json["pos"] = variation[3]
        variation_annotation_json["reference_allele"] = variation[4]
        variation_annotation_json["alternative_allele"] = variation[5]

    variation_annotation_json["population_id"] = str(variation[7])
    return variation_annotation_json

def func(variations, annotations, current_chrom):
    file_name = "annotations_chrom_" + str(current_chrom) + ".csv"
    print("Começando %s, tamanhos-> V: %s, A: %s" % (file_name, len(variations), len(annotations)))
    variations_annotations = []
    genotypes = []
    for variation in variations:
        annotations_from_this_variation = []
        for annotation in annotations:
            if (annotation[0] <= int(variation[3]) and annotation[1] >= int(variation[3])):
                annotations_from_this_variation.append(annotation)
        variations_annotations.append(fill_json(variation, annotations_from_this_variation))

        genotype_json = {
            "variation_identification": variation[2],
            "genotype": str(variation[8])
        }
        genotypes.append(genotype_json)

    print("Persistindo chromossomo " + str(current_chrom))
    collection.insert_many(variations_annotations)


    print("persistindo genotype")
    db.genotype.insert_many(genotypes)

#main
variations_csv = open("/home/brunocarmonia/Documents/Unifesp/ICBD/csv_files_postgresNoSQL/variation.csv", "r")
annotation_by_chromosome = separate_annotation_by_chromosome("/home/brunocarmonia/Documents/Unifesp/ICBD/IniciacaoCientifica/references/all.locus_brief_info.7.0")

variation_lines = []
current_chrom = 1
chrom_current_pool = {}
while(True):
    variation_line = variations_csv.readline()
    if (len(variation_line) != 0):
        variation_line_fields = variation_line.split('\t')

    if (len(variation_line) == 0 or int(variation_line_fields[1]) != current_chrom):
        chrom_current_pool[current_chrom] = variation_lines
        print(current_chrom)
        if (current_chrom % 4 == 0):
            threading.Thread(target=func, args=(chrom_current_pool[current_chrom - 3], annotation_by_chromosome[current_chrom - 3], current_chrom - 3)).start()
            threading.Thread(target=func, args=(chrom_current_pool[current_chrom - 2], annotation_by_chromosome[current_chrom - 2], current_chrom - 2)).start()
            threading.Thread(target=func, args=(chrom_current_pool[current_chrom - 1], annotation_by_chromosome[current_chrom - 1], current_chrom - 1)).start()
            threading.Thread(target=func, args=(chrom_current_pool[current_chrom], annotation_by_chromosome[current_chrom], current_chrom)).start()
            chrom_current_pool = {}
        current_chrom += 1
        variation_lines = []
        variation_lines.append(variation_line_fields)
    else:
        variation_lines.append(variation_line_fields)

    if (len(variation_line) == 0):
        break

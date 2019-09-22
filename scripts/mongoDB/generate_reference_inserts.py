from pymongo import MongoClient

try:
    conn = MongoClient()
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

db = conn.snps
collection = db.reference

for i in range(1):

    inserts = {}
    dir_path = "/home/bruno/Documents/Unifesp/ICBD/IniciacaoCientifica/references/"
    file_name = "Oryza_sativa.IRGSP-1.0.dna_rm.all_chromosomes"
    reference_id = file_name
    associated_paper = "none"
    reference = {"id": file_name,
                  "reference_file_address": dir_path,
                  "associated_paper_address": associated_paper}
    collection.insert_one(reference)

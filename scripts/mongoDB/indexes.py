from pymongo import MongoClient
import pymongo

try:
    conn = MongoClient()
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

db = conn.snps

print(db.individual.drop_indexes())
print(db.chromosome.drop_indexes())
print(db.population.drop_indexes())
print(db.reference.drop_indexes())
print(db.variation.drop_indexes())

print(db.chromosome.create_index([("id" , 1)], name="id_chromosome"))
print(db.chromosome.create_index([("reference_id",pymongo.TEXT)], name="reference_id_chromosome"))

print(db.individual.create_index([("id" , 1)],name="id_individual"))
print(db.individual.create_index([("individual_identification",pymongo.HASHED)], name="individual_identification"))

print(db.population.create_index([("id",1)], name="id_population"))

print(db.reference.create_index([("id",1)],name="id_reference"))

print(db.variation.create_index([("id" , 1)],name="id_variation"))
print(db.variation.create_index([("chrom" , 1)],name="chrom_variation"))
print(db.variation.create_index([("variation_identification", pymongo.HASHED)],name="variation_identification"))
print(db.variation.create_index([("annotations", pymongo.TEXT)],name="annotations"))
print(db.variation.create_index([("pos" , 1)],name="pos_variation"))
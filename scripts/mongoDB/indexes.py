from pymongo import MongoClient
import pymongo

try:
    conn = MongoClient()
    print("Connected successfully!!!")
except:
    print("Could not connect to MongoDB")

db = conn.snps

#db.variation.drop_indexes()

db.chromosome.create_index([("id" , 1)], name="id_chromosome")
db.chromosome.create_index([("reference_id",pymongo.TEXT)], name="reference_id_chromosome")

db.individual.create_index([("id" , 1)],name="id_individual")
db.individual.create_index([("individual_identification",pymongo.TEXT)], name="individual_identification")

db.population.create_index([("id",pymongo.TEXT)], name="id_population")

db.reference.create_index([("id",pymongo.TEXT)],name="id_reference")

db.variation.create_index([("id" , 1)],name="id_variation")
db.variation.create_index([("chrom" , 1)],name="chrom_variation")
db.variation.create_index([("variation_identification",pymongo.TEXT)],name="variation_identification")
db.variation.create_index([("pos" , 1)],name="pos_variation")

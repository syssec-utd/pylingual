import os
from pyspark.sql.functions import explode_outer
from pathling import PathlingContext, to_snomed_coding, translate
HERE = os.path.abspath(os.path.dirname(__file__))
pc = PathlingContext.create()
csv = pc.spark.read.options(header=True).csv(f"file://{os.path.join(HERE, 'data/csv/conditions.csv')}")
result = csv.withColumn('READ_CODES', translate(to_snomed_coding(csv.CODE), 'http://snomed.info/sct/900000000000207008?fhir_cm=900000000000497000').code)
result.select('CODE', 'DESCRIPTION', explode_outer('READ_CODES').alias('READ_CODE')).show()
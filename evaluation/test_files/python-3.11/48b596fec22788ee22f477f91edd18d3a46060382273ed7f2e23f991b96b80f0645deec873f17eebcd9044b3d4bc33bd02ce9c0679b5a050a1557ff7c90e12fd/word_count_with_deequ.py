import sys
from operator import add
from pydeequ import Check, CheckLevel
from pydeequ.analyzers import *
from pydeequ.repository import *
from pydeequ.verification import VerificationSuite
from dbnd import log_dataframe, task
from dbnd_spark.deequ_metrics_repository import DbndMetricsRepository

@task
def word_count(input_path, output_path):
    spark = SparkSession.builder.appName('PythonWordCount').getOrCreate()
    lines = spark.read.text(input_path)
    check = Check(spark, CheckLevel.Warning, 'Review Check')
    check_result = VerificationSuite(spark).onData(lines).addCheck(check.hasSize(lambda x: x >= 3)).run()
    result_key = ResultKey(spark, ResultKey.current_milli_time(), {'name': 'words_df'})
    AnalysisRunner(spark).onData(lines).addAnalyzer(ApproxCountDistinct('value')).useRepository(DbndMetricsRepository(spark)).saveOrAppendResult(result_key).run()
    log_dataframe('lines', lines)
    lines = lines.rdd.map(lambda r: r[0])
    log_dataframe('lines_rdd', lines)
    counts = lines.flatMap(lambda x: x.split(' ')).map(lambda x: (x, 1)).reduceByKey(add)
    output = counts.collect()
    log_dataframe('output', output)
    for word, count in output:
        print('%s: %i' % (word, count))
    spark.sparkContext._gateway.close()
if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print('Usage: wordcount <file> <output>')
        sys.exit(-1)
    word_count(sys.argv[1], sys.argv[2])
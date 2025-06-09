import datetime
import time
from acceldata_sdk.models.job import CreateJob, JobMetadata, Dataset
from acceldata_sdk.models.pipeline import CreatePipeline, PipelineMetadata, PipelineRunResult, PipelineRunStatus
from acceldata_sdk.torch_client import TorchClient

def create_torch_client():
    return TorchClient(url='https://acceldata.sso-demo.acceldata.dev/torch', access_key='1CXZ7RD61X1Z92F', secret_key='CKO7QJ2FZL7J12RIE06KUVRZSA2JOY')

def create_pipeline(torch_client):
    pipeline = CreatePipeline(uid='sso.auth.flow.etl', name='SSO ETL PIPELINE', description='Pipeline to Aggregate the customer orders over 1 year', meta=PipelineMetadata(owner='vaishvik', team='TORCH', codeLocation='www.v.co.in'), context={'tables': 'XYZ'})
    pipeline_response = torch_client.create_pipeline(pipeline=pipeline)
    print('Created the pipeline')
    return pipeline_response

def create_datagen_job(pipeline):
    job = CreateJob(uid='sso.job', name='SSO JOB', description='Generates Pseudo random data for Orders and Customers', inputs=[Dataset('AWS-S3', 'asset1')], outputs=[Dataset('GCS-DS', 'customers')], meta=JobMetadata(owner='vaishvik', team='backend', codeLocation='https://github.com/acme/reporting/reporting.scala'), context={})
    job = pipeline.create_job(job)
    print('Created Job for random data insertion')
    return job

def create_pipeline_run(pipeline):
    return pipeline.create_pipeline_run(context_data={'client_time': str(datetime.datetime.now())})

def start_main_span(pipeline_run):
    span_context = pipeline_run.create_span(uid='customer.orders.monthly.agg', context_data={'client_time': str(datetime.datetime.now())})
    return span_context

def end_main_span(span_context):
    span_context.end()

def end_pipeline_run(pipeline_run, result=PipelineRunResult.SUCCESS, status=PipelineRunStatus.COMPLETED):
    pipeline_run.update_pipeline_run(context_data={'client_time': str(datetime.datetime.now())}, result=result, status=status)
if __name__ == '__main__':
    torch_client = create_torch_client()
    pipeline = create_pipeline(torch_client)
    pipeline_run = create_pipeline_run(pipeline)
    create_datagen_job(pipeline)
    span_context = start_main_span(pipeline_run)
    time.sleep(2)
    end_main_span(span_context)
    end_pipeline_run(pipeline_run)
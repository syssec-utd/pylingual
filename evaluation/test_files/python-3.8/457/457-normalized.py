def put_records(self, records):
    """
        Write batch records to Kinesis Firehose
        """
    firehose_conn = self.get_conn()
    response = firehose_conn.put_record_batch(DeliveryStreamName=self.delivery_stream, Records=records)
    return response
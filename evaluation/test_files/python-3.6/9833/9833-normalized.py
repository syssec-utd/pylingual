def summaries(self):
    """Yield (name, (value, value, ...)) for each summary in the file."""
    length = self.summary_length
    step = self.summary_step
    for (record_number, n_summaries, summary_data) in self.summary_records():
        name_data = self.read_record(record_number + 1)
        for i in range(0, int(n_summaries) * step, step):
            j = self.summary_control_struct.size + i
            name = name_data[i:i + step].strip()
            data = summary_data[j:j + length]
            values = self.summary_struct.unpack(data)
            yield (name, values)
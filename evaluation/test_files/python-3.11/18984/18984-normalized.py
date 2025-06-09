def run(self, i_str, start_count=0, start_chunk_time=None):
    """Run the pipeline.

        This runs all of the steps described in the pipeline constructor,
        reading from some input and writing to some output.

        :param str i_str: name of the input file, or other reader-specific
          description of where to get input
        :param int start_count: index of the first stream item
        :param int start_chunk_time: timestamp for the first stream item

        """
    try:
        if not os.path.exists(self.tmp_dir_path):
            os.makedirs(self.tmp_dir_path)
        if start_chunk_time is None:
            start_chunk_time = time.time()
        i_chunk = self.reader(i_str)
        t_path = None
        len_clean_visible = 0
        sources = set()
        next_idx = 0
        input_item_count = 0
        for si in i_chunk:
            next_idx += 1
            if gevent:
                gevent.sleep(0)
            if next_idx <= start_count:
                continue
            if next_idx % self.rate_log_interval == 0:
                elapsed = time.time() - start_chunk_time
                if elapsed > 0:
                    rate = float(next_idx) / elapsed
                    logger.info('%d in %.1f --> %.1f per sec on (pre-partial_commit) %s', next_idx - start_count, elapsed, rate, i_str)
            if not self.t_chunk:
                t_path = os.path.join(self.tmp_dir_path, 't_chunk-%s' % uuid.uuid4().hex)
                self.t_chunk = streamcorpus.Chunk(path=t_path, mode='wb')
                assert self.t_chunk.message == streamcorpus.StreamItem_v0_3_0, self.t_chunk.message
            si = self._run_incremental_transforms(si, self.incremental_transforms)
            if si:
                sources.add(si.source)
                if self.assert_single_source and len(sources) != 1:
                    raise InvalidStreamItem('stream item %r had source %r, not %r (set assert_single_source: false to suppress)' % (si.stream_id, si.source, sources))
            if si and si.body and si.body.clean_visible:
                len_clean_visible += len(si.body.clean_visible)
            if self.output_chunk_max_count is not None and len(self.t_chunk) == self.output_chunk_max_count:
                logger.info('reached output_chunk_max_count (%d) at: %d', len(self.t_chunk), next_idx)
                self._process_output_chunk(start_count, next_idx, sources, i_str, t_path)
                start_count = next_idx
            elif self.output_max_clean_visible_bytes is not None and len_clean_visible >= self.output_chunk_max_clean_visible_bytes:
                logger.info('reached output_chunk_max_clean_visible_bytes (%d) at: %d', self.output_chunk_max_clean_visible_bytes, len_clean_visible)
                len_clean_visible = 0
                self._process_output_chunk(start_count, next_idx, sources, i_str, t_path)
                start_count = next_idx
            input_item_count += 1
            if self.input_item_limit is not None and input_item_count > self.input_item_limit:
                break
        if self.t_chunk is not None:
            self._process_output_chunk(start_count, next_idx, sources, i_str, t_path)
        return next_idx
    finally:
        if self.t_chunk is not None:
            self.t_chunk.close()
        for transform in self.batch_transforms:
            transform.shutdown()
        if self.cleanup_tmp_files:
            rmtree(self.tmp_dir_path)
"""
    Stable Engine Pseudo-algorithm-
        1. Downloads about 1000 documents.
        2. Processes it in much smaller chunks.
        3. Upserts all 1000 documents.
        4. Repeat until dataset has finished looping

    We download a large chunk and upsert large chunks to avoid hammering
    our servers.

"""
import logging
import traceback
from workflows_core.engine.abstract_engine import AbstractEngine
from workflows_core.utils.document_list import DocumentList
from tqdm.auto import tqdm
logger = logging.getLogger(__file__)

class StableEngine(AbstractEngine):

    def __init__(self, *args, transform_chunksize: int=20, **kwargs):
        """
        Parameters
        -----------

        pull_chunksize
            the number of documents that are downloaded

        """
        super().__init__(*args, **kwargs)
        self._transform_chunksize = min(self.pull_chunksize, transform_chunksize)
        self._show_progress_bar = kwargs.pop('show_progress_bar', True)

    def chunk_documents(self, documents: DocumentList):
        num_chunks = len(documents) // self._transform_chunksize + 1
        for i in range(num_chunks):
            start = i * self._transform_chunksize
            end = (i + 1) * self._transform_chunksize
            chunk = documents[start:end]
            if len(chunk) > 0:
                yield chunk

    def _filter_for_non_empty_list(self, docs: DocumentList):
        return DocumentList([d for d in docs if len(d) > 1])

    def apply(self) -> None:
        """
        Returns the ratio of successful chunks / total chunks needed to iterate over the dataset
        """
        iterator = self.iterate()
        successful_chunks = 0
        error_logs = []
        for (chunk_counter, large_chunk) in enumerate(tqdm(iterator, desc=repr(self.operator), disable=not self._show_progress_bar, total=self.num_chunks)):
            self.update_progress(0)
            chunk_to_update = []
            for chunk in self.chunk_documents(large_chunk):
                chunk = self._filter_for_non_empty_list(chunk)
                if len(chunk) == 0:
                    new_batch = []
                try:
                    new_batch = self.operator(chunk)
                except Exception as e:
                    chunk_error_log = {'exception': str(e), 'traceback': traceback.format_exc(), 'chunk_ids': [document['_id'] for document in chunk]}
                    error_logs.append(chunk_error_log)
                    logger.error(chunk)
                    logger.error(traceback.format_exc())
                else:
                    successful_chunks += 1
                    chunk_to_update.extend(new_batch)
            if chunk_counter < self.MAX_SCHEMA_UPDATE_LIMITER:
                ingest_in_background = False
            else:
                ingest_in_background = True
            result = self.update_chunk(chunk_to_update, update_schema=chunk_counter < self.MAX_SCHEMA_UPDATE_LIMITER, ingest_in_background=ingest_in_background)
            logger.debug(result)
            if self.job_id:
                self.update_progress(chunk_counter + 1)
        self._error_logs = error_logs
        if self.num_chunks > 0:
            self._success_ratio = successful_chunks / self.num_chunks
            logger.debug({'success_ratio': self._success_ratio})
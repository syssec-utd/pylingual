def _finish_event(hits, clusters, start_event_hit_index, stop_event_hit_index, start_event_cluster_index, stop_event_cluster_index):
    """ Set hit and cluster information of the event (e.g. number of cluster in the event (n_cluster), ...).
    """
    for hit_index in range(start_event_hit_index, stop_event_hit_index):
        hits[hit_index]['n_cluster'] = stop_event_cluster_index - start_event_cluster_index
    for cluster_index in range(start_event_cluster_index, stop_event_cluster_index):
        clusters[cluster_index]['event_number'] = hits[start_event_hit_index]['event_number']
    _end_of_event_function(hits=hits, clusters=clusters, start_event_hit_index=start_event_hit_index, stop_event_hit_index=stop_event_hit_index, start_event_cluster_index=start_event_cluster_index, stop_event_cluster_index=stop_event_cluster_index)
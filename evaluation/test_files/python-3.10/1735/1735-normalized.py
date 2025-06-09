def dump_model(path, graph=None, sess=None, ckpt_file=None, bigdl_type='float'):
    """
    Dump a tensorflow model to files. The graph will be dumped to path/model.pb, and the checkpoint will
    be dumped to path/model.bin
    
    :param path: dump folder path
    :param sess: if user pass in session, we assume that the variable of the graph in the session
    has been inited
    :param graph: tensorflow graph. Default use the default graph of the session
    :param bigdl_type: model variable numeric type
    :return: nothing
    """
    if not os.path.isdir(path):
        raise ValueError('Folder ' + path + ' does not exist')
    temp = None
    if ckpt_file is None:
        if sess is None:
            sess = tf.Session()
            init = tf.global_variables_initializer()
            sess.run(init)
            temp = tempfile.mkdtemp()
            ckpt_file = temp
        saver = tf.train.Saver()
        saver.save(sess, ckpt_file)
    tensors = export_checkpoint(ckpt_file)
    save_variable_bigdl(tensors, path + '/model.bin', bigdl_type)
    graph = sess.graph if graph is None else graph
    with gfile.GFile(path + '/model.pb', 'wb') as f:
        f.write(graph.as_graph_def().SerializeToString())
    if temp is not None:
        try:
            shutil.rmtree(temp)
        except OSError as e:
            if e.errno != errno.ENOENT:
                raise
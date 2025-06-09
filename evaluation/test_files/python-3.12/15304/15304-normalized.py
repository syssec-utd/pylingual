def save_weights(sess, output_path, conv_var_names=None, conv_transpose_var_names=None):
    """Save the weights of the trainable variables, each one in a different file in output_path."""
    if not conv_var_names:
        conv_var_names = []
    if not conv_transpose_var_names:
        conv_transpose_var_names = []
    for var in tf.trainable_variables():
        filename = '{}-{}'.format(output_path, var.name.replace(':', '-').replace('/', '-'))
        if var.name in conv_var_names:
            var = tf.transpose(var, perm=[3, 0, 1, 2])
        elif var.name in conv_transpose_var_names:
            var = tf.transpose(var, perm=[3, 1, 0, 2])
        value = sess.run(var)
        with open(filename, 'w') as file_:
            value.tofile(file_)
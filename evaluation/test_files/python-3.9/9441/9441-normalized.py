def list_to_tf_input(data, response_index, num_outcomes):
    """
  Separates the outcome feature from the data.
  """
    matrix = np.matrix([row[:response_index] + row[response_index + 1:] for row in data])
    outcomes = np.asarray([row[response_index] for row in data], dtype=np.uint8)
    return (matrix, outcomes)
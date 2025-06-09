def load_audit_confusion_matrices(filename):
    """
  Loads a confusion matrix in a two-level dictionary format.

  For example, the confusion matrix of a 75%-accurate model
  that predicted 15 values (and mis-classified 5) may look like:
  {"A": {"A":10, "B": 5}, "B": {"B":5}}

  Note that raw boolean values are translated into strings, such that
  a value that was the boolean True will be returned as the string "True".
  """
    with open(filename) as audit_file:
        audit_file.next()
        confusion_matrices = []
        for line in audit_file:
            separator = ':'
            separator_index = line.index(separator)
            comma_index = line.index(',')
            repair_level = float(line[separator_index + 2:comma_index])
            raw_confusion_matrix = line[comma_index + 2:-2]
            confusion_matrix = json.loads(raw_confusion_matrix.replace("'", '"'))
            confusion_matrices.append((repair_level, confusion_matrix))
    confusion_matrices.sort(key=lambda pair: pair[0])
    return confusion_matrices
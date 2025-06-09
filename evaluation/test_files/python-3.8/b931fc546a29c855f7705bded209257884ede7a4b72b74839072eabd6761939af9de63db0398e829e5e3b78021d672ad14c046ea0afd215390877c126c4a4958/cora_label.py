LABEL_NAMES = ['author', 'booktitle', 'date', 'editor', 'institution', 'journal', 'location', 'note', 'pages', 'publisher', 'tech', 'title', 'volume']
num_labels = len(LABEL_NAMES)
id2label = {str(i): label for (i, label) in enumerate(LABEL_NAMES)}
label2id = {v: k for (k, v) in id2label.items()}
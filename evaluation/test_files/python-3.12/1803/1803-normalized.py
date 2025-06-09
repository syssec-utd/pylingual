def _build_basic_network(self, word_outputs):
    """
        Creates the basic network architecture,
        transforming word embeddings to intermediate outputs
        """
    if self.word_dropout > 0.0:
        lstm_outputs = kl.Dropout(self.word_dropout)(word_outputs)
    else:
        lstm_outputs = word_outputs
    for j in range(self.word_lstm_layers - 1):
        lstm_outputs = kl.Bidirectional(kl.LSTM(self.word_lstm_units[j], return_sequences=True, dropout=self.lstm_dropout))(lstm_outputs)
    lstm_outputs = kl.Bidirectional(kl.LSTM(self.word_lstm_units[-1], return_sequences=True, dropout=self.lstm_dropout))(lstm_outputs)
    pre_outputs = kl.TimeDistributed(kl.Dense(self.tags_number_, activation='softmax', activity_regularizer=self.regularizer), name='p')(lstm_outputs)
    return (pre_outputs, lstm_outputs)
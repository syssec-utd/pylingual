import torch
from bpe import BPE_token
from pathlib import Path
import os
paths = [str(x) for x in Path('./text/').glob('**/*.txt')]
tokenizer = BPE_token()
tokenizer.bpe_train(paths)
save_path = 'tokenized_data'
tokenizer.save_tokenizer(save_path)
from transformers import GPT2Config, GPT2LMHeadModel, GPT2Tokenizer
tokenizer = GPT2Tokenizer.from_pretrained(save_path)
tokenizer.add_special_tokens({'eos_token': '</s>', 'bos_token': '<s>', 'unk_token': '<unk>', 'pad_token': '<pad>', 'mask_token': '<mask>'})
config = GPT2Config(vocab_size=tokenizer.vocab_size, bos_token_id=tokenizer.bos_token_id, eos_token_id=tokenizer.eos_token_id)
model = GPT2LMHeadModel(config)
single_string = ''
for filename in paths:
    with open(filename, 'r', encoding='utf-8') as f:
        x = f.read()
    single_string += x + tokenizer.eos_token
string_tokenized = tokenizer.encode(single_string)
examples = []
block_size = 100
BATCH_SIZE = 12
BUFFER_SIZE = 1000
for i in range(0, len(string_tokenized) - block_size + 1, block_size):
    examples.append(string_tokenized[i:i + block_size])
inputs, labels = ([], [])
for ex in examples:
    inputs.append(ex[:-1])
    labels.append(ex[1:])
dataset = torch.util.Dataset.from_tensor_slices((inputs, labels))
dataset = dataset.shuffle(BUFFER_SIZE).batch(BATCH_SIZE, drop_remainder=True)
optimizer = torch.optim.AdamW(lr=3e-05, eps=1e-08)
loss = torch.nn.CrossEntropyLoss()
model.compile(optimizer=optimizer)
num_epoch = 10
history = model.fit(dataset, epochs=num_epoch)
text = '오늘 비가 온다.'
input_ids = tokenizer.encode(text, return_tensors='tf')
beam_output = model.generate(input_ids, max_length=50, num_beams=5, temperature=0.7, no_repeat_ngram_size=2, num_return_sequences=5)
from transformers import WEIGHTS_NAME, CONFIG_NAME
import os
output_dir = './model_bn_custom/'
if not os.path.exists(output_dir):
    os.mkdir(output_dir)
model_to_save = model.module if hasattr(model, 'module') else model
output_model_file = os.path.join(output_dir, WEIGHTS_NAME)
output_config_file = os.path.join(output_dir, CONFIG_NAME)
model.save_pretrained(output_dir)
model_to_save.config.to_json_file(output_config_file)
tokenizer.save_pretrained(output_dir)
import json
from pathlib import Path
from soundfile import write

from create_music.linear_model import helper_functions
import torch
import uuid


device = 'cpu'
sample_length = 32768
model_name = 'music_creation'
metadata_file = 'lofi'
epochs = 40
save_every = 5
sample_rate = 16000


with open(f'models/{metadata_file}/metadata{model_name}.json', 'r') as outfile:
    metadata = json.load(outfile)

for key, value in metadata.items():
    if 'path' in value:
        model_path = value['path']
        starting_iteration = int(key)

model = torch.load(model_path)
model.eval()


for x in range(list(model.parameters())[0].shape[1]):
    switches = [(x, 1)]

    output = helper_functions.create_output(model, switches)

    output_path = Path('create_music/linear_model') / 'outputs' / metadata_file / f'{x}_{uuid.uuid4().__str__()}.wav'

    output_path.parent.mkdir(exist_ok=True, parents=True)

    write(output_path, output, samplerate=sample_rate)

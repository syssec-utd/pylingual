import numpy as np
from PIL import Image
from sdkit import Context

def apply(context: Context, image, scale=4, **kwargs):
    image = image.convert('RGB')
    image = np.array(image, dtype=np.uint8)[..., ::-1]
    (output, _) = context.models['realesrgan'].enhance(image, outscale=scale)
    output = output[:, :, ::-1]
    output = Image.fromarray(output)
    return output
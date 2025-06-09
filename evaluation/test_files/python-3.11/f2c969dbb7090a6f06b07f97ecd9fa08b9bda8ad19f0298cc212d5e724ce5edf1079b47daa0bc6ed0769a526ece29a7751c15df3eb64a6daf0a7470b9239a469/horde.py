import contextlib
from loguru import logger
from PIL import Image, UnidentifiedImageError
from hordelib.comfy_horde import Comfy_Horde
from hordelib.shared_model_manager import SharedModelManager

class HordeLib:
    SAMPLERS_MAP = {'k_euler': 'euler', 'k_euler_a': 'euler_ancestral', 'k_heun': 'heun', 'k_dpm_2': 'dpm_2', 'k_dpm_2_a': 'dpm_2_ancestral', 'k_lms': 'lms', 'k_dpm_fast': 'dpm_fast', 'k_dpm_adaptive': 'dpm_adaptive', 'k_dpmpp_2s_a': 'dpmpp_2s_ancestral', 'k_dpmpp_sde': 'dpmpp_sde', 'k_dpmpp_2m': 'dpmpp_2m', 'ddim': 'ddim', 'uni_pc': 'uni_pc', 'uni_pc_bh2': 'uni_pc_bh2', 'plms': 'euler'}
    BASIC_INFERENCE_PARAMS = {'sampler_name': 'sampler.sampler_name', 'cfg_scale': 'sampler.cfg', 'denoising_strength': 'sampler.denoise', 'seed': 'sampler.seed', 'height': 'empty_latent_image.height', 'width': 'empty_latent_image.width', 'tiling': None, 'clip_skip': 'clip_skip.stop_at_clip_layer', 'image_is_control': None, 'return_control_map': 'return_control_map', 'ddim_steps': 'sampler.steps', 'n_iter': 'empty_latent_image.batch_size', 'model': 'model_loader.model_name', 'source_image': 'image_loader.image', 'source_mask': None, 'source_processing': 'source_processing'}
    CONTROLNET_IMAGE_PREPROCESSOR_MAP = {'canny': 'canny', 'hed': 'hed', 'depth': 'depth', 'normal': 'normal', 'openpose': 'openpose', 'seg': 'seg', 'scribble': 'scribble', 'fakescribbles': 'fakescribble', 'hough': 'mlsd'}
    SOURCE_IMAGE_PROCESSING_OPTIONS = ['img2img', 'inpainting', 'outpainting']

    def _parameter_remap(self, payload: dict[str, str | None]) -> dict[str, str | None]:
        params = {}
        for key, value in payload.items():
            newkey = HordeLib.BASIC_INFERENCE_PARAMS.get(key, None)
            if newkey:
                params[newkey] = value
        if 'model_loader.model_manager' not in params:
            params['model_loader.model_manager'] = SharedModelManager
        return params

    def _parameter_remap_basic_inference(self, payload: dict[str, str | None]) -> dict[str, str | None]:
        params = self._parameter_remap(payload)
        with contextlib.suppress(ValueError):
            params['sampler.seed'] = int(params['sampler.seed'])
        if payload.get('karras', False):
            params['sampler.scheduler'] = 'karras'
        else:
            params['sampler.scheduler'] = 'normal'
        promptsCombined = payload.get('prompt', '')
        if promptsCombined is None:
            raise TypeError('`None` value encountered!')
        promptsSplit = [x.strip() for x in promptsCombined.split('###')][:2]
        if len(promptsSplit) == 1:
            params['prompt.text'] = promptsSplit[0]
            params['negative_prompt.text'] = ''
        elif len(promptsSplit) == 2:
            params['prompt.text'] = promptsSplit[0]
            params['negative_prompt.text'] = promptsSplit[1]
        sampler = HordeLib.SAMPLERS_MAP.get(params['sampler.sampler_name'], 'euler')
        params['sampler.sampler_name'] = sampler
        clip_skip_key = 'clip_skip.stop_at_clip_layer'
        if params.get(clip_skip_key, 0) > 0:
            params[clip_skip_key] = -params[clip_skip_key]
        if payload.get('hires_fix'):
            params['upscale_sampler.seed'] = params['sampler.seed']
            params['upscale_sampler.scheduler'] = params['sampler.scheduler']
            params['upscale_sampler.cfg'] = params['sampler.cfg']
            params['upscale_sampler.steps'] = params['sampler.steps']
            params['upscale_sampler.sampler_name'] = params['sampler.sampler_name']
            params['upscale_sampler.denoise'] = 0.6
            width = params.get('empty_latent_image.width', 0)
            height = params.get('empty_latent_image.height', 0)
            if width > 512 and height > 512:
                final_width = width
                final_height = height
                params['latent_upscale.width'] = final_width
                params['latent_upscale.height'] = final_height
                first_pass_ratio = min(final_height / 512, final_width / 512)
                width = int(final_width / first_pass_ratio) // 64 * 64
                height = int(final_height / first_pass_ratio) // 64 * 64
                params['empty_latent_image.width'] = width
                params['empty_latent_image.height'] = height
                params['hires_fix'] = True
        if (cnet := payload.get('control_type')):
            pre_processor = HordeLib.CONTROLNET_IMAGE_PREPROCESSOR_MAP.get(cnet)
            params['controlnet_model_loader.control_net_name'] = cnet
            params['control_type'] = pre_processor
            if 'source_processing' in params:
                del params['source_processing']
        return params

    def _validate_BASIC_INFERENCE_PARAMS(self, payload):
        if 'hires_fix' in payload and (payload['width'] <= 512 or payload['height'] <= 512):
            payload['hires_fix'] = False
        img_proc = payload.get('source_processing')
        if img_proc and img_proc not in HordeLib.SOURCE_IMAGE_PROCESSING_OPTIONS:
            del payload['source_processing']
        if payload.get('source_image'):
            if not img_proc or img_proc not in HordeLib.SOURCE_IMAGE_PROCESSING_OPTIONS:
                del payload['source_image']
        if 'hires_fix' in payload and (img_proc == 'inpainting' or img_proc == 'outpainting'):
            payload['hires_fix'] = False

    def _get_appropriate_pipeline(self, params):
        pipeline = None
        if 'hires_fix' in params:
            del params['hires_fix']
            pipeline = 'stable_diffusion_hires_fix'
        else:
            pipeline = 'stable_diffusion'
        source_proc = params.get('source_processing')
        if source_proc:
            del params['source_processing']
        if source_proc == 'img2img':
            if params.get('source_mask'):
                pipeline = 'stable_diffusion_paint'
            elif len(params.get('image_loader.image').split()) == 4:
                pipeline = 'stable_diffusion_paint'
        elif source_proc == 'inpainting':
            pipeline = 'stable_diffusion_paint'
        elif source_proc == 'outpainting':
            pipeline = 'stable_diffusion_paint'
        if params.get('control_type'):
            if params.get('return_control_map', False):
                pipeline = 'controlnet_annotator'
            else:
                pipeline = 'controlnet'
        return pipeline

    def _resize_sources_to_request(self, payload):
        """Ensures the source_image and source_mask are at the size requested by the client"""
        source_image = payload.get('source_image')
        if not source_image:
            return
        try:
            if source_image.size != (payload['width'], payload['height']) and (not payload.get('hires_fix')):
                payload['source_image'] = source_image.resize((payload['width'], payload['height']))
        except (UnidentifiedImageError, AttributeError):
            logger.warning('Source image could not be parsed. Falling back to text2img')
            del payload['source_image']
            del payload['source_processing']
            return
        source_mask = payload.get('source_mask')
        if not source_mask:
            return
        try:
            if source_mask.size != (payload['width'], payload['height']):
                payload['source_mask'] = source_mask.resize((payload['width'], payload['height']))
        except (UnidentifiedImageError, AttributeError):
            logger.warning('Source mask could not be parsed. Falling back to img2img without mask')
            del payload['source_mask']

    def basic_inference(self, payload: dict[str, str | None]) -> Image.Image | None:
        generator = Comfy_Horde()
        self._validate_BASIC_INFERENCE_PARAMS(payload)
        self._resize_sources_to_request(payload)
        params = self._parameter_remap_basic_inference(payload)
        pipeline = self._get_appropriate_pipeline(params)
        images = generator.run_image_pipeline(pipeline, params)
        if images is None:
            return None
        return Image.open(images[0]['imagedata'])

    def image_upscale(self, payload: dict[str, str | None]) -> Image.Image | None:
        generator = Comfy_Horde()
        params = self._parameter_remap(payload)
        pipeline = 'image_upscale'
        images = generator.run_image_pipeline(pipeline, params)
        if images is None:
            return None
        return Image.open(images[0]['imagedata'])

    def image_facefix(self, payload: dict[str, str | None]) -> Image.Image | None:
        generator = Comfy_Horde()
        params = self._parameter_remap(payload)
        pipeline = 'image_facefix'
        images = generator.run_image_pipeline(pipeline, params)
        if images is None:
            return None
        return Image.open(images[0]['imagedata'])
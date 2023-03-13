import os
import time

import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from itertools import product

from utils.file_manager import FileManager
from utils.restart import RestartStableDiffusion
import utils.logger as logger

DEFAULT = ['default']
MODES = {
    'txt2img': 'txt2img',
    'img2img': 'img2img',
}


class StableDiffusionBot:

    def __init__(self, pos_prompt, neg_prompt, steps_list=[26], image_num=4, samplers=DEFAULT, seeds=DEFAULT, cfg_scales=DEFAULT, size=[480, 480]):
        chrome_options = Options()
        chrome_options.add_argument("--start-minimized")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get('http://127.0.0.1:7860')
        self.shadow_root = self.get_shadow_root()
        self.pos_prompt = pos_prompt
        self.neg_prompt = neg_prompt
        self.has_error = False
        self.image_num = image_num
        self.steps_list = steps_list
        self.samplers = samplers
        self.seeds = seeds
        self.cfg_scales = cfg_scales
        self.size = size

    def create(self):

        self.verify_samplers()

        self.write_prompts()
        self.change_size(self.size)

        images_total = self.image_num * \
            len(self.samplers) * len(self.seeds) * \
            len(self.cfg_scales) * len(self.steps_list)
        logger.info(f'Total Images: {images_total}')

        count = 1
        for _, params in enumerate(product(self.samplers, self.seeds, self.cfg_scales, self.steps_list), 1):
            for _ in range(self.image_num):
                self.create_image_process(*params, images_total, count)
                count += 1

        time.sleep(1)
        self.move_images()

    def verify_samplers(self):
        if self.samplers != DEFAULT:
            sampler_div = self.shadow_root.find_element(
                By.CSS_SELECTOR, '#txt2img_sampling')
            sampler_options = sampler_div.find_element(
                By.TAG_NAME, 'select').find_elements(By.TAG_NAME, 'option')
            for sampler in self.samplers:
                if not any(sampler in option.text for option in sampler_options):
                    options_value = [option.text for option in sampler_options]
                    raise ValueError(
                        f'{sampler} is not a valid sampler, Valid Samplers: {options_value}')

    def change_size(self, size):
        width_div = self.shadow_root.find_element(
            By.CSS_SELECTOR, '#txt2img_width')
        width_input = width_div.find_element(By.TAG_NAME, 'input')
        width_input.clear()
        width_input.send_keys(size[0])
        height_div = self.shadow_root.find_element(
            By.CSS_SELECTOR, '#txt2img_height')
        height_input = height_div.find_element(By.TAG_NAME, 'input')
        height_input.clear()
        height_input.send_keys(size[1])

    def create_image_process(self, sampler, seed, cfg_scale, steps, images_total, count):
        self.select_params(sampler, seed, cfg_scale, steps)
        self.generate_image()
        self.wait_to_generate()
        if not self.check_error():
            self.save_image(sampler, seed, cfg_scale, steps)
            logger.success(f'Generated {count}/{images_total}')
        else:
            restart_sd = RestartStableDiffusion()
            restart_sd.restart()
            time.sleep(15)

    def select_params(self, sampler, seed, cfg_scale, steps):
        self.change_steps(steps)
        if sampler != DEFAULT[0]:
            self.select_sampler(sampler)
        if seed != DEFAULT[0]:
            self.select_seed(seed)
        if cfg_scale != DEFAULT[0]:
            self.select_cfg_scale(cfg_scale)

    def select_sampler(self, sampler):
        sampler_div = self.shadow_root.find_element(
            By.CSS_SELECTOR, '#txt2img_sampling')
        sampler_select = sampler_div.find_element(By.TAG_NAME, 'select')
        sampler_select.send_keys(sampler)

    def select_seed(self, seed):
        seed_div = self.shadow_root.find_element(
            By.CSS_SELECTOR, '#txt2img_seed')
        seed_input = seed_div.find_element(By.TAG_NAME, 'input')
        seed_input.clear()
        seed_input.send_keys(seed)

    def select_cfg_scale(self, cfg_scale):
        cfg_scale_div = self.shadow_root.find_element(
            By.CSS_SELECTOR, '#txt2img_cfg_scale')
        cfg_scale_input = cfg_scale_div.find_element(By.TAG_NAME, 'input')
        cfg_scale_input.clear()
        cfg_scale_input.send_keys(cfg_scale)

    def get_shadow_root(self):
        gradio_app = self.driver.find_element(By.TAG_NAME, 'gradio-app')
        return self.driver.execute_script(f'return arguments[0].shadowRoot', gradio_app)

    def write_prompts(self):
        time.sleep(2)
        self.write_prompt('#txt2img_prompt', self.pos_prompt)
        self.write_prompt('#txt2img_neg_prompt', self.neg_prompt)

    def write_prompt(self, element_id, prompt_text):
        prompt = self.shadow_root.find_element(
            By.CSS_SELECTOR, element_id)

        prompt_input = prompt.find_element(By.TAG_NAME, 'textarea')

        prompt_input.send_keys(prompt_text)

    def change_steps(self, steps):
        steps_div = self.shadow_root.find_element(
            By.CSS_SELECTOR, '#txt2img_steps')
        steps_input = steps_div.find_element(By.TAG_NAME, 'input')
        steps_input.clear()
        steps_input.send_keys(steps)

    def generate_image(self):
        generate_btn = self.shadow_root.find_element(
            By.CSS_SELECTOR, '#txt2img_generate')
        generate_btn.click()

    def wait_to_generate(self):
        time.sleep(1)
        while True:
            try:

                btn = self.shadow_root.find_element(
                    By.CSS_SELECTOR, '#txt2img_interrupt')
                style = btn.get_attribute('style')
                if 'display: none' in style:
                    break

            except selenium.common.exceptions.NoSuchElementException:
                break

    def save_image(self, sampler, seed, cfg_scale, steps):
        save_btn = self.shadow_root.find_element(
            By.CSS_SELECTOR, '#save_txt2img')
        save_btn.click()
        time.sleep(.5)
        download_section = self.shadow_root.find_element(
            By.CSS_SELECTOR, '#download_files_txt2img')
        download_btn = download_section.find_element(By.TAG_NAME, 'a')
        download_btn.click()

        image_name = download_btn.get_attribute('download')

        if sampler != DEFAULT or seed != DEFAULT or cfg_scale != DEFAULT:
            self.rename_file(image_name, sampler, seed, cfg_scale, steps)

    def rename_file(self, image_name, sampler, seed, cfg_scale, steps):
        new_name = image_name.split('.')[0]
        extension = image_name.split('.')[-1]
        if len(self.samplers) > 1:
            new_name += f'_{sampler}'
        if len(self.seeds) > 1:
            new_name += f'_{seed}'
        if len(self.cfg_scales) > 1:
            new_name += f'_{cfg_scale}'
        if (len(self.steps_list) > 1):
            new_name += f'_{steps}steps'

        file_path = os.path.expanduser("~/Downloads")
        file_manager = FileManager(destination_folder=file_path)
        time.sleep(1)
        file_manager.rename_file(image_name, f"{new_name}.{extension}")

    def check_error(self):
        try:
            text_result = self.shadow_root.find_element(
                By.ID, 'html_log_txt2img')
            div_error = text_result.find_element(By.CSS_SELECTOR, 'div.error')
            text_error = "RuntimeError: Could not allocate tensor with"
            if text_error in div_error.text:
                logger.error("Not enough memory, restarting SD...")
                return True
            else:
                return False
        except selenium.common.exceptions.NoSuchElementException:
            return False

    def move_images(self):
        prompt_first_word = self.pos_prompt.split(" ")[0]
        timestamp = time.strftime("%Y%m%d%H%M%S")
        path_move = os.path.expanduser(
            f"~/Downloads/StableDiffusion/{prompt_first_word}_{timestamp}")

        file_mover = FileManager(path_move)
        file_mover.move_files()

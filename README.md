# Stable Diffusion Bot
This script automates the creation of Stable Diffusion images using the StableDiffusionBot class from the managers.stable_diff_bot module.

> **Note:** This script has only been tested on Windows so far. We plan to test it on Linux in the near future. If you encounter any issues while running the script on Linux, please let us know by opening an issue in this repository.

## Requirements
Before running the script, ensure that you have the required dependencies installed. To install them, run the following command in your terminal:

```python
pip install -r requirements.txt
```

This command will install all the necessary modules listed in the requirements.txt file.

## Usage
To use this script, follow these steps:

> Note: Before running the `restart.py` script, you need to configure the path of the `stable_diffusion` directory inside the script. Open the `restart.py` file and locate the following line of code: 
> ```python
> stable_diffusion_dir = '/path/to/stable_diffusion'
> ```
> Replace `/path/to/stable_diffusion` with the actual path to the `stable_diffusion` directory on your system. Once you have updated the path, save the file and run the script as usual.

1. Set the desired prompt strings for positive and negative prompts in the `autoCreateImg.py` script. For example:
```python
positive_prompt = "House in the middle of the sky"
negative_prompt = "malformed, watermark, poorly drawn"
```

2. Configure the `StableDiffusionBot` instance in the `autoCreateImg.py` script by setting the `steps_list`, `image_num`, `samplers`, `size`, and `cfg_scales` parameters.
```python
bot = StableDiffusionBot(
    positive_prompt, negative_prompt, steps_list=[22, 26], image_num=2, samplers=['DPM++ 2M Karras', 'Euler a'], size=[512, 600], cfg_scales=[7.0])
```

for each element in a list, more images will be created.  
In the above example 8 images should be created 
2 x 2 x 2 = 8
(steps_list, image_num, samplers)

3. Run the command to run the application
```python
python autoCreateImg.py
```

This will execute the script and create the desired Stable Diffusion images.

That's it! You should now be able to use the StableDiffusionBot script to automate the creation of Stable Diffusion images.
The images will be saved in the downloads, inside a random folder
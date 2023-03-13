from managers.stable_diff_bot import StableDiffusionBot


if (__name__ == '__main__'):
    positive_prompt = 'Uraraka, from my hero academia, school, indoors, (soothing tones:1.25), (hdr:1.25), (artstation:1.2), dramatic, (intricate details:1.14), (hyperrealistic 3d render:1.16), (filmic:0.55), (rutkowski:1.1), (faded:1.3)'
    negative_prompt = '(deformed, distorted, disfigured:1.3), poorly drawn, bad anatomy, wrong anatomy, extra limb, missing limb, floating limbs, (mutated hands and fingers:1.4), disconnected limbs, mutation, mutated, ugly, disgusting, blurry, amputation'

    bot = StableDiffusionBot(
        positive_prompt, negative_prompt, steps_list=[22], image_num=2, samplers=['DPM++ 2M Karras', 'Euler a'], size=[512, 600], cfg_scales=[7.0])
    bot.create()


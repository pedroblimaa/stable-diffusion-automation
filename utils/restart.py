import os
import subprocess
import time

STABLE_DIFFUSION_DIR = 'C:/Users/drope/OneDrive/Área de Trabalho/Documents/Dev/Stable Diffusion/stable-diffusion-webui-directml'


class RestartStableDiffusion:

    def kill_terminal(self):
        os.system('taskkill /f /im cmd.exe')
        time.sleep(1)

    def start_stable_diffusion(self):
        os.chdir(STABLE_DIFFUSION_DIR)
        subprocess.Popen(['start', 'cmd', '/k', 'webui-user.bat'], shell=True)

    def restart(self):
        self.kill_terminal()
        self.start_stable_diffusion()


if __name__ == '__main__':
    restart_sd = RestartStableDiffusion()
    restart_sd.restart()

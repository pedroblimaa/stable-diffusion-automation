RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
ENDC = '\033[0m'


def error(error):
    print(f'{RED}ERROR: {error}{ENDC}')
    return True

def info(info):
    print(f'{BLUE}INFO: {info}{ENDC}')
    return True

def warning(warning):
    print(f'{YELLOW}WARNING: {warning}{ENDC}')
    return True

def success(success):
    print(f'{GREEN}SUCCESS: {success}{ENDC}')
    return True
from generators.mock_generator import MockGenerator
from generators.stable_diffusion import StableDiffusion

def create_generator(generator, ip, port):
    if generator == "stable_diffusion":
        return StableDiffusion(ip, port)
    elif generator == "mock_generator":
        return MockGenerator()
    else:
        raise Exception("Unsupported generator type")
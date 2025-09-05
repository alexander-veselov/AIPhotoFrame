from providers.concurrent_image_provider import ConcurrentImageProvider

class GeneratedImageProvider(ConcurrentImageProvider):
    def __init__(self, width, height, rotate, flip, image_generator, prompt_generator, prompt, negative_prompt, improve_prompt):
        super().__init__(width, height, rotate, flip)
        self.image_generator = image_generator
        self.prompt_generator = prompt_generator
        self.prompt = prompt
        self.negative_prompt = negative_prompt
        self.improve_prompt = improve_prompt

    def concurrent_provide(self):
        prompt, negative_prompt = self.prompt_generator.process(
            self.render_size,
            self.prompt,
            self.negative_prompt,
            self.improve_prompt
        )
    
        image_data, generation_info = self.image_generator.generate(
            self.render_size,
            prompt,
            negative_prompt
        )

        return self.create_image(image_data, generation_info)
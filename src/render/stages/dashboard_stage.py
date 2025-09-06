import pygame
import datetime
from render.render_pipeline import RenderStage
from generated_image import GeneratedImage

class DashboardStage(RenderStage):
    def process(self, image: GeneratedImage) -> GeneratedImage:
        surface = image.copy()
        width, height = surface.get_size()

        bar_height = int(height * 0.12)
        padding_x = int(width * 0.03)
        text_color = (255, 255, 255)

        font_date = pygame.font.SysFont(None, int(height * 0.04))
        font_time = pygame.font.SysFont(None, int(height * 0.09))
        font_temp = pygame.font.SysFont(None, int(height * 0.04))

        bar_surface = pygame.Surface((width, bar_height), pygame.SRCALPHA)
        bar_surface.fill((0, 0, 0, 180))

        now = datetime.datetime.now()
        date_text = now.strftime("%a, %b %d")
        time_text = now.strftime("%H:%M")
        temp_text = "24°C"  # TODO: placeholder, replace

        date_surf = font_date.render(date_text, True, text_color)
        time_surf = font_time.render(time_text, True, text_color)
        temp_surf = font_temp.render(temp_text, True, text_color)

        bar_mid = bar_height // 2
        bar_surface.blit(date_surf, (padding_x, bar_mid - date_surf.get_height() // 2))
        bar_surface.blit(time_surf, (width // 2 - time_surf.get_width() // 2,
                                     bar_mid - time_surf.get_height() // 2))
        bar_surface.blit(temp_surf, (width - temp_surf.get_width() - padding_x,
                                     bar_mid - temp_surf.get_height() // 2))

        surface.blit(bar_surface, (0, height - bar_height))

        return GeneratedImage(surface, image.original_image, image.generation_info)

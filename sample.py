import random
import sys

import pygame
from pygame.color import Color
from pygame.event import Event
from pygame.surface import Surface
from pygame.sysfont import SysFont

from surface.buttons import TextButton
from surface.checkbox import Checkbox
from surface.slider import Slider
from surface.textbox import Textbox

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 500
REFRESH_RATE = 60

pygame.init()
pygame.display.set_caption("Surface Sample")
pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))


class GUI:
    def __init__(self) -> None:
        self.title_font = SysFont(None, 72)
        self.component_font = SysFont(None, 36)
        self.label_font = SysFont(None, 22)
        self._init_components()
        self._init_labels()

    def _init_components(self) -> None:
        self.text_button = TextButton(
            text="Click Me", font=self.component_font, position=(50, 150)
        )
        self.bold_checkbox = Checkbox(
            position=(225, 150),
            size=(self.text_button.size[1], self.text_button.size[1]),
        )
        self.underline_checkbox = Checkbox(
            position=(275, 150),
            size=(self.text_button.size[1], self.text_button.size[1]),
        )
        self.italic_checkbox = Checkbox(
            position=(325, 150),
            size=(self.text_button.size[1], self.text_button.size[1]),
        )
        self.slider = Slider(
            position=(425, 155),
            step_count=100,
            step_width=2,
            height=self.text_button.size[1] - 10,
        )
        self.textbox = Textbox(
            position=(50, 275), size=(600, 40), font=SysFont(None, 28)
        )

    def _init_labels(self) -> None:
        self.text_button_label = self.label_font.render(
            "Text Button", True, Color("white")
        )
        self.checkboxes_label = self.label_font.render(
            "Checkboxes", True, Color("white")
        )
        self.slider_label = self.label_font.render("Slider", True, Color("white"))
        self.textbox_label = self.label_font.render("Textbox", True, Color("white"))

    def update(self, events: list[Event]) -> None:
        self.text_button.update(events)
        self.bold_checkbox.update(events)
        self.underline_checkbox.update(events)
        self.italic_checkbox.update(events)
        self.slider.update(events)
        self.textbox.update(events)

    def render(self, window: Surface) -> None:
        self.text_button.render(window)
        self.bold_checkbox.render(window)
        self.underline_checkbox.render(window)
        self.italic_checkbox.render(window)
        self.slider.render(window)
        self.textbox.render(window)

        title_surface = self.title_font.render(
            "Surface",
            True,
            Color("white"),
        )
        title_surface.set_alpha(int(255 * ((100 - self.slider.value) / 100)))
        window.blit(
            title_surface,
            (260, 50),
        )
        window.blit(self.text_button_label, (65, 200))
        window.blit(self.checkboxes_label, (250, 200))
        window.blit(self.slider_label, (510, 200))
        window.blit(self.textbox_label, (321, 330))


class Application:
    def __init__(self) -> None:
        self._window = pygame.display.get_surface()
        self._clock = pygame.time.Clock()
        self._gui = GUI()

    def _handle_text_button_click(self) -> None:
        available_colors = {
            "cyan",
            "red",
            "green",
            "yellow",
            "purple",
            "magenta",
        }.difference(self._gui.text_button.border_color)

        self._gui.text_button.border_color = Color(
            random.choice(tuple(available_colors))
        )

    def _set_textbox_border_color(self) -> None:
        text_length = len(self._gui.textbox.text)
        if text_length < 1:
            self._gui.textbox.border_color = Color("gray")
        elif 1 <= text_length < 8:
            self._gui.textbox.border_color = Color("red")
        elif 8 <= text_length < 12:
            self._gui.textbox.border_color = Color("yellow")
        elif text_length >= 12:
            self._gui.textbox.border_color = Color("green")

    def _update(self) -> None:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        self._gui.update(events)

        if self._gui.text_button.is_clicked():
            self._handle_text_button_click()

        if self._gui.bold_checkbox.is_clicked:
            self._gui.title_font.bold = self._gui.bold_checkbox.is_checked
        if self._gui.underline_checkbox.is_clicked:
            self._gui.title_font.underline = self._gui.underline_checkbox.is_checked
        if self._gui.italic_checkbox.is_clicked:
            self._gui.title_font.italic = self._gui.italic_checkbox.is_checked

        self._set_textbox_border_color()

    def _render(self) -> None:
        self._window.fill((0, 0, 0))
        self._gui.render(self._window)
        pygame.display.update()

    def run(self) -> None:
        while True:
            self._update()
            self._render()
            self._clock.tick(REFRESH_RATE)
            pygame.display.set_caption(
                f"Surface Sample - {int(self._clock.get_fps())}fps"
            )


def main() -> None:
    Application().run()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass

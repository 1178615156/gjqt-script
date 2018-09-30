from PIL.Image import Image


class Screen:
    def __init__(self):
        self.__screen: Image = None

    def screen(self) -> Image:
        assert self.__screen is not None
        return self.__screen

    def update(self, screen):
        self.__screen = screen
        self.update_after()

    def update_after(self):
        pass

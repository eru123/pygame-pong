from window_base import *


class button():
    button_col = CLR_RED
    hover_col = CLR_BLUE
    click_col = CLR_BLACK
    text_col = CLR_WHITE

    def __init__(self, x, y, w, h, text, callback=None):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.text = text
        self.callback = callback

    def draw_button(self, font, clicked):
        action = False

        pos = pygame.mouse.get_pos()

        button_rect = Rect(self.x, self.y, self.width, self.height)

        if button_rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1:
                clicked = True
                pygame.draw.rect(self.screen, self.click_col, button_rect)
            elif pygame.mouse.get_pressed()[0] == 0 and clicked == True:
                clicked = False
                action = True
            else:
                pygame.draw.rect(self.screen, self.hover_col, button_rect)
        else:
            pygame.draw.rect(self.screen, self.button_col, button_rect)

        pygame.draw.line(self.screen, CLR_BLACK, (self.x, self.y),
                         (self.x + self.width, self.y), 2)
        pygame.draw.line(self.screen, CLR_BLACK, (self.x, self.y),
                         (self.x, self.y + self.height), 2)
        pygame.draw.line(self.screen, CLR_BLACK, (self.x, self.y + self.height),
                         (self.x + self.width, self.y + self.height), 2)
        pygame.draw.line(self.screen, CLR_BLACK, (self.x + self.width, self.y),
                         (self.x + self.width, self.y + self.height), 2)

        text_img = font.render(self.text, True, self.text_col)
        text_len = text_img.get_width()
        self.screen.blit(text_img, (self.x + int(self.width / 2) -
                                    int(text_len / 2), self.y + 25))
        return action

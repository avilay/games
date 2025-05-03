from collections import deque
from dataclasses import dataclass
from enum import StrEnum, auto, IntEnum

from pyray import Vector2, draw_texture, WHITE, draw_rectangle, LIME, GREEN, Texture, vector2_move_towards, vector2_add


class Suit(StrEnum):
    CLUBS = auto()
    DIAMONDS = auto()
    HEARTS = auto()
    SPADES = auto()


class Rank(IntEnum):
    ONE = auto()
    TWO = auto()
    THREE = auto()
    FOUR = auto()
    FIVE = auto()
    SIX = auto()
    SEVEN = auto()
    EIGHT = auto()
    NINE = auto()
    TEN = auto()
    ELEVEN = auto()
    TWELVE = auto()
    THIRTEEN = auto()


@dataclass
class Card:
    suit: Suit
    rank: Rank
    is_open: bool
    texture: Texture
    back_texture: Texture
    pos: Vector2 = Vector2()
    src_pos: Vector2 = Vector2()
    dst_pos: Vector2 = Vector2()
    mov_unit: int = 0

    def move(self):
        if self.pos.x >= self.dst_pos.x and self.pos.y <= self.dst_pos.y:
            # self.pos = vector2_add(self.pos, self.mov_unit)
            self.pos = vector2_move_towards(self.pos, self.dst_pos, self.mov_unit)
        else:
            self.pos = self.dst_pos

    def render(self) -> None:
        texture = self.texture if self.is_open else self.back_texture
        draw_texture(texture, int(self.pos.x), int(self.pos.y), WHITE)

    def width(self) -> int:
        return self.texture.width

    def height(self) -> int:
        return self.texture.height


class Deck:
    def __init__(self, back_texture, cards):
        self.cards = deque(cards)
        self.back_texture = back_texture
        self._pos = Vector2()
        self.width = back_texture.width
        self.height = back_texture.height

    def render(self):
        draw_texture(self.back_texture, int(self.pos.x), int(self.pos.y), WHITE)

    def pop(self):
        return self.cards.pop()

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, vec):
        self._pos = vec
        for card in self.cards:
            card.pos = vec


class SuitSlot:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.pos = Vector2()

    def render(self):
        draw_rectangle(int(self.pos.x), int(self.pos.y), self.width, self.height, LIME)


class HoldingSlot:
    def __init__(self, capacity, width, height):
        self.capacity = capacity
        self.cards = deque()
        self.width = width
        self.height = height
        self.pos = Vector2()

    def push(self, card):
        self.cards.append(card)

    @property
    def is_next_card_open(self):
        return self.capacity - len(self.cards) == 1

    @property
    def next_card_pos(self):
        return vector2_add(self.pos, Vector2(0, 10 * len(self.cards)))

    @property
    def is_full(self):
        return len(self.cards) == self.capacity

    def render(self):
        if len(self.cards) <= 0:
            draw_rectangle(int(self.pos.x), int(self.pos.y), self.width, self.height, GREEN)
        else:
            for card in self.cards:
                card.render()

import random
from argparse import ArgumentError
from collections import deque
from dataclasses import dataclass
from enum import auto, StrEnum, IntEnum
from pathlib import Path
from typing import Protocol

from pyray import Texture, draw_texture, load_texture, WHITE, Vector2, draw_rectangle, LIME


class Drawable(Protocol):
    def render(self) -> None: ...

    def width(self) -> int: ...

    def height(self) -> int: ...

    def set_curr_pos(self, pos: Vector2) -> None: ...


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
class Card(Drawable):
    suit: Suit
    rank: Rank
    is_open: bool
    texture: Texture
    back_texture: Texture
    _curr_pos: Vector2 = Vector2()

    def render(self) -> None:
        pass

    def width(self) -> int:
        return self.texture.width

    def height(self) -> int:
        return self.texture.height

    def curr_pos(self, pos: Vector2) -> None:
        self._curr_pos = pos


class AvailableSlot:
    def __init__(self) -> None:
        self._cards: deque[Card] = deque()

    def pop(self) -> Card:
        pass

    def push(self, card: Card) -> None:
        pass

    def __len__(self) -> int:
        return len(self._cards)


class SuitSlot(Drawable):
    def __init__(self, width, height) -> None:
        self._cards: deque[Card] = deque()
        self._curr_pos: Vector2 = Vector2()
        self._width = width
        self._height = height

    def render(self):
        if len(self._cards) == 0:
            draw_rectangle(int(self._curr_pos.x), int(self._curr_pos.y), self.width(), self.height(), LIME)
        else:
            raise NotImplementedError("SuitSlot.render not implemented fully!")

    def width(self) -> int:
        return self._width

    def height(self) -> int:
        return self._height

    def set_curr_pos(self, pos: Vector2) -> None:
        self._curr_pos = pos


class HoldingSlot:
    _closed_cards: deque
    _open_cards: list

    def __init__(self) -> None:
        self._closed_cards: deque[Card] = deque()
        self._open_cards: list[Card] = []

    def pop(self) -> Card:
        pass

    def pop_block(self, starting_card: Card) -> list[Card]:
        pass

    def push(self, card: Card) -> None:
        pass

    def push_block(self, cards: list[Card]) -> None:
        pass


class Deck(Drawable):
    def __init__(self, cards: list[Card], back_texture: Texture) -> None:
        random.shuffle(cards)
        self._cards = deque(cards)
        self.back_texture: Texture = back_texture
        self._curr_pos: Vector2 | None = None

    def render(self) -> None:
        draw_texture(self.back_texture, int(self._curr_pos.x), int(self._curr_pos.y), WHITE)

    def height(self) -> int:
        return self.back_texture.height

    def width(self) -> int:
        return self.back_texture.width

    def set_curr_pos(self, pos: Vector2) -> None:
        # trace_log(TraceLogLevel.LOG_INFO, f"Setting deck's current position: {pos.x}, {pos.y}")
        print("\nAPTG DEBUG: Inside deck::curr_pos\n")
        self._curr_pos = pos


# type GameObjects = GameObjects


class GameObjects:
    _instance = None

    def __init__(self, resource_root: Path):
        self.resource_root = resource_root
        back_texture = load_texture(str(resource_root / "card_back_scaled.png"))

        self.all_cards: list[Card] = []
        for suit in Suit:
            for rank in Rank:
                # texture_file = resource_root / suit / f"{rank}_{suit}.png"
                # texture = load_texture(str(texture_file))
                texture = Texture()
                self.all_cards.append(Card(Suit(suit), Rank(rank), is_open=False, texture=texture, back_texture=back_texture))

        self.available_slot = AvailableSlot()
        self.suit_slots = [SuitSlot(back_texture.width, back_texture.height) for _ in range(4)]
        self.holding_slots = [HoldingSlot() for _ in range(7)]
        self.deck = Deck(self.all_cards, back_texture)

    @classmethod
    def get_instance(cls, resource_root: Path | None = None):
        if resource_root is None and cls._instance is None:
            raise ArgumentError("resource_root must be provided for first time instantiation!")

        if cls._instance is None:
            cls._instance = GameObjects(resource_root)
        return cls._instance

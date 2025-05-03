import asyncio
import platform
import sys
from enum import Enum, auto
from pathlib import Path

from pyray import (
    window_should_close,
    close_window,
    init_window,
    init_audio_device,
    set_target_fps,
    load_texture,
    Vector2,
    begin_drawing,
    clear_background,
    end_drawing,
    DARKGREEN, set_trace_log_level, TraceLogLevel,
)

from solitaire.game_objects import Deck, SuitSlot, HoldingSlot, Suit, Rank, Card

# SCREEN_WIDTH = 980
# SCREEN_HEIGHT = 1461
ANIM_FREQUENCY = 1  # Number frames to do one animation change
ANIM_AMPLITUDE = 32  # Number of pixels to move in one animation
FPS = 60
MARGIN_SIDE = 3
GUTTER = 3
MARGIN_TOP = 10


def are_vectors_equal(v1, v2):
    return v1.x == v2.x and v1.y == v2.y


class GameState(Enum):
    STARTING = auto()
    DEALING = auto()
    WAITING = auto()
    MOVING = auto()
    END = auto()


def native():
    screen_width = 655
    screen_height = 1000

    resource_root = Path(__file__).parent.parent / "native-assets"
    # resource_root = main_dir / "resources"

    init_window(screen_width, screen_height, "Solitaire")
    init_audio_device()
    set_target_fps(FPS)
    set_trace_log_level(TraceLogLevel.LOG_WARNING)

    back_texture = load_texture(str(resource_root / "card_back.png"))

    all_cards = []
    for suit in Suit:
        for rank in Rank:
            texture_file = resource_root / suit / f"{rank}_{suit}.png"
            texture = load_texture(str(texture_file))
            all_cards.append(
                Card(Suit(suit), Rank(rank), is_open=False, texture=texture, back_texture=back_texture,
                     mov_unit=ANIM_AMPLITUDE))

    deck = Deck(back_texture, all_cards)
    deck.pos = Vector2(screen_width - deck.width - MARGIN_SIDE, MARGIN_TOP)

    suit_slots = [SuitSlot(back_texture.width, back_texture.height) for _ in range(4)]
    for i, suit_slot in enumerate(suit_slots):
        suit_slot.pos = Vector2(MARGIN_SIDE + i * (suit_slot.width + GUTTER), MARGIN_TOP)

    holding_slots = [HoldingSlot(i + 1, back_texture.width, back_texture.height) for i in range(7)]
    for i, holding_slot in enumerate(holding_slots):
        holding_slot.pos = Vector2(
            MARGIN_SIDE + i * (holding_slot.width + GUTTER), MARGIN_TOP + suit_slots[0].height + (2 * GUTTER)
        )

    card = None
    is_animating = False
    frame_count = 0
    state = GameState.DEALING
    curr_holding_slot = None
    slot_idx = 0

    while not window_should_close():
        frame_count += 1

        match state:
            case GameState.DEALING:
                # if state == GameState.DEALING:
                if not is_animating:
                    curr_holding_slot = holding_slots[slot_idx]
                    card = deck.pop()
                    card.is_open = curr_holding_slot.is_next_card_open
                    card.src_pos = deck.pos
                    card.dst_pos = curr_holding_slot.next_card_pos
                    # print(f"APTG DEBUG: {card.src_pos.x}, {card.src_pos.y} to {card.dst_pos.x}, {card.dst_pos.y}")
                    is_animating = True
                else:
                    is_animating = not are_vectors_equal(card.pos, card.dst_pos)
                    if not is_animating:
                        # print("APTG DEBUG: Animation complete!")
                        curr_holding_slot.push(card)
                        card = None
                        slot_idx += 1
                    if slot_idx == 7:
                        for idx, holding_slot in enumerate(holding_slots):
                            if not holding_slot.is_full:
                                slot_idx = idx
                                break
                        if slot_idx == 7:
                            state = GameState.WAITING
            case _:
                pass

        if frame_count > ANIM_FREQUENCY:
            if card:
                card.move()
            frame_count = 0

        begin_drawing()
        clear_background(DARKGREEN)

        deck.render()

        for suit_slot in suit_slots:
            suit_slot.render()

        for holding_slot in holding_slots:
            holding_slot.render()

        if card:
            card.render()

        end_drawing()

    close_window()


async def web():
    screen_width = 980
    screen_height = 1461

    resource_root = Path("./web-assets")

    init_window(screen_width, screen_height, "Solitaire")
    init_audio_device()
    set_target_fps(30)

    platform.window.window_resize()

    back_texture = load_texture(str(resource_root / "card_back_scaled_web.png"))
    deck = Deck(back_texture)
    deck.pos = Vector2(screen_width - deck.width - MARGIN_SIDE, MARGIN_TOP)

    suit_slots = [SuitSlot(back_texture.width, back_texture.height) for _ in range(4)]
    for i, suit_slot in enumerate(suit_slots):
        suit_slot.pos = Vector2(MARGIN_SIDE + i * (suit_slot.width + GUTTER), MARGIN_TOP)

    holding_slots = [HoldingSlot(back_texture.width, back_texture.height) for _ in range(7)]
    for i, holding_slot in enumerate(holding_slots):
        holding_slot.pos = Vector2(
            MARGIN_SIDE + i * (holding_slot.width + GUTTER), MARGIN_TOP + suit_slots[0].height + (2 * GUTTER)
        )

    while not window_should_close():
        begin_drawing()
        clear_background(DARKGREEN)

        deck.render()

        for suit_slot in suit_slots:
            suit_slot.render()

        for holding_slot in holding_slots:
            holding_slot.render()

        end_drawing()

        await asyncio.sleep(0)
    close_window()


if sys.platform == "emscripten":
    asyncio.run(web())
else:
    native()

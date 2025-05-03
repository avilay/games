from pathlib import Path

from pyray import (
    init_window,
    set_target_fps,
    init_audio_device,
    begin_drawing,
    clear_background,
    end_drawing,
    DARKGREEN,
    Vector2,
)

from solitaire.game_objects_old import GameObjects

HORIZ_MARGIN = 2
VERT_MARGIN = 10
VERT_GUTTER = 2
POSE_PER_SEC = 10
FPS = 60

frame_count = 0


def initialize(screen_width, screen_height, resource_root: Path) -> None:
    init_window(screen_width, screen_height, "Solitaire")
    init_audio_device()
    set_target_fps(FPS)

    game_objs = GameObjects.get_instance(resource_root)

    game_objs.deck.set_curr_pos(Vector2(screen_width - game_objs.deck.width() - HORIZ_MARGIN, VERT_MARGIN))

    for i, slot in enumerate(game_objs.suit_slots):
        slot.set_curr_pos(Vector2(HORIZ_MARGIN + i * (slot.width() + HORIZ_MARGIN), VERT_MARGIN))


def loop():
    game_objs = GameObjects.get_instance()
    begin_drawing()
    clear_background(DARKGREEN)
    game_objs.deck.render()
    for slot in game_objs.suit_slots:
        slot.render()
    end_drawing()

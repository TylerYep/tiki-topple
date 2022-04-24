from tiki_topple.enums import Action, Tiki

ID = int
Goal = tuple[Tiki, Tiki, Tiki]

TIKI_GROUPS = (
    (Tiki.NANI, Tiki.WIKIWIKI, Tiki.HUHU),
    (Tiki.NUI, Tiki.LOKAHI, Tiki.AKAMAI),
    (Tiki.EEPO, Tiki.HOOKIPA, Tiki.KAPU),
)
STARTING_ACTIONS = [
    Action.UP_ONE,
    Action.UP_ONE,
    Action.UP_TWO,
    Action.UP_THREE,
    Action.TIKI_TOAST,
    Action.TIKI_TOAST,
    Action.TIKI_TOPPLE,
]

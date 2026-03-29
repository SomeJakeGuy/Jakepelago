from .sms_region_helper import *

# Pianta Village
PIANTA_VILLAGE_ENTRANCE: SmsRegion = SmsRegion(
    SmsRegionName.PIANTA_ENTRANCE,
    requirements=[
        Requirements([[NozzleType.rocket]], shines=10),
        Requirements([[NozzleType.rocket]], skip_forward=True),
    ],
    ticketed="Pianta Village Ticket",
    parent_region=SmsRegionName.PLAZA,
)

PIANTA_VILLAGE_ONE: SmsRegion = SmsRegion(
    SmsRegionName.PIANTA_ONE,
    shines=[
        Shine(
            "Chain Chomplets Unchained",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=60,
        ),
    ],
    blue_coins=[
        BlueCoin("River End", in_game_bit=432),
        BlueCoin("Grass", in_game_bit=433),
        BlueCoin("Back Tree", [Requirements([[NozzleType.hover]])], in_game_bit=434),
        BlueCoin("River Bridge", in_game_bit=435),
        BlueCoin("Left Tree", [Requirements([[NozzleType.hover]])], in_game_bit=438),
        BlueCoin("Waterfall", [Requirements([[NozzleType.spray]])], in_game_bit=439),
        BlueCoin(
            "Wall Triangle", [Requirements([[NozzleType.spray]])], in_game_bit=443
        ),
        BlueCoin(
            "Hot Tub Triangle", [Requirements([[NozzleType.spray]])], in_game_bit=444
        ),
        BlueCoin("Left M", [Requirements([[NozzleType.spray]])], in_game_bit=445),
        BlueCoin("Right M", [Requirements([[NozzleType.spray]])], in_game_bit=446),
        BlueCoin("Spawn M", [Requirements([[NozzleType.spray]])], in_game_bit=447),
        BlueCoin("Underside M", [Requirements([[NozzleType.spray]])], in_game_bit=448),
        BlueCoin("Moon", [Requirements(ROCKET_AND_SPRAY_AND_HOVER)], in_game_bit=420),
        BlueCoin("Statue's Nose", in_game_bit=429),
    ],
    parent_region=SmsRegionName.PIANTA_ENTRANCE,
)

PIANTA_VILLAGE_TWO: SmsRegion = SmsRegion(
    SmsRegionName.PIANTA_TWO,
    requirements=[
        Requirements(location=f"{SmsRegionName.PIANTA_ONE} - Chain Chomplets Unchained")
    ],
    shines=[
        Shine(
            "Il Piantissimo's Crazy Climb",
            [Requirements(manual_none=True)],
            in_game_bit=65,
        )
    ],
    blue_coins=[
        BlueCoin("Sign", [Requirements([[NozzleType.spray]])], in_game_bit=431)
    ],
    parent_region=SmsRegionName.PIANTA_ENTRANCE,
)

PIANTA_VILLAGE_THREE: SmsRegion = SmsRegion(
    SmsRegionName.PIANTA_THREE,
    requirements=[
        Requirements(
            location=f"{SmsRegionName.PIANTA_TWO} - Il Piantissimo's Crazy Climb"
        )
    ],
    shines=[
        Shine(
            "The Goopy Inferno",
            requirements=[Requirements(SPROCKET_OR_HOVER)],
            hard=[Requirements(SPROCKET_OR_HOVER_OR_TURBO)],
            tears=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=62,
        ),
    ],
    blue_coins=[
        BlueCoin("Giant M", [Requirements([[NozzleType.spray]])], in_game_bit=430),
        BlueCoin(
            "Burning Pianta", [Requirements([[NozzleType.spray]])], in_game_bit=442
        ),
        BlueCoin("FLUDD M", [Requirements([[NozzleType.spray]])], in_game_bit=449),
    ],
    parent_region=SmsRegionName.PIANTA_ENTRANCE,
)

PIANTA_VILLAGE_FOUR: SmsRegion = SmsRegion(
    SmsRegionName.PIANTA_FOUR,
    requirements=[
        Requirements(location=f"{SmsRegionName.PIANTA_THREE} - The Goopy Inferno")
    ],
    shines=[
        Shine(
            "Chain Chomp's Bath",
            requirements=[Requirements([[NozzleType.spray]])],
            hard=[Requirements(manual_none=True)],
            in_game_bit=61,
        ),
    ],
    blue_coins=[],
    parent_region=SmsRegionName.PIANTA_ENTRANCE,
)

PIANTA_VILLAGE_FIVE: SmsRegion = SmsRegion(
    SmsRegionName.PIANTA_FIVE,
    requirements=[
        Requirements(location=f"{SmsRegionName.PIANTA_FOUR} - Chain Chomp's Bath")
    ],
    shines=[
        Shine(
            "Secret of the Village Underside",
            requirements=[Requirements([[NozzleType.yoshi]])],
            advanced=[Requirements(HOVER_OR_YOSHI)],
            in_game_bit=64,
        ),
        Shine(
            "Red Coin Chucksters",
            requirements=[Requirements(YOSHI_AND_HOVER)],
            advanced=[Requirements([[NozzleType.hover]])],
            tears=[Requirements(HOVER_OR_YOSHI)],
            in_game_bit=68,
        ),
        Shine("100 Coins", [Requirements(ALL_SPLASHER)], hundred=True, in_game_bit=106),
    ],
    blue_coins=[
        BlueCoin("Back Beehive", [Requirements([[NozzleType.yoshi]])], in_game_bit=436),
        BlueCoin(
            "Front Beehive", [Requirements([[NozzleType.yoshi]])], in_game_bit=437
        ),
        BlueCoin("Butterflies", [Requirements([[NozzleType.yoshi]])], in_game_bit=440),
    ],
    parent_region=SmsRegionName.PIANTA_ENTRANCE,
)

PIANTA_VILLAGE_SIX: SmsRegion = SmsRegion(
    SmsRegionName.PIANTA_SIX,
    requirements=[
        Requirements(
            location=f"{SmsRegionName.PIANTA_FIVE} - Secret of the Village Underside"
        )
    ],
    shines=[
        Shine(
            "Piantas in Need",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            advanced=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=63,
        ),
    ],
    blue_coins=[
        BlueCoin(
            "Pianta in Need A", [Requirements([[NozzleType.spray]])], in_game_bit=421
        ),
        BlueCoin(
            "Pianta in Need B", [Requirements([[NozzleType.spray]])], in_game_bit=422
        ),
        BlueCoin(
            "Pianta in Need C", [Requirements([[NozzleType.spray]])], in_game_bit=423
        ),
        BlueCoin(
            "Pianta in Need D", [Requirements([[NozzleType.spray]])], in_game_bit=424
        ),
        BlueCoin(
            "Pianta in Need E", [Requirements([[NozzleType.spray]])], in_game_bit=425
        ),
        BlueCoin(
            "Pianta in Need F", [Requirements([[NozzleType.spray]])], in_game_bit=426
        ),
        BlueCoin(
            "Pianta in Need G", [Requirements([[NozzleType.spray]])], in_game_bit=427
        ),
        BlueCoin(
            "Pianta in Need H", [Requirements([[NozzleType.spray]])], in_game_bit=428
        ),
    ],
    parent_region=SmsRegionName.PIANTA_ENTRANCE,
)

PIANTA_VILLAGE_SEVEN: SmsRegion = SmsRegion(
    SmsRegionName.PIANTA_SEVEN,
    requirements=[
        Requirements(location=f"{SmsRegionName.PIANTA_SIX} - Piantas in Need")
    ],
    shines=[
        Shine(
            "Shadow Mario Runs Wild",
            requirements=[
                Requirements(
                    [[NozzleType.spray]],
                )
            ],
            advanced=[
                Requirements(
                    SPRAY_OR_HOVER,
                )
            ],
            in_game_bit=66,
        )
    ],
    blue_coins=[],
    parent_region=SmsRegionName.PIANTA_ENTRANCE,
)

PIANTA_VILLAGE_EIGHT: SmsRegion = SmsRegion(
    SmsRegionName.PIANTA_EIGHT,
    requirements=[
        Requirements(location=f"{SmsRegionName.PIANTA_SEVEN} - Shadow Mario Runs Wild")
    ],
    shines=[
        Shine(
            "Fluff Festival Coin Hunt",
            requirements=[
                Requirements(
                    ROCKET_OR_HOVER,
                    location=f"{SmsRegionName.PIANTA_SEVEN} - Shadow Mario Runs Wild",
                )
            ],
            advanced=[
                Requirements(
                    ROCKET_OR_HOVER_OR_TURBO,
                    location=f"{SmsRegionName.PIANTA_SEVEN} - Shadow Mario Runs Wild",
                )
            ],
            in_game_bit=67,
        ),
        Shine(
            "Soak the Sun",
            requirements=[Requirements(SPRAY_AND_ROCKET_OR_SPRAY_AND_HOVER)],
            hard=[Requirements(SPRAY_AND_OTHER_FLUDD)],
            in_game_bit=69,
        ),
    ],
    blue_coins=[BlueCoin("Bird", [Requirements(SPRAY_AND_HOVER)], in_game_bit=441)],
    nozzle_boxes=[
        NozzleBox("Rocket Box", [Requirements([[NozzleType.hover]])], in_game_bit=882)
    ],
    parent_region=SmsRegionName.PIANTA_ENTRANCE,
)

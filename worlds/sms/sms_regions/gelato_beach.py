from .sms_region_helper import *

GELATO_BEACH_ENTRANCE: SmsRegion = SmsRegion(
    SmsRegionName.GELATO_ENTRANCE,
    requirements=[
        Requirements(ANY_SPLASHER, shines=5),
        Requirements(skip_forward=True),
    ],
    shines=[
        Shine(
            "100 Coins",
            requirements=[
                Requirements(SPROCKET_OR_HOVER),
                Requirements(
                    SPRAY_OR_HOVER_OR_ROCKET,
                    location=f"{SmsRegionName.GELATO_FIVE} - It's Shadow Mario! After Him!",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    manual_none=True,
                    location=f"{SmsRegionName.GELATO_FIVE} - It's Shadow Mario! After Him!",
                ),
            ],
            advanced=[Requirements(SPRAY_OR_HOVER_OR_ROCKET)],
            hundred=True,
            in_game_bit=102,
        ),
    ],
    ticketed="Gelato Beach Ticket",
    parent_region=SmsRegionName.PLAZA,
)

GELATO_BEACH_ONE: SmsRegion = SmsRegion(
    SmsRegionName.GELATO_ONE,
    shines=[
        Shine(
            "Dune Bud Sand Castle Secret",
            [Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=20,
        ),
        Shine(
            "Red Coins in the Sand Castle",
            requirements=[Requirements([[NozzleType.hover]])],
            hard=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=28,
        ),
        Shine(
            "Sandy Shine Sprite",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=29,
        ),
        Shine(
            "100 Coins",
            requirements=[
                Requirements(SPROCKET_OR_HOVER),
                Requirements(
                    SPRAY_OR_HOVER_OR_ROCKET,
                    location=f"{SmsRegionName.GELATO_FIVE} - It's Shadow Mario! After Him!",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    manual_none=True,
                    location=f"{SmsRegionName.GELATO_FIVE} - It's Shadow Mario! After Him!",
                ),
            ],
            advanced=[Requirements(SPRAY_OR_HOVER_OR_ROCKET)],
            hundred=True,
            in_game_bit=102,
        ),
    ],
    blue_coins=[
        BlueCoin(
            "Juicer",
            [
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    location=f"{SmsRegionName.GELATO_FIVE} - Il Piantissimo's Sand Sprint"
                ),
            ],
            in_game_bit=275,
        ),
        BlueCoin(
            "Rocket M",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_FIVE} - Il Piantissimo's Sand Sprint",
                ),
            ],
            advanced=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_FIVE} - Il Piantissimo's Sand Sprint",
                ),
            ],
            in_game_bit=276,
        ),
        BlueCoin(
            "Spawn Triangle",
            requirements=[Requirements([[NozzleType.spray]])],
            hard=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_FIVE} - Il Piantissimo's Sand Sprint",
                ),
            ],
            in_game_bit=277,
        ),
        BlueCoin(
            "Trees Triangle",
            requirements=[Requirements([[NozzleType.spray]])],
            hard=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_FIVE} - Il Piantissimo's Sand Sprint",
                ),
            ],
            advanced=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_FIVE} - Il Piantissimo's Sand Sprint",
                ),
            ],
            in_game_bit=278,
        ),
        BlueCoin(
            "Left Bird",
            requirements=[
                Requirements([[NozzleType.spray]]),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_FIVE} - Il Piantissimo's Sand Sprint",
                ),
            ],
            tears=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_FIVE} - Il Piantissimo's Sand Sprint",
                ),
            ],
            in_game_bit=280,
        ),
        BlueCoin(
            "Right Bird",
            requirements=[
                Requirements([[NozzleType.spray]]),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_FIVE} - Il Piantissimo's Sand Sprint",
                ),
            ],
            tears=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_FIVE} - Il Piantissimo's Sand Sprint",
                ),
            ],
            in_game_bit=281,
        ),
        BlueCoin(
            "Highest Rope",
            requirements=[Requirements(ROCKET_OR_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=282,
        ),
        BlueCoin(
            "Pole",
            requirements=[Requirements(ROCKET_OR_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=283,
        ),
        BlueCoin("Deck", in_game_bit=288),
        BlueCoin(
            "Swing",
            requirements=[Requirements(SPRAY_OR_HOVER)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=289,
        ),
        BlueCoin("Big Tree", in_game_bit=290),
        BlueCoin("Crevice", in_game_bit=291),
        BlueCoin("Sand Cabana Roof", in_game_bit=293),
    ],
    parent_region=SmsRegionName.GELATO_ENTRANCE,
)

GELATO_BEACH_TWO: SmsRegion = SmsRegion(
    SmsRegionName.GELATO_TWO,
    requirements=[
        Requirements(
            location=f"{SmsRegionName.GELATO_ONE} - Dune Bud Sand Castle Secret"
        )
    ],
    shines=[
        Shine(
            "Mirror Madness! Tilt, Slam, Bam!",
            requirements=[Requirements([[NozzleType.spray]])],
            hard=[Requirements(SPRAY_OR_HOVER)],
            advanced=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=21,
        )
    ],
    blue_coins=[
        BlueCoin(
            "Big Sand Shine",
            requirements=[
                Requirements(SPRAY_OR_HOVER),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_FIVE} - Il Piantissimo's Sand Sprint",
                ),
            ],
            hard=[
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_FIVE} - Il Piantissimo's Sand Sprint",
                ),
            ],
            in_game_bit=292,
        )
    ],
    parent_region=SmsRegionName.GELATO_ENTRANCE,
)

GELATO_BEACH_THREE: SmsRegion = SmsRegion(
    SmsRegionName.GELATO_THREE,
    requirements=[
        Requirements(
            location=f"{SmsRegionName.GELATO_TWO} - Mirror Madness! Tilt, Slam, Bam!"
        )
    ],
    shines=[
        Shine(
            "Wiggler Ahoy! Full Steam Ahead!",
            [Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            in_game_bit=22,
        )
    ],
    blue_coins=[],
    parent_region=SmsRegionName.GELATO_ENTRANCE,
)

GELATO_BEACH_FOUR: SmsRegion = SmsRegion(
    SmsRegionName.GELATO_FOUR,
    requirements=[
        Requirements(
            location=f"{SmsRegionName.GELATO_THREE} - Wiggler Ahoy! Full Steam Ahead!"
        )
    ],
    shines=[
        Shine(
            "The Sand Bird is Born",
            requirements=[Requirements([[NozzleType.hover]])],
            hard=[Requirements(manual_none=True)],
            in_game_bit=23,
        )
    ],
    blue_coins=[
        BlueCoin(
            "Sand Bird A",
            [Requirements([[NozzleType.hover]])],
            [Requirements(manual_none=True)],
            in_game_bit=296,
        ),
        BlueCoin(
            "Sand Bird B",
            [Requirements([[NozzleType.hover]])],
            [Requirements(manual_none=True)],
            in_game_bit=297,
        ),
        BlueCoin(
            "Sand Bird C",
            [Requirements([[NozzleType.hover]])],
            [Requirements(manual_none=True)],
            in_game_bit=298,
        ),
        BlueCoin(
            "Sand Bird D",
            [Requirements([[NozzleType.hover]])],
            [Requirements(manual_none=True)],
            in_game_bit=299,
        ),
    ],
    nozzle_boxes=[NozzleBox("Turbo Box", in_game_bit=877)],
    parent_region=SmsRegionName.GELATO_ENTRANCE,
)

GELATO_BEACH_FIVE: SmsRegion = SmsRegion(
    SmsRegionName.GELATO_FIVE,
    requirements=[
        Requirements(location=f"{SmsRegionName.GELATO_FOUR} - The Sand Bird is Born")
    ],
    shines=[
        Shine(
            "Il Piantissimo's Sand Sprint",
            requirements=[Requirements(ROCKET_OR_HOVER_OR_TURBO)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=24,
        )
    ],
    blue_coins=[
        BlueCoin(
            "Blue Cataquack",
            [
                Requirements(SPRAY_OR_HOVER_OR_TURBO),
                Requirements(
                    [[NozzleType.yoshi]],
                    location=f"{SmsRegionName.GELATO_FIVE} - Il Piantissimo's Sand Sprint",
                ),
            ],
            [Requirements(manual_none=True)],
            in_game_bit=273,
        )
    ],
    nozzle_boxes=[
        NozzleBox("Rocket Box", [Requirements(ROCKET_OR_SPLASHER)], in_game_bit=876)
    ],
    parent_region=SmsRegionName.GELATO_ENTRANCE,
)

GELATO_BEACH_SIX: SmsRegion = SmsRegion(
    SmsRegionName.GELATO_SIX,
    requirements=[
        Requirements(
            location=f"{SmsRegionName.GELATO_FIVE} - Il Piantissimo's Sand Sprint"
        )
    ],
    shines=[Shine("Red Coins in the Coral Reef", in_game_bit=25)],
    blue_coins=[
        BlueCoin(
            "Yellow Goo Dune Bud", [Requirements([[NozzleType.yoshi]])], in_game_bit=279
        ),
        BlueCoin("Beehive", [Requirements([[NozzleType.yoshi]])], in_game_bit=295),
    ],
    parent_region=SmsRegionName.GELATO_ENTRANCE,
)

GELATO_BEACH_SEVEN: SmsRegion = SmsRegion(
    SmsRegionName.GELATO_SEVEN,
    requirements=[
        Requirements(
            location=f"{SmsRegionName.GELATO_SIX} - Red Coins in the Coral Reef"
        )
    ],
    shines=[
        Shine(
            "It's Shadow Mario! After Him!",
            requirements=[Requirements([[NozzleType.spray]])],
            hard=[Requirements(SPRAY_OR_HOVER)],
            in_game_bit=26,
        )
    ],
    blue_coins=[],
    parent_region=SmsRegionName.GELATO_ENTRANCE,
)

GELATO_BEACH_EIGHT: SmsRegion = SmsRegion(
    SmsRegionName.GELATO_EIGHT,
    requirements=[
        Requirements(
            location=f"{SmsRegionName.GELATO_SEVEN} - It's Shadow Mario! After Him!"
        )
    ],
    shines=[
        Shine(
            "The Watermelon Festival",
            requirements=[Requirements(SPRAY_OR_HOVER_OR_TURBO)],
            hard=[Requirements(manual_none=True)],
            in_game_bit=27,
        )
    ],
    blue_coins=[],
    parent_region=SmsRegionName.GELATO_ENTRANCE,
)

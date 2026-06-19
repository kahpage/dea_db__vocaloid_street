# Notes:
import sys
import json
from pathlib import Path
from typing import Any

# Add project root to sys.path (find the directory containing db_structs.py)
_root = Path(__file__).resolve().parent
while _root.parent != _root:
    if (_root / "db_structs.py").exists():
        if str(_root) not in sys.path:
            sys.path.append(str(_root))
        break
    _root = _root.parent

from db_structs import (
    Medium,
    Circle,
    Event,
    EventGroup,
    Source,
    ReliabilityTypes,
    OriginTypes,
    Location,
)

RT, OT = ReliabilityTypes, OriginTypes

PATH_HELPER = Path(__file__).parent
PATH_EVENT_GROUP = PATH_HELPER.parent
PATH_MEDIA = PATH_EVENT_GROUP / "media"


def retrieve_circles(event_name: str) -> list[Circle]:
    """Retrieve circles of given event. In the circle file has not been created, execute the creation script first."""
    circles_json_path = PATH_HELPER / event_name / "circles.json"
    if not circles_json_path.exists():
        print(
            f"Circle file for {event_name} not found, running the creation script ..."
        )
        creation_script_path = PATH_HELPER / event_name / "main.py"
        if not creation_script_path.exists():
            raise FileNotFoundError(
                f"Creation script for {event_name} not found at {creation_script_path}"
            )
        # Import main() from the creation script and execute
        import importlib.util

        spec = importlib.util.spec_from_file_location(
            f"{event_name}.main", creation_script_path
        )
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "main"):
                module.main()

        if not circles_json_path.exists():
            raise FileNotFoundError(
                f"Creation script {creation_script_path} failed to create {circles_json_path}"
            )

    with circles_json_path.open("r", encoding="utf-8") as f:
        circles_raw = json.load(f)
    return [Circle.load_from_json(c) for c in circles_raw]


if __name__ == "__main__":
    events: list[Event] = []
    active_events: list[int | str] = list(range(1, 12 + 1)) + [
        "tajimi",
        "sendai",
        "sendai2",
    ]

    i = 1  # ==== vocaloid_street1 ====
    if i in active_events:
        event_name = f"vocaloid_street{i}"
        print(f"Processing {event_name} ...")

        media_ = [
            Medium(
                "01_20180801210313_top.png",
                [
                    Source(
                        "https://web.archive.org/web/20180801210313/http://voca-st.com/",
                        (RT.Reliable, OT.Official),
                    )
                ],
                comments="イラスト·ロゴ:GYARI(ココアシガレットP)",
            ),
            Medium(
                "01_layout.pdf",
                [
                    Source(
                        "https://web.archive.org/web/20190330135726/http://voca-st.com/circlelist.php",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3267.751071069338!2d135.7783858758542!3d35.01293597281049!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x600108e5fdb0fb75%3A0x32f576fbc1dc5042!2sMiyako%20Messe%20(Kyoto%20International%20Exhibition%20Hall)!5e0!3m2!1sen!2sfr!4v1781558408737!5m2!1sen!2sfr",
                description="みやこめっせ(京都市勧業館)",
                sources=[
                    Source(
                        "https://x.com/voca_st/status/1018457181073489920",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[
                "VOCALOID STREET",
                "ボーカロイドストリート",
                "ボカスト",
                f"VOCALOID STREET {i:02d}",
                f"ボーカロイドストリート{i:02d}",
                f"ボカスト{i:02d}",
            ],
            dates="2019.03.10",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://x.com/voca_st/status/1018457181073489920",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    "Participating circles: https://web.archive.org/web/20190330135726/http://voca-st.com/circlelist.php",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            # description=None,
            # comments=None,
            last_edited="2026.06.15",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    n = "tajimi"  # ==== vocaloid_streettajimi ====
    if n in active_events:
        event_name = f"vocaloid_street{n}"
        print(f"Processing {event_name} ...")

        media_ = [
            Medium(
                "tajimi_EBrNtI0VAAAGhyO.png",
                [
                    Source(
                        "https://x.com/voca_st/status/1160466040364515328",
                        (RT.Reliable, OT.Official),
                    )
                ],
                comments="Artist: 黎(クロイ,@kuroi0)",
            ),
            Medium(
                "tajimi_layout.pdf",
                [
                    Source(
                        "https://web.archive.org/web/20191209210239/http://voca-st.com/circlelist",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3254.866190194564!2d137.1268545758678!3d35.33414417270119!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x60036a70848ce44f%3A0xaea80b3888b9c8db!2sSangyobunka%20Center!5e0!3m2!1sen!2sfr!4v1781559191962!5m2!1sen!2sfr",
                description="多治見市産業文化センター",
                sources=[
                    Source(
                        "https://web.archive.org/web/20190918183721/http://voca-st.com/about",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[
                "VOCALOID STREET in 多治見",
                "ボーカロイドストリート in 多治見",
                "ボカスト in 多治見",
                "VOCALOID STREET in Tajimi",
            ],
            dates="2019.10.20",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20190918183721/http://voca-st.com/about",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    "Participating circles: https://web.archive.org/web/20191209210239/http://voca-st.com/circlelist",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            # description=None,
            # comments=None,
            last_edited="2026.06.15",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = 2  # ==== vocaloid_street2 ====
    if i in active_events:
        event_name = f"vocaloid_street{i}"
        print(f"Processing {event_name} ...")

        media_ = [
            Medium(
                "02_20200222012935_top.png",
                [
                    Source(
                        "https://web.archive.org/web/20200222012935/http://voca-st.com/",
                        (RT.Reliable, OT.Official),
                    )
                ],
                comments="イラスト：黎(クロイ)",
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3267.751071069338!2d135.7783858758542!3d35.01293597281049!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x600108e5fdb0fb75%3A0x32f576fbc1dc5042!2sMiyako%20Messe%20(Kyoto%20International%20Exhibition%20Hall)!5e0!3m2!1sen!2sfr!4v1781558408737!5m2!1sen!2sfr",
                description="京都府　みやこめっせ(京都市勧業館)",
                sources=[
                    Source(
                        "https://web.archive.org/web/20200222012935/http://voca-st.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[
                f"VOCALOID STREET {i:02d}",
                f"ボーカロイドストリート{i:02d}",
                f"ボカスト{i:02d}",
            ],
            dates="2020.04.05 → CANCELLED",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20200222012935/http://voca-st.com/",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    'Cancelled: "イベントは中止となりました。" https://web.archive.org/web/20200811030143/http://voca-st.com/',
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    "Participating circles: https://web.archive.org/web/20210131061732/http://voca-st.com/circlelist",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            # description=None,
            # comments=None,
            last_edited="2026.06.16",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = 3  # ==== vocaloid_street3 ====
    if i in active_events:
        event_name = f"vocaloid_street{i}"
        print(f"Processing {event_name} ...")

        media_ = [
            Medium(
                "03_20210204092210_top.png",
                [
                    Source(
                        "https://web.archive.org/web/20210204092210/http://voca-st.com/index",
                        (RT.Reliable, OT.Official),
                    )
                ],
                comments="イラスト:さつき",
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3266.3094377477023!2d136.8427694758556!3d35.04900197279786!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x600378c7ed0d5733%3A0x73484dff1b6c3f92!2sPort%20Messe%20Nagoya%20Exhibition%20Hall%202!5e0!3m2!1sen!2sfr!4v1781645670036!5m2!1sen!2sfr",
                description="名古屋市国際展示場 (ボートメッセなこや) 第2展示館",
                sources=[
                    Source(
                        "https://web.archive.org/web/20210204092210/http://voca-st.com/index",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[
                f"VOCALOID STREET {i:02d}",
                f"ボーカロイドストリート{i:02d}",
                f"ボカスト{i:02d}",
            ],
            dates="2021.03.27",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20210204092210/http://voca-st.com/index",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    "Participating circles: https://web.archive.org/web/20210624083117/http://voca-st.com/circlelist",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            # description=None,
            # comments=None,
            last_edited="2026.06.16",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = 4  # ==== vocaloid_street4 ====
    if i in active_events:
        event_name = f"vocaloid_street{i}"
        print(f"Processing {event_name} ...")

        media_ = [
            Medium(
                "04_20211230004440_top.png",
                [
                    Source(
                        "https://web.archive.org/web/20211230004440/http://voca-st.com/",
                        (RT.Reliable, OT.Official),
                    )
                ],
                comments="イラスト:yoku",
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3270.3660211470983!2d135.74787622585134!3d34.94743372283293!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x60010587a8d65d7b%3A0xc0fa6c9a0c5ce765!2sKy%C5%8Dto%20Pulse%20Plaza!5e0!3m2!1sen!2sfr!4v1781646695675!5m2!1sen!2sfr",
                description="京都府総合見本市会館 (京都パルスプラザ)",
                sources=[
                    Source(
                        "https://web.archive.org/web/20220117062807/http://voca-st.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[
                f"VOCALOID STREET {i:02d}",
                f"ボーカロイドストリート{i:02d}",
                f"ボカスト{i:02d}",
            ],
            dates="2022.01.10",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20211230004440/http://voca-st.com/",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    "Participating circles: https://web.archive.org/web/20220328181339/http://voca-st.com/circlelist",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            # description=None,
            # comments=None,
            last_edited="2026.06.16",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = 5  # ==== vocaloid_street5 ====
    if i in active_events:
        event_name = f"vocaloid_street{i}"
        print(f"Processing {event_name} ...")

        media_ = [
            Medium(
                "05_4268.png",
                [Source("https://vocadb.net/E/4268", (RT.Likely, OT.External))],
                comments="イラスト:たんたんめん",
            ),
            Medium(
                "05_Fa19BGfVQAA7w-A.jpg",
                [
                    Source(
                        "https://x.com/voca_st/status/1562042560930992129",
                        (RT.Reliable, OT.Official),
                    )
                ],
                comments="イラスト:たんたんめん",
            ),
            Medium(
                "05_FX6r9HmagAAxbOE.jpg",
                [
                    Source(
                        "https://x.com/voca_st/status/1548864562744930310",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3270.3660211470983!2d135.74787622585134!3d34.94743372283293!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x60010587a8d65d7b%3A0xc0fa6c9a0c5ce765!2sKy%C5%8Dto%20Pulse%20Plaza!5e0!3m2!1sen!2sfr!4v1781646695675!5m2!1sen!2sfr",
                description="京都府総合見本市会館 (京都パルスプラザ)",
                sources=[
                    Source(
                        "https://x.com/voca_st/status/1562042560930992129",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[
                f"VOCALOID STREET {i:02d}",
                f"ボーカロイドストリート{i:02d}",
                f"ボカスト{i:02d}",
            ],
            dates="2022.09.11",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://x.com/voca_st/status/1562042560930992129",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    "Participating circles: https://web.archive.org/web/20220814181011/http://voca-st.com/circlelist",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            # description=None,
            # comments=None,
            last_edited="2026.06.17",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = 6  # ==== vocaloid_street6 ====
    if i in active_events:
        event_name = f"vocaloid_street{i}"
        print(f"Processing {event_name} ...")

        media_ = [
            Medium(
                "06_FpZykrEacAIVuDC.jpg",
                [
                    Source(
                        "https://x.com/voca_st/status/1627614472079835136",
                        (RT.Reliable, OT.Official),
                    )
                ],
                comments="イラスト:守木涼",
            ),
            Medium(
                "06_20220924101715_top.png",
                [
                    Source(
                        "https://web.archive.org/web/20220924101715/http://voca-st.com/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "06_FcxWpYMacAEDox3.jpg",
                [
                    Source(
                        "https://x.com/voca_st/status/1570725725711511553",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d13051.9153575633!2d136.8873299!3d35.1322016!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x600379fe829a2f51%3A0x284de675a464956a!2sShirotori%20Hall!5e0!3m2!1sen!2sfr!4v1781209672065!5m2!1sen!2sfr",
                description="名古屋国際会議場 白鳥ホール",
                sources=[
                    Source(
                        "https://x.com/voca_st/status/1570725725711511553",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[
                f"VOCALOID STREET {i:02d}",
                f"ボーカロイドストリート{i:02d}",
                f"ボカスト{i:02d}",
            ],
            dates="2023.03.12",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://x.com/voca_st/status/1570725725711511553",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    "Participating circles: https://web.archive.org/web/20230204094524/https://voca-st.com/circleList",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            # description=None,
            # comments=None,
            last_edited="2026.06.17",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = 7  # ==== vocaloid_street7 ====
    if i in active_events:
        event_name = f"vocaloid_street{i}"
        print(f"Processing {event_name} ...")

        media_ = [
            Medium(
                "07_20230809163032_top_07-2.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20230809163032/https://voca-st.com/",
                        (RT.Reliable, OT.Official),
                    )
                ],
                comments="イラスト:縞城依月",
            ),
            Medium(
                "07_20230328055951_top_07-1.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20230328055951/https://voca-st.com/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3270.3700040500134!2d135.74830447585123!3d34.94733387283321!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x60010587a8d65d7b%3A0xc0fa6c9a0c5ce765!2sKy%C5%8Dto%20Pulse%20Plaza!5e0!3m2!1sen!2sfr!4v1781728312780!5m2!1sen!2sfr",
                description="京都パルスプラザ",
                sources=[
                    Source(
                        "https://web.archive.org/web/20230608222126/https://voca-st.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[
                f"VOCALOID STREET {i:02d}",
                f"ボーカロイドストリート{i:02d}",
                f"ボカスト{i:02d}",
            ],
            dates="2023.09.03",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20230608222126/https://voca-st.com/",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    "Participating circles: https://web.archive.org/web/20230312094223/https://voca-st.com/circleList",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            # description=None,
            # comments=None,
            last_edited="2026.06.17",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = 8  # ==== vocaloid_street8 ====
    if i in active_events:
        event_name = f"vocaloid_street{i}"
        print(f"Processing {event_name} ...")

        media_ = [
            Medium(
                "08_GG8hMBVawAA_IEz.jpg",
                [
                    Source(
                        "https://x.com/voca_st/status/1760663234355626035",
                        (RT.Reliable, OT.Official),
                    )
                ],
                comments="イラスト:おむ烈",
            ),
            Medium(
                "08_F7MWPO_aEAA5N6y.png",
                [
                    Source(
                        "https://x.com/voca_st/status/1707733164381401307",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "08_20231002052001_top_08-1.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20231002052001/https://voca-st.com/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d13051.9153575633!2d136.8873299!3d35.1322016!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x600379fe829a2f51%3A0x284de675a464956a!2sShirotori%20Hall!5e0!3m2!1sen!2sfr!4v1781209672065!5m2!1sen!2sfr",
                description="名古屋国際会議場 白鳥ホール",
                sources=[
                    Source(
                        "https://web.archive.org/web/20231002052001/https://voca-st.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[
                f"VOCALOID STREET {i:02d}",
                f"ボーカロイドストリート{i:02d}",
                f"ボカスト{i:02d}",
            ],
            dates="2024.03.03",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20231002052001/https://voca-st.com/",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    "Participating circles: https://web.archive.org/web/20240228123634/https://voca-st.com/circleList",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            # description=None,
            # comments=None,
            last_edited="2026.06.17",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = 9  # ==== vocaloid_street9 ====
    if i in active_events:
        event_name = f"vocaloid_street{i}"
        print(f"Processing {event_name} ...")

        media_ = [
            Medium(
                "09_20241007091042_top_09-2.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20241007091042/https://voca-st.com/events/09/",
                        (RT.Reliable, OT.Official),
                    )
                ],
                comments="イラスト:縞城依月",
            ),
            Medium(
                "09_20241007083034_logo_09.png",
                [
                    Source(
                        "https://web.archive.org/web/20241007083034/https://voca-st.com/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "09_GQRbLMMakAAdIPs.jpg",
                [
                    Source(
                        "https://x.com/voca_st/status/1802666003131965582",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "09_20240923_layout.pdf",
                [
                    Source(
                        "https://web.archive.org/web/20241109234703/https://voca-st.com/events/09/circlelist",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3267.751071069338!2d135.7783858758542!3d35.01293597281049!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x600108e5fdb0fb75%3A0x32f576fbc1dc5042!2sMiyako%20Messe%20(Kyoto%20International%20Exhibition%20Hall)!5e0!3m2!1sen!2sfr!4v1781558408737!5m2!1sen!2sfr",
                description="京都市勧業館みやこめっせ",
                sources=[
                    Source(
                        "https://web.archive.org/web/20240715124116/https://voca-st.com/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[
                f"VOCALOID STREET {i:02d}",
                f"ボーカロイドストリート{i:02d}",
                f"ボカスト{i:02d}",
            ],
            dates="2024.09.23",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20240715124116/https://voca-st.com/",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    "Participating circles: https://web.archive.org/web/20241109234703/https://voca-st.com/events/09/circlelist",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            # description=None,
            # comments=None,
            last_edited="2026.06.15",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = 10  # ==== vocaloid_street10 ====
    if i in active_events:
        event_name = f"vocaloid_street{i}"
        print(f"Processing {event_name} ...")

        media_ = [
            Medium(
                "10_Gfz2qvlbcAAp0yL.jpg",
                [
                    Source(
                        "https://x.com/voca_st/status/1872642778012041671",
                        (RT.Reliable, OT.Official),
                    )
                ],
                comments="イラスト·ロゴデザイン: GYARI",
            ),
            Medium(
                "10_Gg7ZythaEAAFF5z.jpg",
                [
                    Source(
                        "https://x.com/voca_st/status/1877678004165542064",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "10_20241007080027_top_10-1.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20241007080027/https://voca-st.com/events/10/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "10_20241007083034_logo_10.png",
                [
                    Source(
                        "https://web.archive.org/web/20241007083034/https://voca-st.com/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))])
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m14!1m8!1m3!1d13051.9153575633!2d136.8873299!3d35.1322016!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x600379fe829a2f51%3A0x284de675a464956a!2sShirotori%20Hall!5e0!3m2!1sen!2sfr!4v1781209672065!5m2!1sen!2sfr",
                description="名古屋国際会議場 白鳥ホール",
                sources=[
                    Source(
                        "https://web.archive.org/web/20250304100157/https://voca-st.com/events/10/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[
                f"VOCALOID STREET {i:02d}",
                f"ボーカロイドストリート{i:02d}",
                f"ボカスト{i:02d}",
            ],
            dates="2025.01.12",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20250304100157/https://voca-st.com/events/10/",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    "Participating circles: https://web.archive.org/web/20250215223553/https://voca-st.com/events/10/circleList",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            # description=None,
            # comments=None,
            last_edited="2026.06.17",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = 11  # ==== vocaloid_street11 ====
    if i in active_events:
        event_name = f"vocaloid_street{i}"
        print(f"Processing {event_name} ...")

        media_ = [
            Medium(
                "11_top_11-2.jpg",
                [
                    Source(
                        "",  # TODO
                        (RT.Reliable, OT.Official),
                    )
                ],
                comments="イラスト: 猫橋ねこ",
            ),
            Medium(
                "11_top_11-1.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20251108122956/https://voca-st.com/events/11/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "11_20251122_layout.pdf",
                [
                    Source(
                        "https://voca-st.com/events/11/circleList",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3267.751071069338!2d135.7783858758542!3d35.01293597281049!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x600108e5fdb0fb75%3A0x32f576fbc1dc5042!2sMiyako%20Messe%20(Kyoto%20International%20Exhibition%20Hall)!5e0!3m2!1sen!2sfr!4v1781558408737!5m2!1sen!2sfr",
                description="京都市勧業館みやこめっせ",
                sources=[
                    Source(
                        "",  # TODO
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[
                f"VOCALOID STREET {i:02d}",
                f"ボーカロイドストリート{i:02d}",
                f"ボカスト{i:02d}",
            ],
            dates="2025.11.22",
            circles=[],
            media=media_,
            sources=[
                Source("Date: ", (RT.Reliable, OT.Official)),
                Source(
                    "Participating circles: https://voca-st.com/events/11/circleList",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            # description=None,
            # comments=None,
            last_edited="2026.06.19",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    n = "sendai"  # ==== vocaloid_streetsendai ====
    if n in active_events:
        event_name = f"vocaloid_street{n}"
        print(f"Processing {event_name} ...")

        media_ = [
            Medium(
                "sendai_Gt4QohkXYAAhi5-.jpg",
                [
                    Source(
                        "https://x.com/voca_st/status/1936003520584728979",
                        (RT.Reliable, OT.Official),
                    )
                ],
                comments="イラスト: 守木涼",
            ),
            Medium(
                "sendai_top_sendai.png",
                [
                    Source(
                        "https://web.archive.org/web/20250422054140/https://voca-st.com/events/sendai/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "sendai_20250314073352_logo_640x224_sendai.png",
                [
                    Source(
                        "https://web.archive.org/web/20250314073352/https://voca-st.com/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d327610.7480136059!2d140.85146171062968!3d38.2582700560318!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x5f8988bab8926a4d%3A0xd0418f9f93c216c7!2sMiyagi%20Industrial%20Exchange%20Center%20-%20Yume%20Messe%20Miyagi!5e0!3m2!1sen!2sfr!4v1781902929343!5m2!1sen!2sfr",
                description="みやぎ産業交流センター (萝メッセみやぎ 西館ホール)",
                sources=[
                    Source(
                        "Venue: https://web.archive.org/web/20250422054140/https://voca-st.com/events/sendai/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    ),
                    Source(
                        "Hall: https://web.archive.org/web/20250720054402/https://voca-st.com/events/sendai/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    ),
                ],
            ),
        ]
        event = Event(
            aliases=[
                f"VOCALOID STREET {i:02d}",
                f"ボーカロイドストリート{i:02d}",
                f"ボカスト{i:02d}",
            ],
            dates="2025.06.22",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20250422054140/https://voca-st.com/events/sendai/",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    "Participating circles: https://web.archive.org/web/20250621231429/https://voca-st.com/events/sendai/circleList",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            # description=None,
            # comments=None,
            last_edited="2026.06.19",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    i = 12  # ==== vocaloid_street12 ====
    if i in active_events:
        event_name = f"vocaloid_street{i}"
        print(f"Processing {event_name} ...")

        media_ = [
            Medium(
                "12_top_12-3.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20260410162347/https://voca-st.com/events/12/",
                        (RT.Reliable, OT.Official),
                    )
                ],
                comments="イラスト: saki",
            ),
            Medium(
                "12_top_12-2.jpg",
                [
                    Source(
                        "https://web.archive.org/web/20251011044654/https://voca-st.com/events/12/",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            Medium(
                "12_20260216_layout.pdf",
                [
                    Source(
                        "https://voca-st.com/events/12/circleList",
                        (RT.Reliable, OT.Official),
                    )
                ],
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3254.866190194564!2d137.1268545758678!3d35.33414417270119!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x60036a70848ce44f%3A0xaea80b3888b9c8db!2sSangyobunka%20Center!5e0!3m2!1sen!2sfr!4v1781903916732!5m2!1sen!2sfr",
                description="多治見市産業文化センター ",
                sources=[
                    Source(
                        "https://web.archive.org/web/20260410162347/https://voca-st.com/events/12/",
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    )
                ],
            ),
        ]
        event = Event(
            aliases=[
                f"VOCALOID STREET {i:02d}",
                f"ボーカロイドストリート{i:02d}",
                f"ボカスト{i:02d}",
            ],
            dates="2026.02.15",
            circles=[],
            media=media_,
            sources=[
                Source(
                    "Date: https://web.archive.org/web/20260410162347/https://voca-st.com/events/12/",
                    (RT.Reliable, OT.Official),
                ),
                Source(
                    "Participating circles: https://voca-st.com/events/12/circleList",
                    (RT.Reliable, OT.Official),
                ),
            ],
            locations=locations,
            # description=None,
            # comments=None,
            last_edited="2026.06.19",
        )

        # Retrieve circles
        event.circles = retrieve_circles(event_name)
        events.append(event)

    n = "sendai2"  # ==== vocaloid_streetsendai2 ====
    if n in active_events:
        event_name = f"vocaloid_street{n}"
        print(f"Processing {event_name} ...")

        media_ = [
            Medium(
                "sendai2_sendai_02_a.jpg",
                [Source("", (RT.Reliable, OT.Official))],  # TODO
                comments="イラスト: あすらて",
            ),
            # Medium("", [Source("", (RT.Reliable, OT.Official))]),
        ]
        locations = [
            Location(
                iframe_url="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d327610.7480136059!2d140.85146171062968!3d38.2582700560318!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x5f8988bab8926a4d%3A0xd0418f9f93c216c7!2sMiyagi%20Industrial%20Exchange%20Center%20-%20Yume%20Messe%20Miyagi!5e0!3m2!1sen!2sfr!4v1781902929343!5m2!1sen!2sfr",
                description="みやぎ産業交流センター(夢メッセみやぎ)",
                sources=[
                    Source(
                        "",  # TODO
                        (ReliabilityTypes.Reliable, OriginTypes.Official),
                    ),
                ],
            ),
        ]
        event = Event(
            aliases=[
                f"VOCALOID STREET {i:02d}",
                f"ボーカロイドストリート{i:02d}",
                f"ボカスト{i:02d}",
            ],
            dates="2026.07.12",
            circles=[],
            media=media_,
            sources=[
                Source("Date: ", (RT.Reliable, OT.Official)),  # TODO
                # Source("Participating circles: ", (RT.Reliable, OT.Official)),
            ],
            locations=locations,
            # description=None,
            # comments=None,
            last_edited="2026.06.19",
        )

        # Retrieve circles
        # event.circles = retrieve_circles(event_name)
        events.append(event)

    # ==== event group ====
    media = [
        # Medium("", [Source("", (RT.Reliable, OT.Official))]),
    ]
    links = ["http://voca-st.com/", "https://x.com/voca_st"]

    event_group = EventGroup(
        aliases=["VOCALOID STREET", "ボーカロイドストリート", "ボカスト"],
        events=events,
        media=media,
        links=links,
        sources=[
            # Source(
            #     "",
            #     (ReliabilityTypes.Reliable, OriginTypes.Official),
            # ),
        ],
        comments=None,
        description=None,
        last_edited="2026.06.19",
    )

    print(f"Saving {Path(__file__).stem} database...")
    event_group.save(PATH_EVENT_GROUP, indent=None)
    print("Done")

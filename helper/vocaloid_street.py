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
    active_events: list[int | str] = list(range(1, 12)) + ["tajimi"]

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

    n = "tajimi"  # ==== vocaloid_street2 ====
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

    # i =   # ==== vocaloid_street ====
    # if i in active_events:
    #     event_name = f"vocaloid_street{i}"
    #     print(f"Processing {event_name} ...")

    #     media_ = [
    #         # Medium("", [Source("", (RT.Reliable, OT.Official))]),
    #         # Medium("", [Source("", (RT.Reliable, OT.Official))]),
    #     ]
    #     locations = [
    #         # Location(
    #         #     iframe_url="",
    #         #     description="",
    #         #     sources=[
    #         #         Source(
    #         #             "",
    #         #             (ReliabilityTypes.Reliable, OriginTypes.Official),
    #         #         )
    #         #     ],
    #         # ),
    #     ]
    #     event = Event(
    #         aliases=[
    #             f"VOCALOID STREET {i:02d}",
    #             f"ボーカロイドストリート{i:02d}",
    #             f"ボカスト{i:02d}",
    #         ],
    #         dates="",
    #         circles=[],
    #         media=media_,
    #         sources=[
    #             # Source("Date: ", (RT.Reliable, OT.Official)),
    #             # Source("Participating circles: ", (RT.Reliable, OT.Official)),
    #         ],
    #         locations=locations,
    #         # description=None,
    #         # comments=None,
    #         last_edited="2026.06.15",
    #     )

    #     # Retrieve circles
    #     # event.circles = retrieve_circles(event_name)
    #     events.append(event)

    # i =   # ==== vocaloid_street ====
    # if i in active_events:
    #     event_name = f"vocaloid_street{i}"
    #     print(f"Processing {event_name} ...")

    #     media_ = [
    #         # Medium("", [Source("", (RT.Reliable, OT.Official))]),
    #         # Medium("", [Source("", (RT.Reliable, OT.Official))]),
    #     ]
    #     locations = [
    #         # Location(
    #         #     iframe_url="",
    #         #     description="",
    #         #     sources=[
    #         #         Source(
    #         #             "",
    #         #             (ReliabilityTypes.Reliable, OriginTypes.Official),
    #         #         )
    #         #     ],
    #         # ),
    #     ]
    #     event = Event(
    #         aliases=[
    #             f"VOCALOID STREET {i:02d}",
    #             f"ボーカロイドストリート{i:02d}",
    #             f"ボカスト{i:02d}",
    #         ],
    #         dates="",
    #         circles=[],
    #         media=media_,
    #         sources=[
    #             # Source("Date: ", (RT.Reliable, OT.Official)),
    #             # Source("Participating circles: ", (RT.Reliable, OT.Official)),
    #         ],
    #         locations=locations,
    #         # description=None,
    #         # comments=None,
    #         last_edited="2026.06.15",
    #     )

    #     # Retrieve circles
    #     # event.circles = retrieve_circles(event_name)
    #     events.append(event)

    # ==== event group ====
    media = [
        # Medium("",
        #        [Source("", (RT.Reliable, OT.Official))]),
        # Medium("",
        #        [Source("", (RT.Reliable, OT.Official))]),
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
        last_edited="2026.06.15",
    )

    print(f"Saving {Path(__file__).stem} database...")
    event_group.save(PATH_EVENT_GROUP, indent=None)
    print("Done")

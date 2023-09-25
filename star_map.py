import dataclasses
import logging
import math
import pathlib
import typing

import PIL.Image
import PIL.ImageDraw

import tycho2

dirname = pathlib.Path(__file__).resolve().parent


@dataclasses.dataclass
class Collection:
    stars: list[tuple[typing.Any]]
    color: str
    size: float

    @classmethod
    def from_magnitude_range(
        cls,
        database: tycho2.Database,
        minimum_magnitude: float | None,
        maximum_magnitude: float,
        color: str,
        size: float,
    ):
        return cls(
            stars=database.find(
                minimum_magnitude=minimum_magnitude, maximum_magnitude=maximum_magnitude
            ),
            color=color,
            size=size,
        )


def generate_pages(
    cylinder_circumference_meters: float,
    paper_width_meters: float,
    paper_height_meters: float,
    paper_margin_meters: float,
    pixels_per_meter: float,
    output_directory: pathlib.Path,
    collections: list[Collection],
):
    ceili = lambda value: int(math.ceil(value))
    roundi = lambda value: int(round(value))
    output_directory.mkdir(exist_ok=True)
    paper_effective_width = paper_width_meters - paper_margin_meters * 2.0
    pages_count = ceili(cylinder_circumference_meters / paper_effective_width)
    scale = 2.0 * math.pi / cylinder_circumference_meters
    paper_effective_half_height = paper_height_meters / 2 - paper_margin_meters
    dec_maximum = (
        2.0
        * math.atan(math.exp(paper_effective_half_height * scale))
        * (180.0 / math.pi)
        - 90.0
    )
    for index in range(0, pages_count):
        image = PIL.Image.new(
            mode="RGB",
            size=(
                roundi(paper_width_meters * pixels_per_meter),
                roundi(paper_height_meters * pixels_per_meter),
            ),
            color="#CCCCCC",
        )
        draw = PIL.ImageDraw.Draw(image)
        if index == pages_count - 1:
            draw.rectangle(
                xy=(
                    roundi(
                        (
                            paper_margin_meters
                            + (
                                pages_count * paper_effective_width
                                - cylinder_circumference_meters
                            )
                        )
                        * pixels_per_meter
                    ),
                    roundi(paper_margin_meters * pixels_per_meter),
                    roundi(
                        (paper_width_meters - paper_margin_meters) * pixels_per_meter
                    ),
                    roundi(
                        (paper_height_meters - paper_margin_meters) * pixels_per_meter
                    ),
                ),
                fill="#FFFFFF",
            )
        else:
            draw.rectangle(
                xy=(
                    roundi(paper_margin_meters * pixels_per_meter),
                    roundi(paper_margin_meters * pixels_per_meter),
                    roundi(
                        (paper_width_meters - paper_margin_meters) * pixels_per_meter
                    ),
                    roundi(
                        (paper_height_meters - paper_margin_meters) * pixels_per_meter
                    ),
                ),
                fill="#FFFFFF",
            )
        physical_left = index * paper_effective_width
        physical_right = (index + 1) * paper_effective_width
        ra_minimum = physical_left / cylinder_circumference_meters * 360.0
        ra_maximum = physical_right / cylinder_circumference_meters * 360.0
        for collection in collections:
            print(ra_minimum, ra_maximum)
            radius_pixels = roundi(collection.size / 2.0 * pixels_per_meter)
            for star in collection.stars:
                ra = star[tycho2.Database.right_ascension]
                dec = star[tycho2.Database.declination]
                if all(
                    (
                        ra >= ra_minimum,
                        ra <= ra_maximum,
                        abs(dec) <= dec_maximum,
                    )
                ):
                    x = roundi(
                        (
                            paper_width_meters
                            - (
                                (ra - ra_minimum)
                                / 360.0
                                * cylinder_circumference_meters
                                + paper_margin_meters
                            )
                        )
                        * pixels_per_meter
                    )
                    y = roundi(
                        (
                            paper_height_meters
                            - (
                                math.log(math.tan((dec + 90) * (math.pi / 180) / 2))
                                / scale
                                + paper_margin_meters
                                + paper_effective_half_height
                            )
                        )
                        * pixels_per_meter
                    )
                    draw.ellipse(
                        xy=(
                            x - radius_pixels,
                            y - radius_pixels,
                            x + radius_pixels,
                            y + radius_pixels,
                        ),
                        fill=collection.color,
                    )
        image.save(str(output_directory / f"{index}.png"))


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.INFO)
    database = tycho2.Database()
    generate_pages(
        cylinder_circumference_meters=0.91,
        paper_width_meters=0.2025,
        paper_height_meters=0.285,
        paper_margin_meters=0.025,
        pixels_per_meter=300.0 * 39.3701,
        output_directory=dirname / "star_map",
        collections=[
            Collection.from_magnitude_range(
                database, None, 2.0, "#5790FC", 5.0 / 1000.0
            ),
            Collection.from_magnitude_range(
                database, 2.0, 3.0, "#F89C20", 3.0 / 1000.0
            ),
            Collection.from_magnitude_range(
                database, 3.0, 4.0, "#964A8B", 2.0 / 1000.0
            ),
        ],
    )

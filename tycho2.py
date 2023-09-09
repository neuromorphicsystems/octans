import pathlib
import re
import sqlite3
import typing

dirname = pathlib.Path(__file__).resolve().parent


class Database:
    create_table_pattern = re.compile(r"CREATE TABLE (\w+) \((.+)\)")
    tyc_pattern = re.compile(r"^TYC (\d{1,4})-(\d{1,5})-(\d)$")
    tyc_identifier = 0
    right_ascension = 1
    declination = 2
    right_ascension_dot = 3
    declination_dot = 4
    magnitude = 5
    iau_name = 6
    iau_designation = 7
    iau_bayer_designation = 8
    iau_system_position = 9

    def __init__(self, path: pathlib.Path = dirname / "tycho2_m6.db"):
        self.path = str(path)

    def find(
        self,
        minimum_magnitude: float | None,
        maximum_magnitude: float,
    ) -> list[tuple[typing.Any]]:
        with sqlite3.connect(self.path) as connection:
            cursor = connection.cursor()
            cursor.execute(
                " ".join(
                    (
                        "SELECT * FROM catalogue",
                        f"WHERE magnitude < {maximum_magnitude}",
                        *(
                            ()
                            if minimum_magnitude is None
                            else (f"AND magnitude >= {minimum_magnitude}",)
                        ),
                    )
                )
            )
            return cursor.fetchall()

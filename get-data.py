# Scrape reconstructions from reco.nz
# checks for 3x3 category, and for a correct solution

import json
import re
from enum import StrEnum

import requests
from rubik.cube import Cube
from bs4 import BeautifulSoup
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
from rich.console import Console
from rich.progress import track


SOLVED_CUBE_STR = "OOOOOOOOOYYYWWWGGGBBBYYYWWWGGGBBBYYYWWWGGGBBBRRRRRRRRR"
MOVE_PATTERN = re.compile(r"[xyzULFRBDMESulfrbd]2?'?")
URL = "https://reco.nz/solve/{}"
END_ID = 12113
START_ID = 3


class Move(StrEnum):
    # Face Rotations
    Left = "L"
    Left2 = "L2"
    InvLeft = "L'"
    InvLeft2 = "L2'"
    Right = "R"
    Right2 = "R2"
    InvRight = "R'"
    InvRight2 = "R2'"
    Upper = "U"
    Upper2 = "U2"
    InvUpper = "U'"
    InvUpper2 = "U2'"
    Down = "D"
    Down2 = "D2"
    InvDown = "D'"
    InvDown2 = "D2'"
    Front = "F"
    Front2 = "F2"
    InvFront = "F'"
    InvFront2 = "F2'"
    Back = "B"
    Back2 = "B2"
    InvBack = "B'"
    InvBack2 = "B2'"

    # Slice Rotations
    Middle = "M"
    Middle2 = "M2"
    InvMiddle = "M'"
    InvMiddle2 = "M2'"
    Equator = "E"
    Equator2 = "E2"
    InvEquator = "E'"
    InvEquator2 = "E2'"
    Standing = "S"
    Standing2 = "S2"
    InvStanding = "S'"
    InvStanding2 = "S2'"

    # Cube Rotations
    X = "X"
    X2 = "X2"
    InvX = "X'"
    InvX2 = "X2'"
    Y = "Y"
    Y2 = "Y2"
    InvY = "Y'"
    InvY2 = "Y2'"
    Z = "Z"
    Z2 = "Z2"
    InvZ = "Z'"
    InvZ2 = "Z2'"

    # Advanced Stuff - Double Layer Moves
    ## NOTE: The rubik-cube package doesn't support these directly,
    ##       but they can be done using a combination of other moves
    DoubleFront = "f"
    DoubleFront2 = "f2"
    InvDoubleFront = "f'"
    InvDoubleFront2 = "f2'"
    DoubleRight = "r"
    DoubleRight2 = "r2"
    InvDoubleRight = "r'"
    InvDoubleRight2 = "r2'"
    DoubleUpper = "u"
    DoubleUpper2 = "u2"
    InvDoubleUpper = "u'"
    InvDoubleUpper2 = "u2'"
    DoubleLeft = "l"
    DoubleLeft2 = "l2"
    InvDoubleLeft = "l'"
    InvDoubleLeft2 = "l2'"
    DoubleBack = "b"
    DoubleBack2 = "b2"
    InvDoubleBack = "b'"
    InvDoubleBack2 = "b2'"
    DoubleDown = "d"
    DoubleDown2 = "d2"
    InvDoubleDown = "d'"
    InvDoubleDown2 = "d2'"

    def to_str(self) -> str:
        match self:
            case (
                Move.Left
                | Move.Right
                | Move.Upper
                | Move.Down
                | Move.Front
                | Move.Back
                | Move.Middle
                | Move.Standing
                | Move.Equator
                | Move.X
                | Move.Y
                | Move.Z
            ):
                return str(self)

            case (
                Move.InvLeft
                | Move.InvRight
                | Move.InvUpper
                | Move.InvDown
                | Move.InvFront
                | Move.InvBack
                | Move.InvMiddle
                | Move.InvStanding
                | Move.InvEquator
                | Move.InvX
                | Move.InvY
                | Move.InvZ
            ):
                move = str(self).replace("'", "i")
                return move
            case (
                Move.Left2
                | Move.Right2
                | Move.Upper2
                | Move.Down2
                | Move.Front2
                | Move.Back2
                | Move.Middle2
                | Move.Standing2
                | Move.Equator2
                | Move.X2
                | Move.Y2
                | Move.Z2
                | Move.InvLeft2
                | Move.InvRight2
                | Move.InvUpper2
                | Move.InvDown2
                | Move.InvFront2
                | Move.InvBack2
                | Move.InvMiddle2
                | Move.InvStanding2
                | Move.InvEquator2
                | Move.InvX2
                | Move.InvY2
                | Move.InvZ2
            ):
                move = str(self).replace("2", "").replace("'", "i")
                return f"{move} {move}"
            case Move.DoubleFront:
                return f"{Move.Front.to_str()} {Move.Standing.to_str()}"
            case Move.DoubleBack:
                return f"{Move.Back.to_str()} {Move.InvStanding.to_str()}"
            case Move.DoubleUpper:
                return f"{Move.Upper.to_str()} {Move.InvEquator.to_str()}"
            case Move.DoubleDown:
                return f"{Move.Down.to_str()} {Move.Equator.to_str()}"
            case Move.DoubleRight:
                return f"{Move.Right.to_str()} {Move.InvMiddle.to_str()}"
            case Move.DoubleLeft:
                return f"{Move.Left.to_str()} {Move.Middle.to_str()}"
            case Move.InvDoubleFront:
                return f"{Move.InvFront.to_str()} {Move.InvStanding.to_str()}"
            case Move.InvDoubleBack:
                return f"{Move.InvBack.to_str()} {Move.Standing.to_str()}"
            case Move.InvDoubleUpper:
                return f"{Move.InvUpper.to_str()} {Move.Equator.to_str()}"
            case Move.InvDoubleDown:
                return f"{Move.InvDown.to_str()} {Move.InvEquator.to_str()}"
            case Move.InvDoubleRight:
                return f"{Move.InvRight.to_str()} {Move.Middle.to_str()}"
            case Move.InvDoubleLeft:
                return f"{Move.InvLeft.to_str()} {Move.InvMiddle.to_str()}"
            case Move.DoubleFront2:
                return f"{Move.Front2.to_str()} {Move.Standing2.to_str()}"
            case Move.DoubleBack2:
                return f"{Move.Back2.to_str()} {Move.InvStanding2.to_str()}"
            case Move.DoubleUpper2:
                return f"{Move.Upper2.to_str()} {Move.InvEquator2.to_str()}"
            case Move.DoubleDown2:
                return f"{Move.Down2.to_str()} {Move.Equator2.to_str()}"
            case Move.DoubleRight2:
                return f"{Move.Right2.to_str()} {Move.InvMiddle2.to_str()}"
            case Move.DoubleLeft2:
                return f"{Move.Left2.to_str()} {Move.Middle2.to_str()}"
            case Move.InvDoubleFront2:
                return f"{Move.InvFront2.to_str()} {Move.InvStanding2.to_str()}"
            case Move.InvDoubleBack2:
                return f"{Move.InvBack2.to_str()} {Move.Standing2.to_str()}"
            case Move.InvDoubleUpper2:
                return f"{Move.InvUpper2.to_str()} {Move.Equator2.to_str()}"
            case Move.InvDoubleDown2:
                return f"{Move.InvDown2.to_str()} {Move.InvEquator2.to_str()}"
            case Move.InvDoubleRight2:
                return f"{Move.InvRight2.to_str()} {Move.Middle2.to_str()}"
            case Move.InvDoubleLeft2:
                return f"{Move.InvLeft2.to_str()} {Move.InvMiddle2.to_str()}"
            case _:
                raise Exception(f"Move {self} not covered by `move.to_str()`")


class MoveSequence:
    def __init__(self, moves):
        moves = MOVE_PATTERN.findall(moves)
        self.moves = []

        for move in moves:
            if "x" in move or "y" in move or "z" in move:
                move = move.upper()
            self.moves.append(Move(move))

    def __str__(self):
        return " ".join([move.to_str() for move in self.moves])

    def __iter__(self):
        for move in self.moves:
            yield move


class Reconstruction:
    def __init__(self, url: str, scramble: MoveSequence, solve: MoveSequence):
        self.url = url
        self.scramble = scramble
        self.solve = solve

    def is_valid(self):
        cube = cube_from_scramble(str(self.scramble))
        cube.sequence(str(self.solve))
        return cube.is_solved()

    def to_dict(self):
        return {
            "url": self.url,
            "scramble": [str(move) for move in self.scramble],
            "solve": [str(move) for move in self.solve],
        }


def cube_from_scramble(scramble: str):
    c = Cube(SOLVED_CUBE_STR)
    c.sequence(scramble)
    return c


def scrape(id: int):
    current_url = URL.format(id)
    res = requests.get(
        current_url, headers={"User-Agent": ua_rotator.get_random_user_agent()}
    )
    soup = BeautifulSoup(res.content, features="html.parser")
    title = soup.find("h1").text

    if "3x3" not in title:
        raise Exception("Reconstruction is not a 3x3 solve")

    reconstruction = soup.find(id="reconstruction").text
    lines = [
        line.lstrip() for line in reconstruction.splitlines() if len(line.lstrip()) > 0
    ]
    scramble = lines[0]
    solve = "".join([re.sub(r"//.+", "", line) for line in lines[1:]])

    solve = MoveSequence(solve)
    scramble = MoveSequence(scramble)
    reconstruction = Reconstruction(current_url, scramble, solve)

    if not reconstruction.is_valid():
        raise Exception("Solution does not produce a solved cube")

    return reconstruction


if __name__ == "__main__":
    console = Console()
    ua_rotator = UserAgent(
        software_names=[SoftwareName.CHROME.value, SoftwareName.FIREFOX.value],
        operating_systems=[
            OperatingSystem.WINDOWS.value,
            OperatingSystem.LINUX.value,
            OperatingSystem.MACOS.value,
        ],
        limit=1000,
    )
    reconstructions = []

    try:
        for id in track(range(START_ID, END_ID), console=console):
            try:
                r = scrape(id)
                reconstructions.append(r)
            except Exception as e:
                console.log(f"Error processing item {id}: {e}")
    finally:
        with open("solves.json", "w") as file:
            json.dump([r.to_dict() for r in reconstructions], file)

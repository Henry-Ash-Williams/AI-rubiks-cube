import random
import re
from enum import StrEnum

from rubik.cube import Cube
from typing import Union

SOLVED_CUBE_STR = "OOOOOOOOOYYYWWWGGGBBBYYYWWWGGGBBBYYYWWWGGGBBBRRRRRRRRR"
MOVE_PATTERN = re.compile(r"[xyzXYZULFRBDMESulfrbd]2?'?")


def cube_from_scramble(scramble: str):
    c = Cube(SOLVED_CUBE_STR)
    c.sequence(scramble)
    return c


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

    @classmethod
    def random_sequence(cls: "MoveSequence", n_moves: int = 20) -> "MoveSequence":
        # Generate a random sequence of moves

        # TODO: Post-process this sequence so that a move followed by its
        # inverse are removed?

        invalid_moves = [
            Move.X,
            Move.X2,
            Move.InvX,
            Move.InvX2,
            Move.Y,
            Move.Y2,
            Move.InvY,
            Move.InvY2,
            Move.Z,
            Move.Z2,
            Move.InvZ,
            Move.InvZ2,
        ]
        seq = []
        while len(seq) < n_moves:
            random_move = random.choice(list(Move))

            if random_move not in invalid_moves:
                seq.append(random_move)

        new_seq = cls(moves="")
        new_seq.moves = seq
        return new_seq


class Reconstruction:
    def __init__(
        self,
        url: str,
        scramble: Union[MoveSequence, str],
        solve: Union[MoveSequence, str],
    ):
        self.url = url
        self.scramble = (
            scramble if isinstance(scramble, MoveSequence) else MoveSequence(scramble)
        )
        self.solve = solve if isinstance(solve, MoveSequence) else MoveSequence(solve)

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

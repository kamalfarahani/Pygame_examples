from typing import NamedTuple, List


class BaseTile(NamedTuple):
    x: int
    y: int

class TileOne(BaseTile):
    pass

class TileTwo(BaseTile):
    pass

class TileThree(BaseTile):
    pass

class TileFour(BaseTile):
    pass

class TileFive(BaseTile):
    pass


TileMap = List[BaseTile]
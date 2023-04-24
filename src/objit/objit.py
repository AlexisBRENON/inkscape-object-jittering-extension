import argparse
import functools
import math
import typing

import inkex

import constructors

def embed(v: float, n: int = 100) -> inkex.transforms.ImmutableVector2d:
    return inkex.transforms.ImmutableVector2d(
        -(math.cos(v * n * 2 * math.pi) - 1) / 2, v
    )


SEQUENCE_CONTRUCTORS = {
    f.__name__: f for f in (
        constructors.correlation,
        constructors.additive_recurrence,
        constructors.additive_recurrence2,
        constructors.vdc,
        constructors.sobol
    )
}

class Objit(inkex.EffectExtension):
    def add_arguments(self, pars: argparse.ArgumentParser):
        pars.add_argument(
            "--objit_notebook",
        )
        pars.add_argument(
            "--constructor", default="correlation", choices=SEQUENCE_CONTRUCTORS.keys()
        )

    def effect(self):
        selection_bb = functools.reduce(
            inkex.transforms.BoundingBox.__add__,
            (
                ebb
                for e in self.svg.selection
                if (
                    isinstance(e, inkex.elements.ShapeElement)
                    and (ebb := e.bounding_box()) is not None
                )
            ),
            inkex.transforms.BoundingBox()
        )

        coords = [embed(x) for x in SEQUENCE_CONTRUCTORS[self.options.constructor](len(self.svg.selection))]
        for coord, e in zip(
            coords,
            typing.cast(
                typing.Iterable[inkex.elements.BaseElement], self.svg.selection
            ),
        ):
            tr = typing.cast(inkex.transforms.Transform, e.transform)
            matrix = (
                (tr.a, tr.b, coord.x),
                (tr.d, tr.e, coord.y)
            )
            e.transform = inkex.transforms.Transform(matrix)

        return True


if __name__ == "__main__":
    Objit().run()

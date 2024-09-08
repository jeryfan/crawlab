from inspect import isgenerator, isasyncgen
from crawlab.exceptions import TransformTypeError


async def transform(outputs):
    if isgenerator(outputs):
        for output in outputs:
            yield output
    elif isasyncgen(outputs):
        async for output in outputs:
            yield output
    else:
        raise TransformTypeError()

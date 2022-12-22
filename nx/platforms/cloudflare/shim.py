# TODO: Get rid of direct Reference usage
from nx.runtime import Reference, entrypoint

from .runtime import Request, Response, ScheduledEvent


@entrypoint
async def fetch(request: Request, env: Reference, ctx: Reference) -> Response:
    # TODO: Routing via nx.framework
    raise NotImplementedError


@entrypoint
async def scheduled(event: ScheduledEvent, env: Reference, ctx: Reference) -> None:
    raise NotImplementedError


@entrypoint
async def email(message: Reference, env: Reference, ctx: Reference) -> None:
    raise NotImplementedError

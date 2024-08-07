from dotenv import load_dotenv
from dependency_injector.wiring import inject, Provide
from provider.container import Container
from provider.api.api_handler import APIHandler


@inject
def main(api_handler: APIHandler = Provide[Container.api_handler]):
    return api_handler.app


if __name__ == "__main":
    load_dotenv()
    container = Container()
    container.init_resources()
    container.wire(modules=[__name__])
    app = main()

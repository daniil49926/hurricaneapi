from typing import Optional

from hurricaneapi.dependencies import DependenceProtocol


def resolve_dependence(app_object, object_name: str) -> Optional[DependenceProtocol]:
    try:
        return app_object.get_dependencies_as_dict().get(object_name, None)
    except AttributeError as error:
        raise RuntimeError(
             'Var app_object must be a reference to the main object of the HurricaneApi class'
         ) from error

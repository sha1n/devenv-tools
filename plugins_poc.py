from inspector.api.context import Context
from inspector.api.collector import Collector
from inspector.api.executor import Executor
from inspector.api.reactor import Reactor
from inspector.api.validator import Validator

import importlib
import pkgutil

import plugins


def iter_namespace(ns_pkg):
    return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")


def discover_plugins():
    return {
        name: importlib.import_module(name)
        for finder, name, ispkg
        in iter_namespace(plugins)
    }


def register_plugins(ctx: Context):
    info = ctx.logger.info
    registry = ctx.registry
    discovered_plugins = discover_plugins()
    plugin_modules = (discovered_plugins[plugin_name] for plugin_name in discovered_plugins.keys())

    for module in plugin_modules:
        comp_id = module.component_id()
        for instance in module.objects(ctx):
            if Collector in instance.__class__.__bases__:
                info("Registering Collector plugin {} for component {}".format(instance, comp_id))
                registry.register_collector(comp_id, instance)
            if Validator in instance.__class__.__bases__:
                info("Registering Validator plugin {} for component {}".format(instance, comp_id))
                registry.register_validator(comp_id, instance)
            if Reactor in instance.__class__.__bases__:
                info("Registering Reactor plugin {} for component {}".format(instance, comp_id))
                registry.register_reactor(comp_id, instance)


def main():
    ctx = Context(name="poc")
    executor = Executor()
    register_plugins(ctx)

    ctx.logger.info("Executing...")
    executor.execute(ctx)
    ctx.logger.success("Done!")


if __name__ == '__main__':
    main()

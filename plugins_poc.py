from inspector.commons.context import Context
from inspector.collectors.basecollector import Collector
from inspector.executor import Executor
from inspector.reactors.basereactor import Reactor
from inspector.validators.basevalidator import Validator

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


def register_plugins(executor: Executor, ctx: Context):
    info = ctx.logger.info
    discovered_plugins = discover_plugins()
    plugin_modules = (discovered_plugins[plugin_name] for plugin_name in discovered_plugins.keys())

    for module in plugin_modules:
        comp_id = module.component_id()
        for instance in module.objects(ctx):
            if Collector in instance.__class__.__bases__:
                info("Registering Collector plugin {} for component {}".format(instance, comp_id))
                executor.register_collector(comp_id, instance)
            if Validator in instance.__class__.__bases__:
                info("Registering Validator plugin {} for component {}".format(instance, comp_id))
                executor.register_validator(comp_id, instance)
            if Reactor in instance.__class__.__bases__:
                info("Registering Reactor plugin {} for component {}".format(instance, comp_id))
                executor.register_reactor(comp_id, instance)


def main():
    ctx = Context(name="poc")
    executor = Executor()
    register_plugins(executor, ctx)

    ctx.logger.info("Executing...")
    executor.execute(ctx)
    ctx.logger.success("Done!")


if __name__ == '__main__':
    main()

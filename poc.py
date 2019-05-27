from inspector.api.context import Context
from inspector.collectors.bazel import BazelInfoCollector, SemVer
from inspector.validators.bazel import BazelInfoValidator
from inspector.reactors.bazel import BazelValidationLogReactor, BazelValidationInstallReactor
from inspector.api.executor import Executor


def main():
    ctx = Context(name="poc")
    registry = ctx.registry

    bazel_id = "bazel"
    bazel_log_reactor = BazelValidationLogReactor(ctx=ctx)

    registry.register_collector(bazel_id, BazelInfoCollector(ctx))
    registry.register_validator(bazel_id, BazelInfoValidator(expected_ver=SemVer("0", "23", "0"), ctx=ctx))
    registry.register_reactor(bazel_id, bazel_log_reactor)

    ctx.logger.info("*** Executing inspection flow ***")
    executor = Executor()
    executor.execute(ctx)

    print("\n")

    registry.register_reactor(bazel_id, BazelValidationInstallReactor(ctx=ctx))
    ctx.logger.info("*** Executing installation dry run flow ***")
    executor.execute(ctx)


if __name__ == '__main__':
    main()

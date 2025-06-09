from pants.backend.python.target_types import PythonRequirementModulesField, PythonRequirementResolveField, PythonRequirementsField, PythonRequirementTarget
from pants.engine.rules import collect_rules, rule
from pants.engine.target import COMMON_TARGET_FIELDS, BoolField, GeneratedTargets, GenerateTargetsRequest, TargetGenerator
from pants.engine.unions import UnionMembership, UnionRule
from pants.util.strutil import help_text
from pants.version import MAJOR_MINOR, PANTS_SEMVER

class PantsRequirementsTestutilField(BoolField):
    alias = 'testutil'
    default = True
    help = 'If true, include `pantsbuild.pants.testutil` to write tests for your plugin.'

class PantsRequirementsTargetGenerator(TargetGenerator):
    alias = 'pants_requirements'
    help = help_text(f"\n        Generate `python_requirement` targets for Pants itself to use with Pants plugins.\n\n        This is useful when writing plugins so that you can build and test your\n        plugin using Pants. The generated targets will have the correct version based on the\n        `version` in your `pants.toml`, and they will work with dependency inference.\n\n        Because the Plugin API is not yet stable, the version is set automatically for you\n        to improve stability. If you're currently using a dev release, the version will be set to\n        that exact dev release. If you're using an alpha release, release candidate (rc), or stable\n        release, the version will allow any non-dev-release release within the release series, e.g.\n        `>={MAJOR_MINOR}.0rc0,<{PANTS_SEMVER.major}.{PANTS_SEMVER.minor + 1}`.\n\n        (If this versioning scheme does not work for you, you can directly create\n        `python_requirement` targets for `pantsbuild.pants` and `pantsbuild.pants.testutil`. We\n        also invite you to share your ideas at\n        https://github.com/pantsbuild/pants/issues/new/choose)\n        ")
    generated_target_cls = PythonRequirementTarget
    core_fields = (*COMMON_TARGET_FIELDS, PantsRequirementsTestutilField)
    copied_fields = COMMON_TARGET_FIELDS
    moved_fields = (PythonRequirementResolveField,)

class GenerateFromPantsRequirementsRequest(GenerateTargetsRequest):
    generate_from = PantsRequirementsTargetGenerator

def determine_version() -> str:
    return f'=={PANTS_SEMVER}' if PANTS_SEMVER.is_devrelease else f'>={PANTS_SEMVER.major}.{PANTS_SEMVER.minor}.0a0,<{PANTS_SEMVER.major}.{PANTS_SEMVER.minor + 1}'

@rule
def generate_from_pants_requirements(request: GenerateFromPantsRequirementsRequest, union_membership: UnionMembership) -> GeneratedTargets:
    generator = request.generator
    version = determine_version()

    def create_tgt(dist: str, module: str) -> PythonRequirementTarget:
        return PythonRequirementTarget({PythonRequirementsField.alias: (f'{dist}{version}',), PythonRequirementModulesField.alias: (module,), **request.template}, request.template_address.create_generated(dist), union_membership)
    result = [create_tgt('pantsbuild.pants', 'pants')]
    if generator[PantsRequirementsTestutilField].value:
        result.append(create_tgt('pantsbuild.pants.testutil', 'pants.testutil'))
    return GeneratedTargets(generator, result)

def rules():
    return (*collect_rules(), UnionRule(GenerateTargetsRequest, GenerateFromPantsRequirementsRequest))
import os
from pbr import packaging

from .base import BaseConfig


class DependenciesConfig(BaseConfig):
    requirements_base = [
        'requires',
        'requirements',
        'requirements/base',
        'requirements/prod',
        'requirements/main',
    ]

    requirements_test = [
        'test-requires',
        'test_requires',
        'test-requirements',
        'test_requirements',
        'requirements_test',
        'requirements-test',
        'requirements/test',
    ]

    requirements_extensions = [
        '',
        '.pip',
        '.txt',
    ]

    def __call__(self, config, facility_section_name):
        metadata = config.setdefault('metadata', {})
        backwards_compat = config.setdefault('backwards_compat', {})

        base_requirements = self._get_requirements(self.requirements_base)
        test_requirements = self._get_requirements(self.requirements_test)

        packaging.append_text_list(metadata, 'requires_dist', packaging.parse_requirements(base_requirements))
        packaging.append_text_list(backwards_compat, 'tests_require', packaging.parse_requirements(test_requirements))

        base_links = packaging.parse_dependency_links(base_requirements)
        test_links = packaging.parse_dependency_links(test_requirements)

        links = list(set(base_links + test_links))
        packaging.append_text_list(backwards_compat, 'dependency_links', links)

    @staticmethod
    def _combine(files, extensions):
        for filename in files:
            for ext in extensions:
                yield filename + ext

    @staticmethod
    def _is_file_exists(path):
        return os.path.exists(path) and os.path.isfile(path)

    def _get_requirements(self, files):
        return filter(self._is_file_exists, self._combine(files, self.requirements_extensions))

dependencies_config = DependenciesConfig()
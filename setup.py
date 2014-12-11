from setuptools import setup, find_packages, Command
import os
import subprocess


def get_version():
    try:
        from speedrate._version import get_version as get
        return get()
    except ImportError:
        return 'dev'


_VERSION = """
# search engine version information

_build = '%(build)s'
_branch = '%(branch)s'
_commit = '%(commit)s'


def get_version():
    return '-'.join([_build, _branch, _commit])


def get_version_url():
    if _build != 'dev':
        return 'https://circleci.com/gh/https://github.com/josephtoles/search-engine/tree/tox/' + _build
        """

class SetVersion(Command):
    description = 'Writes version information'
    user_options = []
    boolean_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def _git(self, cmd):
        return subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0].strip()

    def run(self):
        branch = os.environ.get('CIRCLE_BRANCH') or self._git(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
        branch = branch.replace('/', '-')
        build_num = os.environ.get('CIRCLE_BUILD_NUM') or 'dev'
        commit = os.environ.get('CIRCLE_SHA1') or self._git(['git', 'rev-parse', '--verify', 'HEAD'])
        with open('speedrate/_version.py', 'w+') as f:
            f.write(_VERSION % {
                'build': build_num,
                'branch': branch,
                'commit': commit
            })


class Version(Command):
    description = 'Prints version information'
    user_options = []
    boolean_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print get_version()


setup(
    name='search engine',
    version=get_version(),
    packages=find_packages(),
    url='All rights reserved.',
    license='',
    author='Joseph Toles & team',
    author_email='jbtoles@gmail.com',
    description='',
    include_package_data=True,
    cmdclass={
        "set_version": SetVersion, "version": Version
    }
)

import subprocess

# Usage: put it in the current directory, and run
#   py.test -p gitignore [...]


def pytest_ignore_collect(path, config):
    if path.basename == '.git':  # Ignore .git directory
        return True
    child = subprocess.Popen(['git', 'check-ignore', str(path)],
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)
    output = child.communicate()[0]
    status = child.wait()
    # Possible return values: (via git help check-ignore)
    #    0: Yes, the file is ignored
    #    1: No, the file isn't ignored
    #  128: Fatal error, git can't tell us whether to ignore
    #
    # The latter happens a lot with python virtualenvs, since they have
    # symlinks and git gives up when you try to follow one.  But maybe you have
    # a test directory that you include with a symlink, who knows?
    return status == 0
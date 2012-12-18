"""
Tests for the :class:`DotfileRepo` class.
"""
import os
import string
import random

import pytest

from moredots.repo import DotfileRepo

from tests.utils import random_string


# Tests

class TestInit(object):

    def test_init_basics(self, repo_dir, home_dir):
        repo = DotfileRepo.init(repo_dir, home_dir)
        assert repo.dir == repo_dir
        assert repo.home_dir == home_dir

    def test_init_persists_home_dir(self, repo_dir, home_dir):
        repo1 = DotfileRepo.init(repo_dir, home_dir)
        repo2 = DotfileRepo(repo_dir)  # from existing repo
        assert repo1.home_dir == repo2.home_dir

    def test_init_in_existing_repo(self, empty_repo):
        with pytest.raises(IOError):
            DotfileRepo.init(empty_repo.dir)


class TestAdd(object):

    def test_add_file_to_empty(self, empty_repo, dotfile):
        repo = empty_repo
        repo.add(dotfile)

        _, name = os.path.split(dotfile)
        assert os.path.exists(os.path.join(repo.dir, name[1:]))

    def test_add_file_to_nonempty(self, filled_repo, dotfile):
        repo = filled_repo
        repo.add(dotfile)

        _, name = os.path.split(dotfile)
        assert os.path.exists(os.path.join(repo.dir, name[1:]))

    def test_add_existing_file(self, empty_repo, dotfile):
        repo = empty_repo
        repo.add(dotfile)

        with pytest.raises(IOError):
            repo.add(dotfile)


class TestRemove(object):

    def test_remove_existing_file(self, filled_repo):
        repo = filled_repo

        dotfile = next(repo.dotfiles)
        repo.remove(dotfile)

        _, name = os.path.split(dotfile)
        assert not os.path.exists(os.path.join(repo.dir, name[1:]))

    def test_remove_nonexistent_file(self, filled_repo):
        repo = filled_repo

        dotfile = next(repo.dotfiles) + '_does_not_exist'
        with pytest.raises(OSError):
            repo.remove(dotfile)


# Fixtures / resources

@pytest.fixture
def repo_dir(tmpdir):
    """Directory to place the dotfile repo in."""
    return str(tmpdir.mkdir('repo'))


@pytest.fixture
def home_dir(tmpdir):
    """Directory to act as $HOME for the dotfile repo."""
    return str(tmpdir.mkdir('home'))


@pytest.fixture
def empty_repo(repo_dir, home_dir):
    """Empty moredots repository."""
    return DotfileRepo.init(repo_dir, home_dir)


@pytest.fixture
def filled_repo(repo_dir, home_dir):
    """Moredots repository with at least one dotfile."""
    repo = DotfileRepo.init(repo_dir, home_dir)

    # add some dotfiles
    for _ in xrange(random.randint(1, 5)):
        repo.add(dotfile(home_dir, dotfile_name()))

    return repo


@pytest.fixture
def dotfile(home_dir, dotfile_name):
    """A dotfile inside home directory.
    :return: Name of a dotfile
    """
    path = os.path.join(home_dir, dotfile_name)
    with open(path, 'w') as f:
        print >>f, random_string()
    return path


@pytest.fixture
def dotfile_name():
    """Random name of a dotfile."""
    return "." + random_string(chars=string.ascii_letters, length=16)

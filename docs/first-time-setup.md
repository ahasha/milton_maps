## First-time Setup

If the tools used by this project template are not already part of your development workflow, you will have to go through a few installation and configuration steps before you run a project following this project structure. You should not need to repeat these steps again to work on another project created with this cookiecutter.

### Python, Pyenv, and Poetry

Poetry is easy to use once set up, but it can be a little confusing to transition from other Python environment management tools, or to use it in the same environment as other tools.  This section will guide you through the one-time setup to install a clean Python environment using `pyenv` and install Poetry.

Using `pyenv` isn't necessary to use Poetry, but it's a convenient way to manage multiple isolated Python versions in your development environment without a lot of overhead.

Running the following in the terminal to install pyenv:

```bash
$ curl https://pyenv.run | bash
```

Then add the following to your shell login script (`~/.zshrc by default for Macs`):

```zsh
export PYENV_ROOT="\$HOME/.pyenv"
command -v pyenv >/dev/null || export PATH="\$PYENV_ROOT/bin:\$PATH"
eval "\$(pyenv init -)"
eval "\$(pyenv virtualenv-init -)"
```

If you've been using conda, and it's configured to automatically activate your base conda enviornment on login, you'll likely want to turn this off by running

```bash
$ conda config --set auto_activate_base false
```

Then log back into your shell and install poetry and the desired versions of python using

```bash
$ pyenv install <desired python version number>
$ pyenv global <desired default python version number>
$ curl -sSL https://install.python-poetry.org | python3 -
```

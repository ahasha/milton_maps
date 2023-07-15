# Getting started

This section will enable you to reproduce the project's analyses and data from a fresh clone fo the repository.

## Software Prerequisites

This project uses [poetry](https://python-poetry.org/docs/) to recreate an identical analytical software environment on each developer's machine.  To bootstrap this environment, you will need an existing installation of

* Python version 3.10
* Poetry v1.5.1+

For instructions to install these prerequisites for the first time, consult [First Time Setup](about.md#first-time-setup).

## Environment set up

Begin by cloning the model development repository

```bash
$ git clone git@github.com:ahasha/milton_maps.git
```

and change to the root directory of the project.  The command

```bash
$ make initialize
```

will install the project's software envionrment using poetry and install the project's git hooks, which enforce consistent code style, linting, and [dvc actions](https://dvc.org/doc/command-reference/install#description) to ensure data and code versions are synchronized.

You then run

```bash
$ poetry shell
```

to enter the virtual environment associated with the project.  Typing `exit` will exit the poetry shell, analogous to `deactivate` for a virtual environment.

## Get project data

This project uses [DVC](https://dvc.org) to store and track versioned data.  Similar to how git works, the DVC cache is a hidden storage folder (by default in
`.dvc/cache`) containing all versions of all files and directories tracked by
DVC.  It uses a [content-addressable structure](https://dvc.org/doc/user-guide/project-structure/internal-files#structure-of-the-cache-directory) that allows only the current version of tracked data corresponding to the current state of the code in the git repository to be automatically loaded into the workspace.

A shared dvc cache (analogous to a shared git remote on github.com) is located
in Google Cloud storage at `gs://hasha-ds-portfolio-projects/milton_maps/`.

As long as you can access this cloud bucket from your current working environment,
you can populate your local cache (analogous to running `git clone` to get the latest
version of a codebase) by running

```bash
$ dvc pull
```

from any directory inside the project.

## Reproduce the project results

Once the initial setup steps are complete, you can run the analysis pipeline to create the
notebook data inputs with the [`dvc repro`](https://dvc.org/doc/command-reference/repro) command.

```bash
$ dvc repro
```

generates pipeline results by executing the sequence of stages defined in dvc.yaml to calculate all outputs referenced in `dvc.lock`.  Stages are checked to determine which ones need to run -- if the stage output checksum is referenced in `dvc.lock` and already exists in the cache or the workspace, the stage is skipped.

If you wish to recalculate pipeline outputs to verify that they match reported results, run

```bash
$ dvc repro -f --no-commit
```

The `-f` flag tells DVC to recalculate all pipeline stages, even if there are no changes to their input dependencies.  The `--no-commit` flag tells DVC not to store the outputs of this execution in the cache.  If the pipeline has large outputs, a single byte difference will cause its checksum to change and DVC will add it permanently to the cache.  With many binary data formats, you can get a different file checksum even if the data contents are functionally identical.  `--no-commit` will enable you to verify the results have been appropriately reproduced without bloating the cache with functionally identical data files.  If later you do want to add the results to the cache, you can do so by running `dvc comit`.
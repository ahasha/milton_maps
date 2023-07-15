# About this Project's Structure

This project's structure and software stack reflect my current (as of July 2023) approach to producing analytics that is transparent and reproducible.  It incorporates years of experience as a model validator with common obstacles for stakeholders seeking to understand and use an analysis, and years of learning about how to apply software engineering best practices to minimize and remove them.

If you want to get your hands on the data and extend or reproduce my analysis, the instructions in [Getting Started](getting-started.md) should get you there. If you're curious to better understand how the project works and *why* I've made the choices I have, read through [Motivation and Guiding Ideas](about.md#motivations-and-guiding-ideas) below.  The [User Guide](about.md#user-guide) will take you deeper on how to use dvc, poetry, and sphinx effectively in this project or your own projects.

## Motivations and Guiding Ideas

### Reproducible history of all your analyses and results

It's no secret that Data Science is an exploratory process, and that failed experiments can be as informative as successful ones. But in the real-world, with deadlines, endless meetings, and constantly-shifting requirements, only the most (ahem) *detail-oriented* analyst have the fortitude to keep an explicit log of what they tried, let alone ensuring those results are reproducible.

Analytical results are produced by applying code to data.  To reproduce them, you need to apply the same code to the same data.  Using source control tools like `git` to track the detailed revision history of code has become standard practice on most Data Science teams, but because these tools are not designed to track large datasets, it is rare to see systematic data versioning.  This means that Data Scientists are typically tracking the alignment of code and data *mentally* during a project.  If you're not the author (or a few months have passed) it can be pretty tough to piece together what happened.

```{figure} https://imgs.xkcd.com/comics/documents.png
:alt: XKCD -- "Never look in someone else's documents folder"
:name: documents-folder

Taken with gratitude from [xkcd](https://xkcd.com/1459/).
```

While they are not as widely adopted as code versioning tools, data versioning tools delegate this task to the computer and free the analyst from having to mentally track code/data alignment.  This template uses [DVC](https://dvc.org/doc/user-guide) for data versioning because it requires no specialized infrastructure and integrates with all common data storage systems.

### End-to-end reproducible pipelines

Training and evaluating a model is a complex workflow with many interdependent steps that must be run in
the correct order.  Typical, notebook-centric analyses leave this task dependency structure
implicit, but there are major benefits to explicitly encoding them as a "Directed Acyclic Graph", or DAG.  Two key benefits are [^parallel-dvc-ref]

* **Consistency and Reproducibility**: once the workflow's structure has been encoded as a DAG, a workflow scheduler ensures that every step is executed in the correct order every time (unlike a tired Data Scientist working late to finish an analysis).
* **Clarity**: DAGs can be visualized automatically, and these visualizations are intuitive even for non-technical audiences.

There are many DAG orchestration tools in widespread use by Data Scientists
[^other-dag-tools], but most require remotely hosted infrastructure and/or a
significant learning curve to apply to an analysis project.  In addition to its data
versioning capabilities, DVC enables Data Scientists to build DAG workflows and
transparently track their data versions without requiring any remotely hosted task
orchestration infrastructure.

[^other-dag-tools]: For example, [Airflow](https://airflow.apache.org/index.html), and [Luigi](http://luigi.readthedocs.org/en/stable/index.html).

[^parallel-dvc-ref]: Parallelizing task execution is another major benefit of coding analysis as DAGs, but unfortunately DVC does not currently support task scheduling automatically, though this support will hopefully be added in the future.  See [iterative/dvc#75](https://github.com/iterative/dvc/issues/755) for more info.  Parallel task execution can be triggered manually as described [here](https://dvc.org/doc/command-reference/repro#parallel-stage-execution) if needed.

:::{mermaid}
:alt: A workflow graph of model development in all its hair-raising complexity.
:caption: Every model build I've ever worked on has ended up looking something like this.
flowchart TD

    BEG(figure out the business problem)

    BEG --> A
    A(select data) --> B(sample design)
    B --> C(query data)
    C --> D(calculate features)
    D --> E(fit models)

    BEG --> a
    a(select model type) --> b(choose model performance metrics)
    a --> E
    E --> d(evaluate model)
    b --> d
    d --> e(tune hyperparameters)
    d --> ee(select features)
    ee --> E
    e --> E

    d --> M(make lots of plots)
    M --> G

    d --> F
    F(pick a model) --> G(document everything)
    G --> H(review results with stakeholders)
    H --> Q(Make the decision)
    Q --> Z(become fabulously wealthy)


    H -->|Eek!| BEG
    H -->|Eegad!!| a
    H -->|sure, I can add that...| A
:::

### Optimize for faster iterations

If you're still exploring what analysis to perform or how to execute it, manual and interactive analysis tools are powerful, allowing analysts to experiment with different approaches to find what works.

But over the lifecycle of a modeling project, there's often a "phase transition" from experimenting with the scope and sequence of the analysis to repeating a well-defined sequence of steps over and over again with small variations as you make updates, fix bugs, and attempt to satisfy the curiosities of your stakeholders.  Typically, at this stage the analysis has also become more complex and involves multiple interconnected steps. Manual execution becomes increasingly time-consuming, error-prone, and inefficient in handling repetitive tasks and managing variations.

If your analysis is not currently automated end-to-end, the quickest path to the next deliverable will always be to crank it out manually. But if you make the investment to automate your analysis from initial data pull to final results, you can test more hypotheses and learn faster over the lifespan of the project.

Starting from scratch, the necessary investment is prohibitive for many Data Science teams.  But this template makes end-to-end automation with DVC much easier.

### Notebooks are for exploration and communication

Notebook packages like [Jupyter notebook](http://jupyter.org/) and other literate
programming tools are very effective for exploratory data analysis.  However, they are less
helpful for reproducing an analysis, unless the author takes special care to ensure they
run linearly end-to-end (effort that might be better spent refactoring the notebook into a
stand-alone script that can be imported for code re-use or scheduled in a DAG).  Notebooks
are also challenging objects for source control (e.g. diffs of the underlying `json` format
are often not human-readable, and require specialized plugins to view in your source
control platform that your IT department may not be willing to install or support.)

The guidelines for use of notebooks in this project structure are:

1.  Follow a naming convention that shows the owner and any sequencing required to run the
    notebooks correctly, for example `<step>-<ghuser>-<description>.ipynb` (e.g.,
    `0.3-ahasha-visualize-distributions.ipynb`).
2.  Refactor code and analysis steps that will be repeated frequently into python scripts
    within the the `your_proj` package.  You can import your code and
    use it in notebooks with a cell like the following;

    ```
    # OPTIONAL: Load the "autoreload" extension so that imported code is reloaded after a change.
    %load_ext autoreload
    %autoreload 2

    from your_proj.data import make_dataset
    ```

### Reproducible environment installation with Poetry

The first step in reproducing an analysis is always reproducing the computational environment it was run in. You need the same tools, the same libraries, and the same versions to make everything play nicely together.  Python is notorious for [making this difficult](https://medium.com/knerd/the-nine-circles-of-python-dependency-hell-481d53e3e025), even though there are a bunch of tools that are supposed to do this: `pip`, `virtualenv`, `conda`, `poetry`, etc.

A key thing to think about from a reproducibility standpoint to consider when choosing among these tools is subtle differences in their goals.  `pip` and `conda` are designed to be flexible — they want you to be able to install a given package with as wide a range of versions of other packages in your environment as possible, so you can construct environments with as many packages as you need.

This is great news for productivity, but bad news for reproducibility, because by default they'll install the latest version of any dependency that's compatible with the other declared dependencies. `pip` and `conda` have the capability to "peg" requirements to specific versions, but that isn't the default behavior and it requires quite a bit of manual work to use the tools that way, so people generally don't do it.

For example, suppose you want to use `pandas`, and you create the following `requirements.txt` file and install it with `pip install -r requirements.txt`:

```
pandas==1.4.2
```

When you first run the pip install command, you might get version 1.20.0 of `numpy` installed to satisfy `pandas` requirements. However, when you run the pip install command again half a year later, you might find that the version of numpy installed has changed to 1.22.3, even though you are using the same requirements.txt file.

Worse, package developers are often sloppy about testing all possible combinations of dependency versions, so it's not uncommon that packages that are "compatible" in terms of their declared requirements in fact don't work together. An environment managed with pip or conda that worked a few months ago no longer works when you do a clean install today.

This template uses [`poetry`](https://python-poetry.org/) to manage the dependency environment.  `poetry` is a great choice from a reproducibility perspective because it assumes you want to peg all dependency versions by default and its priority is to generate the same environment predictably every time.[^conda-speed-aside]

[^conda-speed-aside]: It also seems to be a lot faster than conda, which is great.

### Consistency and familiarity

A well-defined, standard project structure lets a newcomer start to understand an analysis having to spend a lot of time getting oriented. They don't have to read 100% of the code before knowing where to look for very specific things.  Well-organized code is self-documenting in that the organization itself indicates that function of specific components, without requiring additional explanation.

In an organization with well-established standards,

* Managers have more flexibility to move team members between projects and domains, because less "tribal knowledge" is required
* Colleagues can quickly focus on understanding the substance of your analysis, without getting hung up on the mechanics
* Conventional problems are solved in conventional ways, leaving more energy to focus on the unique challenges of each project
* New best practices and design patterns can quickly be projected to the team by updating the template.

A good example of this can be found in any of the major web development frameworks like Django or Ruby on Rails. Nobody sits around before creating a new Rails project to figure out where they want to put their views; they just run `rails new` to get a standard project skeleton like everybody else. Because that default project structure is _logical_ and _reasonably standard across most projects_, it is much easier for somebody who has never seen a particular project to figure out where they would find the various moving parts.  Ideally, that's how it should be when a colleague opens up your data science project.

That said,

> "A foolish consistency is the hobgoblin of little minds" — Ralph Waldo Emerson (and [PEP 8!](https://www.python.org/dev/peps/pep-0008/#a-foolish-consistency-is-the-hobgoblin-of-little-minds))

Or, as PEP 8 put it:

> Consistency within a project is more important. Consistency within one module or function is the most important. ... However, know when to be inconsistent -- sometimes style guide recommendations just aren't applicable. When in doubt, use your best judgment. Look at other examples and decide what looks best.

:::{include} first-time-setup.md
:::

:::{include} user-guide.md
:::
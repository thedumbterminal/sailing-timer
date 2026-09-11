from invoke import task


@task
def format(c):
    print("Running formatting...")
    c.run("black .")


@task
def start(c):
    print("Running start...")
    c.run("python -m src.main -d")


@task
def dev(c):
    print("Running dev...")
    c.run("watchfiles 'invoke start'")


@task
def typecheck(c):
    print("Running type checking...")
    c.run("mypy src")


@task
def syntax(c):
    print("Checking syntax...")
    c.run("python -m compileall -q src")


@task(syntax)
def ci(c):
    print("Running CI tasks...")

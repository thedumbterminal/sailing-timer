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

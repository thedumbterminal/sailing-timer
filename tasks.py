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

@task
def start_docker(c):
    print("Running start docker...")
    c.run("docker buildx build --platform linux/arm64 -t sailing-timer --load .")
    print("Now run the following command to start the container:")   
    print("docker run -it -p 2222:22 -p 5901:5901 sailing-timer")   

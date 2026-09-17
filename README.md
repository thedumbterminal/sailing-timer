# Sailing Timer

Built using kivy:

https://kivy.org/

## Requirements

* pyenv

## Install

```bash
script/setup-python.sh
script/install.sh
```

## Run

To run use:

```bash
invoke start
```

Or with reloading:


```bash
invoke dev
```

## Run from docker

This allows you to have access to a small X server to mimic the small touch screen.

```bash
invoke build-docker
```

Then connect via VNC to `vnc://localhost:5901`

FROM debian:bookworm

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update

RUN apt install -y xfce4 \
    xfce4-goodies \
    tigervnc-standalone-server \
    tigervnc-tools \
    openssh-server \
    dbus-x11 \
    sudo \
    python3 \
    python-is-python3 \
    vim \
    locales \
    python3-pip

RUN sed -i 's/^# *en_GB.UTF-8 UTF-8/en_GB.UTF-8 UTF-8/' /etc/locale.gen && locale-gen en_GB.UTF-8

ENV LANG=en_GB.UTF-8
ENV LANGUAGE=en_GB:en
ENV LC_ALL=en_GB.UTF-8

RUN useradd -m -s /bin/bash pi
RUN echo "pi:raspberry" | chpasswd
RUN usermod -aG sudo pi

RUN mkdir -p /run/sshd
RUN ssh-keygen -A

USER pi
WORKDIR /home/pi

RUN mkdir -p /home/pi/.vnc
RUN mkdir -p /home/pi/.Xresources
RUN printf "raspberry\nraspberry\nn\n" | vncpasswd

COPY --chown=pi:pi . /home/pi/sailing-timer
RUN pip install --break-system-packages --user -r /home/pi/sailing-timer/requirements.txt

USER root

EXPOSE 22 5901

CMD /usr/sbin/sshd && exec su - pi -c "vncserver :1 -geometry 480x320 -depth 24 -localhost no -fg -- xfce4-session"

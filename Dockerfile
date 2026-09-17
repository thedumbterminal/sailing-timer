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
    vim \
    locales \
    python3-pip 

RUN sed -i 's/^# *en_GB.UTF-8 UTF-8/en_GB.UTF-8 UTF-8/' /etc/locale.gen && locale-gen en_GB.UTF-8

ENV LANG=en_GB.UTF-8
ENV LANGUAGE=en_GB:en
ENV LC_ALL=en_GB.UTF-8

RUN useradd -m -s /bin/bash pi
RUN echo "pi:raspberry" | chpasswd

RUN mkdir -p /run/sshd
RUN ssh-keygen -A
RUN /usr/sbin/sshd

USER pi
WORKDIR /home/pi

RUN mkdir -p /home/pi/.vnc
RUN mkdir -p /home/pi/.Xresources
RUN printf "raspberry\nraspberry\nn\n" | vncpasswd

EXPOSE 22 5901

CMD ["vncserver", ":1", "-geometry", "800x600", "-depth", "24", "-localhost", "no", "-fg", "--", "xfce4-session"]

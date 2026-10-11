# Remote X

From the GUI terminal:

xhost +SI:localuser:pi

From SSH to the pi:

 export DISPLAY=:0
 export XAUTHORITY=/home/pi/.Xauthority

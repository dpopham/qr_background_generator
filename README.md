## QR Code Background Generator

Written by Darren Popham

### What is this?

The QR code background generator is a simple web service that allows someone to input text (with or without URLs) that they want to encode as an image that may be suitable for their Zoom or Teams background.  People curious about the QR code floating over your shoulder may take their phone, point at it, and voila, instant Rick Roll.

### Why would I use this?

For the hilarity that ensues, or perhaps to embed a hidden image such as "We are hiring, if you were quick enough to decode this then click.....".  Who knows what else you might want to use this.  I suspect though primarily for the hilarity.

### How do I build it?

Python.

Basically:

> cd FOLDER<br>
> virtualenv -p python3 vpython<br>
> source vpython/bin/activate<br>
> pip install -r requirements.txt<br>

### How do I start it?

If in a hurry,

> python qr.py<br>

However I also supplied a sample systemctl script if you want to start it as a service that way and a simple proxy location snippet if you use nginx as your front end web server.  As always, never expose services directly on the network, always protect your services behind a tool designed to keep it safe, such as nginx.

Enjoy!


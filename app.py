#!/usr/bin/env python

from blah import *

if __name__ == "__main__":
    development = True
else:
    development = False

app = BlahApp(development)

if __name__ == "__main__":
    app.run()

# Selenium Chrome with Proxy in Headless mode
Selenium Chrome dont support extensions in headless mode. We need to set a display properties to simulate it.
## INSTALL
* sudo apt install -y xvfb
* pip3 install selenium pyvirtualdisplay jinja2
## TO FIX
* Cannot use extensions in incognito mode. Check config in [manifest](src/manifest.json)
    ```python 
    options.add_argument("--incognito")
    ```
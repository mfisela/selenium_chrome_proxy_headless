#!/usr/bin/python3

import json
import jinja2
from os import path, remove
from zipfile import ZipFile
from pyvirtualdisplay import Display
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options


def get_path() -> str:
    return path.dirname(path.abspath('__file__'))


def get_pref() -> dict:
    filename = path.join(get_path(), 'src', 'pref.json')
    with open(filename) as f:
        data = f.read()
    return json.loads(data)


def get_proxy_plugin(**kwargs):
    def get_jinja_template(template: str, vars: dict = dict()):
        with open(template) as f:
            data = f.read()
        tpl = jinja2.Template(data)
        return tpl.render(vars)

    def get_manifest():
        template = path.join(get_path(), 'src', 'manifest.json')
        return get_jinja_template(template=template)

    def get_background(**kwargs):
        proxy = kwargs.get('proxy', dict())
        template = path.join(get_path(), 'tpl', 'background.js.jinja2')
        return get_jinja_template(template=template, vars=proxy)

    pluginfile = path.join(get_path(), 'tmp', 'proxy_auth_plugin.zip')
    manifest_json = get_manifest()
    background_js = get_background(**kwargs)
    with ZipFile(pluginfile, 'w') as zp:
        zp.writestr("manifest.json", manifest_json)
        zp.writestr("background.js", background_js)
    return pluginfile


def chrome_options(headless: bool = False) -> Options:
    options = Options()
    options.headless = headless
    #options.add_argument("--incognito")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    prefs = get_pref()
    options.add_experimental_option('prefs', prefs)
    return options


def get_driver(**kwargs) -> Chrome:
    """
    kwargs:
        * proxy: dict (optional)
        * user_agent: str (optional)
    """
    options: Options = chrome_options()
    chromedriver: str = path.join(get_path(), 'src', 'chromedriver')
    if kwargs.get('proxy'):
        pluginfile = get_proxy_plugin(**kwargs)
        options.add_extension(pluginfile)
    if kwargs.get('user_agent'):
        options.add_argument('--user-agent=%s' % kwargs.get('user_agent'))
    driver = Chrome(chromedriver, options=options)
    return driver


def main(url, **kwargs):
    display = Display(visible=0, size=(1280, 720))
    display.start()
    driver: Chrome = get_driver(**kwargs)
    driver.get(url)
    print(driver.page_source)
    driver.close()
    display.stop()
    remove(path.join(get_path(), 'tmp', 'proxy_auth_plugin.zip'))


if __name__ == '__main__':
    url = 'https://api.ipify.org/?format=json'
    proxy = {
        'PROXY_HOST': '127.0.0.1',
        'PROXY_PORT': 1234,
        'PROXY_USER': 'user',
        'PROXY_PASS': 'pass'
    }
    main(url=url, proxy=proxy)

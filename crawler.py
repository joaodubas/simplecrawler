#!/usr/bin/env python
# encoding: utf-8

"""Simple wrapper from webdriver, exposing only a set of operations."""

from selenium import webdriver


class Crawler(object):
    """Simple web crawler based on selenium webdriver."""

    def __init__(self, browser='Firefox'):
        """Pass the desired browser to be used by the crawler, exposing it via
        ``nav`` attribute.

        browser -- navigator app to be used by the crawler, defaults to Firefox

        >>> hasattr(c, 'nav')
        True
        >>> c.nav.name == 'firefox'
        True
        >>> c.navigate_to('http://www.python.org/')
        >>> c.nav.current_url
        u'http://www.python.org/'

        """
        if browser.islower():
            browser = browser[0].upper() + browser[1:]
        if hasattr(webdriver, browser):
            self.nav = getattr(webdriver, browser)()
        else:
            raise ValueError(u'%s is not a valid browser' % browser)

    def __del__(self):
        """Closes the browser session before delete the instance."""
        self.close_browser()

    def navigate_to(self, url):
        """Make the browser open the defined url and return the navigator
        reference.

        url -- the web address to be opened on the navigator app.

        """
        self.nav.get(url)

    def page_source(self):
        """Return the page source, allowing it to be used by html parsers."""
        return self.nav.page_source

    def close_browser(self):
        """Close the navigator app, ending the current session."""
        self.nav.close()


if __name__ == '__main__':
    import doctest
    doctest.testmod(extraglobs={
        'c': Crawler(),
    })

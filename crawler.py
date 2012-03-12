#!/usr/bin/env python
# encoding: utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class Crawler(object):
    """Simple web crawler based on selenium webdriver."""
    def __init__(self, browser='Firefox'):
        """Pass the desired browser to be used by the crawler, exposing it via
        ``nav`` attribute.

        browser -- navigator app to be used by the crawler, defaults to Firefox

        >>> crawler = Crawler()
        >>> hasattr(crawler, 'nav')
        True
        >>> nav.name == 'Firefox'
        True

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
        super(Crawler, self).__del__()

    def navigate_to(self, url):
        """Make the browser open the defined url and return the navigator
        reference.

        url -- the web address to be opened on the navigator app.

        >>> crawler = Crawler()
        >>> crawler.navigate_to('http://www.python.org/')
        >>> crawler.current_url
        u'http://www.python.org/'

        """
        self.nav.get(url)

    def page_source(self):
        """Return the page source, allowing it to be used by html parsers."""
        return self.nav.page_source()

    def close_browser(self):
        """Close the navigator app, ending the current session."""
        self.nav.close()


class Location(object):
    """Obtain the state and city served by Amil."""
    base_url = 'http://www.amil.com.br/'

    def __init__(self):
        """Add the property ``state`` to the class instance."""
        self.state = {}

    def get_state(self):
        pass

    def get_city(self, state):
        pass


if __name__ == '__main__':
    crawler = Crawler()
    crawler.navigate_to('http://www.python.org/')
    assert 'Python' in crawler.nav.title
    el = crawler.nav.find_element_by_name('q')
    el.send_keys('selenium')
    el.send_keys(Keys.RETURN)
    assert 'Google' in crawler.nav.title
    crawler.close_browser()

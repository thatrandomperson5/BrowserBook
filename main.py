from BrowserBook import brbook
import time
browser = brbook('book')
id = browser.sessionStart()
while True:
  url = input('url: ')
  Session = browser.getSessionObject(browser.name, id)
  Session.localize = True
  Session.Get(url)
  if input('Would you like to continue?(y/n)') == 'n':
    browser.EndSession(id)
    break
  else:
    Session.dump()

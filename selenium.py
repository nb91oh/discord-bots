from selenium import webdriver
from selenium.webdriver.common.keys import Keys

url = "https://duckduckgo.com/?q={}&iar=images&iax=images&ia=images"
css_path = "html.has-zcm.is-mobile-header-exp.js.no-touch.opacity.csstransforms3d.csstransitions.svg.cssfilters.is-not-mobile-device.full-urls body.body--serp div.site-wrapper.js-site-wrapper div#zero_click_wrapper.zci-wrap div#zci-images.zci.zci--images.zci--type--tiles.is-full-page.is-expanded.is-active div.js-tileview.tileview--grid div.tile-wrap div.zci__main.zci__main--tiles.js-tiles.has-nav.tileview__images.has-tiles--grid div.tile.tile--img.has-detail div.tile--img__media span.tile--img__media__i img.tile--img__img.js-lazyload"


driver = webdriver.Firefox()
driver.get(url)

element = driver.find_element_by_css_selector(css_path)
src = element.get_attribute('src')

print(src)

driver.close()
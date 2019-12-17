# Convert  Jupyter notebook into a Python script called scrape_mars.py with a function called scrape that will execute all of your scraping code from above and return one Python dictionary containing all of the scraped data.
def scrape():
    # Import dependencies
    from splinter import Browser
    from bs4 import BeautifulSoup
    from selenium import webdriver
    import pandas as pd
    from IPython.display import display 
    from IPython.display import display_html

    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

    #-----------NASA MARS NEWS---------------
    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. Assign the text to variables that you can reference later.
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    # Find latest News Title
    titles = soup.find_all('div',class_='content_title')
    news_title = titles[0].text

    # Find latest News Paragraph Text
    paragraphs = soup.find_all('div',class_='article_teaser_body')
    news_p = paragraphs[0].text

    #-------------JPL MARS SPACE IMAGES - FEATURED IMAGE-------------
    # Use splinter to navigate the site and find the image url for the current Featured Mars Image and assign the url string to a variable called featured_image_url.
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    jpl_short_url = jpl_url.split('/spaceimages')[0]
    browser.visit(jpl_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    large_url = soup.find_all('a', class_="button fancybox")[0]['data-link']
    large_entire_url = jpl_short_url + large_url
    browser.visit(large_entire_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    large_size_partial = soup.find_all('img', class_='main_image')[0]['src']
    featured_image_url = jpl_short_url + large_size_partial
    # featured_image_url = jpl_url+soup.find_all('a',id="full_image")[0]['data-fancybox-href']
    # # featured_image_url

    #----------- MARS WEATHER---------------
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    driver = webdriver.Chrome()
    driver.get(twitter_url)
    html = driver.page_source
    mars_weather = driver.find_element_by_class_name('TweetTextSize').text

    #-------------- MARS FACTS---------------
    table_url = 'https://space-facts.com/mars/'
    browser.visit(table_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    df_table = pd.read_html(html)[0]
    df_table = df_table.rename(columns={0:'description',1:'value'})
    df_table = df_table.set_index('description')
    html_table_string = df_table.to_html()

    #----------- MARS HEMISPHERES---------------
    hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    hemi_short_url = hemi_url.split('/search')[0]
    browser.visit(hemi_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    link_test = browser.find_by_css('h3')
    hemi_names = [link.value for link in link_test]
    hrefs = [img.a['href'] for img in soup.find_all('div',class_='description')]
    clicked_urls = [(hemi_short_url + href) for href in hrefs]
    img_urls = []
    for url in clicked_urls:
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')
        img_urls.append(hemi_short_url + soup.find_all('img',class_='wide-image')[0]['src'])

    hemi_1 = {'title':hemi_names[0],'img_url':img_urls[0]}
    hemi_2= {'title':hemi_names[1],'img_url':img_urls[1]}
    hemi_3 = {'title':hemi_names[2],'img_url':img_urls[2]}
    hemi_4 = {'title':hemi_names[3],'img_url':img_urls[3]}
    hemisphere_image_urls = [hemi_1, hemi_2, hemi_3, hemi_4]

    # Return one python dictionary containing all of the scraped data
    main_dict = {'news_title':news_title}
    main_dict['news_p']=news_p
    main_dict['featured_image_url']=featured_image_url
    main_dict['mars_weather']=mars_weather
    main_dict['html_table_string']=html_table_string
    main_dict['hemisphere_image_urls']=hemisphere_image_urls

    # close the browser
    browser.quit()

    return main_dict
"""
Authour: Naresh Kumar Chava
Date: 02/10/2021

Desc: Linkedin Utils is a set of helper functions to scrape Linkedin posts for a specific key word and get desired data that include Post link, job link, authour profile, location, job title 


Version history:

05/21/2021- Updated author_profile functions to accomodate new Li containers


"""


def linkedin_login(web_driver,username,password):
    '''
    Helper function to get login to Linkedin with provided username and password
    
    Parameters
    ----------
    web_driver : selenium driver object
    username: string 
    password: string
    '''
    #Open Linkedin login page
    web_driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')

    #Enter login info:
    elementID = web_driver.find_element_by_id('username')
    elementID.send_keys(username)

    elementID = web_driver.find_element_by_id('password')
    elementID.send_keys(password)
    #Note: replace the keys "username" and "password" with your LinkedIn login info
    elementID.submit()

    #Close any message pop ups to make default page active
    #Import exception check
    from selenium.common.exceptions import NoSuchElementException
    try:
        if browser.find_element_by_class_name('msg-overlay-list-bubble--is-minimized') is not None:
            pass
    except NoSuchElementException:
        try:
            if browser.find_element_by_class_name('msg-overlay-bubble-header') is not None:
                browser.find_element_by_class_name('msg-overlay-bubble-header').click()
        except NoSuchElementException:
            pass
    return

def author_profile(author_profile_link):
    '''
    Helper function to get Name, Title & Location from the linkedin profile
    
    Parameters
    ----------
    author_profile_link : string
    
        Linkedin profile link
    
    Returns
    -------
    list
    
        a list of containing profile_link, Name, Title & Location
    
    '''
    #Opne new web page to visit author profile
    browser.execute_script(f'''window.open("{author_profile_link}","_blank");''')
    browser.switch_to.window(browser.window_handles[-1])
    #Wait 5 sec for the page to load
    time.sleep(1)
    #Linkedin profile soup object
    src = browser.page_source
    soup = bs4.BeautifulSoup(src, 'lxml')
    #Extract profile information
    profile_info_div = soup.find('div', {'class': 'pv-text-details__left-panel mr5'})
    name=profile_info_div.find_all('h1')[0].get_text().strip()
    title= profile_info_div.find('div', {'class': 'text-body-medium break-words'}).get_text().strip()
    location=profile_info_div.find('span', {'class': 'text-body-small inline t-black--light break-words'}).get_text().strip()
    # name = profile_info_div.find_all('ul')[0].find('li').get_text().strip()
    # name=profile_info_div.find_all('h1')[0].get_text().strip()
    # title=profile_info_div.find_all('h2')[0].get_text().strip()
    # location=profile_info_div.find_all('ul')[1].find('li').get_text().strip()
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    return [name,title,location,author_profile_link]

def post_link(web_driver,post_container):
    '''
    Helper function to get Post link
    
    Parameters
    ----------
    post_container : soup object
    
        soup object of the post
    
    Returns
    -------
    string
        
        Web link of the Linkedin post        
    
    '''
    #Get new page source code
    src = web_driver.page_source
    soup = bs4.BeautifulSoup(src, 'lxml')
    #Get cpost menu button id
    post_menu=post_container.find_all('button',{"class":"artdeco-dropdown__trigger artdeco-dropdown__trigger--placement-bottom ember-view artdeco-button artdeco-button--2 artdeco-button--tertiary artdeco-button--circle artdeco-button--muted mr1"})
    post_menu_id=post_menu[0].get('id')     
    #click on Post Menu
    actions = ActionChains(web_driver)
    post_ellipses=browser.find_elements_by_xpath(f"//button[@type='button' and @id='{post_menu_id}']")
    actions.move_to_element(post_ellipses[0]).click().perform()
    time.sleep(1)
    #Get Copy link button id. Copy link is option 2 in linkedin post menu
    post_menu_options=post_container.find_all('div',{"class":"artdeco-dropdown__item artdeco-dropdown__item--is-dropdown ember-view entity-result__overflow-actions-menu-item"})
    copy_link_id=post_menu_options[2].get('id') 
    #click on Copy link
    copy_link=browser.find_elements_by_xpath(f"//div[@id='{copy_link_id}']")
    copy_link[0].click()
    #Link from clipboard
    post_link = pyperclip.paste()
    actions.move_to_element(post_ellipses[0]).click().perform()
    return post_link

def post_content(post_link):
    '''
    Helper function to get Post Content
    
    Parameters
    ----------
    post_link : string
    
        web link of linkedin post
    
    Returns
    -------
    string
        
        content of given linkeding post along with a job posting link if exists      
    
    '''
    #Open new web page to visit the post
    browser.execute_script(f'''window.open("{post_link}","_blank");''')
    browser.switch_to.window(browser.window_handles[-1])
    #Wait 2 sec for the page to load
    time.sleep(2)
    #visited Post soup object
    src = browser.page_source
    soup = bs4.BeautifulSoup(src, 'lxml')
    s=soup.find('span', {'class': 'break-words'})
    #Capture posting link if exists
    try:    
        job_link=""
        original_posting=soup.find('div',{'class':'feed-shared-article__link-container'})
        job_link=original_posting.find('a').get('href')
    except:
        job_link=""
    
    #Close browser
    browser.close()
    browser.switch_to.window(browser.window_handles[0])
    return [s.getText(),job_link]
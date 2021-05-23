# Selenium Automation tool for Linkedin Scraping

Cold calls to recruiters/hiring managers will have a better conversion rate than directly applying for a job. While there are many ways to make cold calls for a role of interest, a targeted approach will save time of both the candidate & the person on other side.


One targeted approach with highest conversion rate (based on my personal experience) is contacting a person who posts about a specific role with terms hiring/looking on Linkedin. 


Although one can filter for Linkedin posts with a specific key word, Likedin doesn't allow to filter on the location of post source or in other words Author's location who has posted. Because of which, filtering for a specific keyword will result in enormous amounts of posts from all around the world most of which may not be relevant due to location.      

To overcome this drawback in Linkedin, this tool presents Selenium based automation to scrape Linkeding posts with Specific Key word (Say 'Data Scientist') and filters those with term Hiring/Looking for X role (X: Data Scientist) and further scrapes authour profile and ouputs a excel file  with following fields.

1. Link to Post
2. Post content
3. Link to authour profile
4. authour name, title, location
5. Direct link to job posting (if it's part of the post)



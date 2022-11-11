# Splash-Web-Scrape-Quotes  
Scrape quotes from multi-page JavaScript website using Splash and Scrapy  

# Modern Web Scraping Section 11: Scraping JavaScript Websites using Splash Part 6: Scraping Quotes Website Assessment  
## Objective  
Scrape this website 'http://quotes.toscrape.com/js'. It does require JavaScript so using either Splash or Selenium is required.  
Scrape the quote text, the author and all the tags for each quote from all the available pages.  
# Process  
## Investigate the website  
Type http://quotes.toscrape.com/robots.txt   
No robots.txt file so we are safe to scrape  
Within developer tools, disable JavaScript on http://quotes.toscrape.com/js to see what we are working with  
You cant see anything when you disable JavaScript so we are going to have to use Splash  
## Create a new project:  
Open Anaconda prompt from the virtual_workspace environment  
From within the projects folder  
Type cd projects if necessary  
Create a new project by typing: 
  
    scrapy startproject quotes     
Use cd quotes to get into the new quotes folder to scaffold the new spider  
### Scaffold the new spider  
Type: 
  
    scrapy genspider quote quotes.toscrape.com/js/    
## Launch VS Code from the Anaconda virtual_workspace environment  
Open QUOTES folder  
## Install Scrapy-Splash  
To be able to use Splash with Scrapy, we need to install a package called scrapy-splash  
Go to https://github.com/scrapy-plugins/scrapy-splash   
Copy the installation command at the top of the page: 
  
    pip install scrapy-splash    
In Anaconda Prompt, paste: pip install scrapy-splash <PRESS ENTER>  
Now we have scrapy-splash installed   
## Configure Scrapy-Splash  
### In VS Code:  
#### Add Splash url  
Open the settings.py file  
Scroll to the bottom  
Add SPLASH_URL equals to single quotes, and then paste in the access code.   
The webpage my Splash is working on starts with: http://localhost:8050   
Like this: 
  
    SPLASH_URL = 'http://localhost:8050/'    
#### Add DOWNLOADER_MIDDLEWARES  
Copy the code from #2 in the Configuration section of the github page  
In VS Code:  
In the settings.py file  
Scroll to the middle to the section called “Enable or disable downloader middlewares”  
Highlight the DOWNLOADER_MIDDLEWARES = {} section and paste in what you copied from the github  
Like this:  
    
    DOWNLOADER_MIDDLEWARES = {  
        'scrapy_splash.SplashCookiesMiddleware': 723,  
        'scrapy_splash.SplashMiddleware': 725,  
        'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,  
    }    
#### Add SPIDER_MIDDLEWARES  
Copy the code from #3 in the Configuration section of the github page  
In VS Code:  
In the settings.py file  
Scroll to the middle to the section called “Enable or disable spider middlewares”  
Highlight the SPIDER_MIDDLEWARES = {} section and paste in what you copied from the github  
Like this:  
  
    SPIDER_MIDDLEWARES = {  
        'scrapy_splash.SplashDeduplicateArgsMiddleware': 100,  
    }      
#### Set the duplicator filter class  
This step will prevent duplicate requests   
Copy the code from #4 in the Configuration section of the github page    
In VS Code:  
In the settings.py file  
Scroll to the middle to the section called “Enable or disable downloader middlewares”  
After the DOWNLODER_MIDDLEWARES section, paste in the DUPEFILTER_CLASS you copied from the github  
Like this: 
   
    DOWNLOADER_MIDDLEWARES = {  
        'scrapy_splash.SplashCookiesMiddleware': 723,  
        'scrapy_splash.SplashMiddleware': 725,  
        'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,  
    }    
    DUPEFILTER_CLASS = 'scrapy_splash.SplashAwareDupeFilter'    
Crtl + s to save  
## Import scrapy-splash  
At the top of the quote.py file, add:

    from scrapy_splash import SplashRequest  
Crtl + s to save  
## Boot up Splash  
Open Docker Desktop  
Click containers  
Click the “play” button the one with the image “scrapinghub/splash”  
Click on the row of “scrapinghub/splash” to open the code log  
In the log, click on the “open in browser” button  
## In Splash  
Paste into the Splash search bar the web address: http://quotes.toscrape.com/js    
### In the Script:  
Set up your main() function  
Set url variable equal to args.url  
Assert go equal to url in order to go to the url   
You have to tell Splash to wait when you go to a new url to make sure the url is fully rendered, so assert a wait time  
Return splash html, since that is what Scrapy is going to need  
Like this:  
  
    function main(splash, args)  
    url = args.url  
    assert(splash:go(url))  
    assert(splash:wait(1))  
    return splash:html()   
    end    
Click the “Render” button  
This returned the html that looks correct, so that is good  
Copy the Splash script  
## In VS Code  
Open the quote.py spider  
### Add the Script:  
In properties, type: script = then triple quotes and then paste in the contents of the Splash script, then end with triple quotes   
Like this: 

    script = '''  
        function main(splash, args)  
            url = args.url  
            assert(splash:go(url))  
            assert(splash:wait(1))  
            return splash:html()  
   
        end  
    '''  
### Write start_requests() method  
Then, after the script, define a new method, called start_requests()  
Within the start_requests method, type: yield SplashRequest()  
The first argument would be the rule of the target website  
so , url=”<url>”,    
The second argument would be the callback method  
So, callback=self.parse,  
The third argument is called endpoint  
And since we want to execute the script from Splash, we should set the the endpoint to execute   
Finally, we should tell the SplashRequest class what script you want to execute   
This argument is args=curly brackets  
Inside the curly brackets, the key is ‘lua_source’ and the value is self.script  
Like so:  
  
        end  
    '''  
    def start_requests(self):  
        yield SplashRequest(url="http://quotes.toscrape.com/", callback=self.parse,   endpoint="execute", args={  
            'lua_source': self.script  
        })  
     def parse(self, response):  
  
### Modify the parse() method  
Change the pass inside the parse method to print(response.body)  
This will print the html markup   
Looks like this:  
  
    def parse(self, response):  
        print(response.body)  

Crtl + s to save the file   
## Open the integrated terminal  
Terminal > New terminal  
Execute the command:

    scrapy crawl quote  
As you can see, we did get the html markup as expected  
Now we can write the parse to get the contents  
## In Developer tools:  
We want to get the quote text, the author, and all the tags from each entry. Let’s see where we can find those things    
All the elements for a single entry are in a div with a class of quote as seen here:  
//div[@class='quote']  
- Quote text:   

  
    //div[@class='quote']/span[@class='text']/text()  

- Author:  

  
    //div[@class='quote']/span/small[@class='author']/text()  

- Tags:   

  
    //div[@class='quote']/div[@class='tags']/a/text()  

## In VS Code:  
Within the parse method, delete the print statement  
Write: 
    
    for quote in response.xpath(“<enter the address of a single entry>”):  
Within the parse statement, write  yield, followed by curly brackets  
The three items we will yield, written in dict form are:   
- Quote text  
- Author  
- Tags  

So it looks like this:  
  
    def parse(self, response):  
        for currency in response.xpath("//div[@class='quote']"):  
            yield {  
                'Quote Text': currency.xpath(".//span[@class='text']/text()").get(),  
                'Author': currency.xpath(".//span/small[@class='author']/text()").get(),  
                'Tags': currency.xpath(".//div[@class='tags']/a/text()").get_all()  
            }  
Crtl + s to save  
## In the integrated terminal  
If not already open, Terminal > New terminal  
Optionally, type “cls” to clear contents  
Execute the command: 

    scrapy crawl quote  
This returned the desired results for page one  
Now we can add the “next” button clicking statement within the parse statement  
## In VS Code:  
After the closing of the curly brackets in the quotes yield statement, write an the xpath response statement to get the “next” button  
Follow that with an if statement saying, if there is a next button, click it  
Then yield a splash request to use the newly defined url and go back to the beginning of the parse method to scrape that next page’s quotes using the script created by the Splash statement
So it looks like this:  
  
        next_page = response.xpath("//li[@class='next']/a/@href").get()  
        if next_page:  
            absolute_url = f'http://quotes.toscrape.com{next_page}'  
            yield  SplashRequest(url=absolute_url, callback=self.parse, endpoint='execute', args={
                'lua_source': self.script  
            })  

Crtl + s to save   
## In the integrated terminal  
If not already open, Terminal > New terminal  
Optionally, type “cls” to clear contents  
Execute the command: 

    scrapy crawl quote  
This returned an  'item_scraped_count': 100,  
There are ten quotes on page one and the last page to have a “next” button links to page 10, so that checks out  
## Save file  
To save the quotes to a csv file, execute the command: 

    scrapy crawl quote -O extractedQuotes.csv 
     
## Optionally, upload project to GitHub  




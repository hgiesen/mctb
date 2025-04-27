# This is an experiment to play with the concepts of
# using genai on webscraped content
# process is easy; use the BBC weather site (KNMI is in dutch)
# and ask a back end ai what the clothing advise based of the weather is
# in my setting i use a local version of Deepseek 7bn model via Ollama
# (don't expecting big results, but it is a test)
#
# as this is experimental code, don't expect clean code, nor propper error handling
# goal is to learn new techniques and have fun. Creating the tools for a future trading bot
#
# HG 2025


# We need crawler and asyncio to a-synchonos let the crawler run
# i really liked learning to work also with asyncio in python, feels its less 
# scripting now and more programming  :-)
import asyncio
from crawl4ai import *

# need ollama to run the model 
# when running at home, remember this code doesnt include ollama, but you need to 
# run it locally.
import ollama

# First lets get the input from the bbc site and store it in neResult
async def main():
    async with AsyncWebCrawler() as crawler:
        result = await crawler.arun(
            url="https://www.bbc.com/weather/2759794",
        )
        #####print(result.markdown)
        return result

if __name__ == "__main__":
    neResult = asyncio.run(main())

# to be honest, i know a debug statement would be easier, but this is one of my perks 
# from higher informatics, when experimenting i prefer print statements :-)
print("URL page is: ")

# cross check if we got the right page
print(neResult.url)

# and mention we are done with the scraping, moving to get in the slow waiting mode for model run 
print("Crawler import done" )

# Using deepseek, more as it was by end of 2024 the best free model running on my
# verry modest local machine (in a VM....)
desiredModel='deepseek-r1:1.5b'

# this will be offcourse in the bot different, plan is to scrap reddit for 
# sentiment on coins
questionToAsk='Can you describe the weather for today in the netherlands? Use the weatherforcast as follows: '

# adding the scraped content. Can be heavily optimized by only extracting the weather part
# but for this experiment its not needed. Accepting its slow
questionToAsk = questionToAsk + neResult.markdown


# dummy overwrite to quick check if DS is running
# questionToAsk='hello who are you?' 

# Again print statement that we are done with the question and start the deepseeking
print("Model initialized successfull" )
print(questionToAsk
      )
# run the model.
response = ollama.chat(model=desiredModel, messages=[
  {
    'role': 'user',
    'content': questionToAsk,
  },
])


# print the output, in this case the weather clothing advise
# storing the response in a variable for later usage
print(" Response is: ")

OllamaResponse=response['message']['content']
print(OllamaResponse)

print (' and duration was:') 

# show also how much tokens this took in duration
print(response.total_duration)
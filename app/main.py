from flask import Flask, render_template, request
from .tools.web_scraping import get_urls
from .tools.web_scraping import web_scrape
from time import time

global_data = []

app = Flask(__name__)

@app.route("/")
def hello():
    return render_template('indexv2.html')



big_d = []


@app.route("/result", methods=["POST", "GET"])
def result():
  if request.method == "GET":
    # 1. Get the urls from the urls scraper
    movie_name = request.url.split('anime_name=')[1].strip()
    global_data.append(movie_name)
    urls = get_urls.method2(f'${movie_name} titles')

    # 2. Using the urls to scrape data, and get the data back.
    
    data = web_scrape.scrapeUrlsv2(urls)
    print([entry[0] for entry in data])
    big_d.append(data)
    global_data.append(data)


    # 3. Send data back and render it.
    return render_template('queries.html', data=data)

  return render_template('index.html')

@app.route("/filter/<name>")
def filters(name):
  data = big_d[0]
  if name in ['shounen', 'seinen', 'action', 'adventure', 'romance', 'isekai']:
    filtered_data = [anime for anime in data if name.title() in anime[4].split('!?|')]
  elif name in ['pg-13', 'r', 'r+', 'pg']:
    mapper = {
      'pg-13': 'PG-13 - Teens 13 or older',
      'r': 'R - 17+ (violence &amp; profanity)',
      'r+': 'R+ - Mild Nudity',
      'pg': 'PG - Children'
    }
    mapped_val = mapper[name]
    filtered_data = [anime for anime in data if mapped_val == anime[5]]
  else:
    lower_limit = int(name.split('-')[0])
    if 'current' in name:
      upper_limit = 2030
    else:
      upper_limit = int(name.split('-')[1])
    filtered_data = [anime for anime in data if anime[3].isdigit() and lower_limit <= int(anime[3]) <= upper_limit]
  print([entry[0] for entry in filtered_data])
  return render_template('queries.html', data=filtered_data)

# movie_name = global_data[0].replace('+', ' ')
# anime = global_data[1]
# with open(f'app/tools/web_scraping/searches.txt', 'a') as f:

#   f.write(f"{movie_name}|!? ")
#   f.close()

# for res in anime:
#   name = res[0]
#   with open(f'app/tools/web_scraping/chosen_anime.txt', 'a') as f:
          
#     f.write(f"{name}|!? ")
#     f.close()


# from app import app
# import urllib.request,json
# from .models import Quotes

# # Movie = movie.Movie


# # Getting api key
# def configure_request(app):
#     global base_url
#     base_url = app.config['QUOTES_API_BASE_URL']


# def get_quotes():
#     '''
#     Function that gets the json response to our url request
#     '''
  

#     with urllib.request.urlopen(get_quotes_url) as url:
#         get_quotes_data = url.read()
#         get_quotes_response = json.loads(get_quotes_data)

#         quote_results = None

#         if get_quotes_response:
#             author = get_quotes_response.get("author")
#             quote = get_quotes_response.get("quote")
#             quote_results = Quotes(author,quote)


#     return quote_results
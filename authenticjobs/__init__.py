import requests
import json

class AuthenticJobsClient(object):

  API_ENDPOINT = 'http://www.authenticjobs.com/api/'

  def __init__(self, api_key='', ajp_id=None):
    self.api_key = api_key
    self.ajp_id = ajp_id
    self.params = {
      'api_key': api_key,
      'format': 'json',
    }
  
  def get(self, method, **kwargs):
    ''' Makes a get request to AJ. Returns a Python dict of the results. '''
    params = self.params
    params['method'] = method
    params = dict(params.items() + kwargs.items())
    r = requests.get(self.API_ENDPOINT, params=params)
    return r.json

  def get_url_for_listing_id(self, listing_id):
    ''' Generates the URL for a listing based on its ID. Includes AJP ID if there is one. '''
    url = 'http://www.authenticjobs.com/' + listing_id
    if self.ajp_id:
      url = url + '?ajp=' + str(self.ajp_id)
    return url

  # The following methods map directly to AJ API methods.
  def jobs_getCompanies(self):
    method = 'aj.jobs.getCompanies'
    results = self.get(method)
    results_list = results['companies']
    return results_list

  def jobs_getLocations(self):
    method = 'aj.jobs.getLocations'
    results = self.get(method)
    results_list = results['locations']
    return results_list

  def jobs_search(self, **kwargs):
    method = 'aj.jobs.search'
    results = self.get(method, **kwargs)
    results_list = results['listings']['listing']

    # Add the URL for the listing since the AJ API doesn't include it.
    for listing in results_list:
      listing['url'] = self.get_url_for_listing_id(listing['id'])

    return results_list

  def types_getList(self):
    method = 'aj.types.getList'
    results = self.get(method)
    results_list = results['types']
    return results_list

  def categories_getList(self):
    method = 'aj.categories.getList'
    results = self.get(method)
    results_list = results['categories']
    return results_list


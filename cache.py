from ast import List
import json
import os
from ast import literal_eval

class Cache():
    def __init__(self, 
                 immediate_push:bool=False, 
                 use_file:bool=True#, 
#                 auto_execute_on_run:bool=True
                ):
        self.cache = {}
        # Files
        self.jobs = []
        self.cache_file = os.path.join(os.path.dirname(__file__), 'cache.json')
        # Check for cache file exist
        if use_file:
            if not os.path.exists(self.cache_file):
                # Create cache file
                with open(self.cache_file, 'w') as f:
                    json.dump(self.cache, f)
            if os.path.exists(self.cache_file):
                with open(self.cache_file, 'r') as file:
                    content = file.read()
                    if content=="":
                        self.cache = {
                            "cache": {}
                        }
                    else:
                        self.cache = json.loads(content)
        
        
        try:
          content = self.cache["cache"]
          for key in self.cache["cache"]:
            pass
        except:
          self.cache["cache"] = {}
        self.get_jobs()
        
        # Settings
        self.immediate_push = immediate_push
        self.use_file = use_file
        #self.auto_execute_on_run = auto_execute_on_run
        # Get settings
        

    def get_jobs(self):

          for key in self.cache["cache"]:
            self.jobs.append(key)

    def cache_push(self): # Push cache to file
        if self.use_file:
            with open(self.cache_file, 'w') as f:
                cache = self.cache
                
                content = json.dumps(cache)
                f.write(content)
                f.close()
    
                
    def add_job(self, data, id=None):
        
        # Add job to cache
        
        # Add to cache
        if id==None:
          # Create job ID
          length = len(self.jobs)
          id = length+1
        self.cache["cache"][id] = {
            "data": data,
        }
        if self.immediate_push and self.use_file:
            self.cache_push()
        self.get_jobs()
        return id
    
    def fetch_job(self, id):
        #returns = "" # list to return
        returns = (str(self.cache["cache"][id]["data"]))
        return returns
    
    def get_latest_job(self, execute:bool=True):
        self.get_jobs()
        length = len(self.jobs)-1
        key = self.jobs[length]
        #print(self.cache)
        cache = self.cache["cache"][key]
        #print(cache["function"])
        to_do = cache["data"]
        list = [key, to_do]
        return to_do
        self.delete_job(key)
        
        
    def delete_job(self, id):
        del self.cache["cache"][id]
    
#    def auto_execute_on_run(self):
#        if self.auto_execute_on_run:
#            for i in len(self.jobs):
#               job = self.do_next_job()
               
               
               
import github
from twilio.rest import Client

class ADILabs:
    
    def __init__(self):
        self.git_client = github.Github("username", "key-here")
        self.twilio_client = Client('key-here', 'key-here')
        self.index = 3
        self.pulls = []
        self.pull_counts = {}
        
    def get_all_repos(self):
        self.pulls = []
        count = 0
        for i in self.git_client.get_user().get_orgs()[self.index].get_repos():
            self.pulls.append(i.get_pulls('all'))
            self.pull_counts[count] = 0
            count += 1
            
    def set_pull_counts(self):
        count = 0 
        for repo in self.pulls:
            for j in repo:
                self.pull_counts[count] = self.pull_counts[count] + 1
            count += 1
    
    def check_counts(self):
	"""
	checks current number of pull requests against last update of pull requests
	returns: True or False (whether the number of pull requests is the same)
	"""
        counts_check = {}
        count = 0 
        for pl in self.git_client.get_user().get_orgs()[self.index].get_repos():
            pl_repos = pl.get_pulls('all')
            counts_check[count] = 0
            for repo in pl_repos:
                counts_check[count] = counts_check[count] + 1
            count += 1
        return self.pull_counts == counts_check
    
    def send_message(self):
        message = self.twilio_client.messages.create(
            to="+1number", # put numbers in +1XXXXXXXXXX format
            from_="+1number", 
            body="You have new pull requests for ADI Labs!")

if __name__ == "__main__":
    labs = ADILabs()
    labs.get_all_repos()
    labs.set_pull_counts()
    while True:
        if not labs.check_counts():
            labs.send_message()
            labs.pull_counts = {}
            labs.get_all_repos()
            labs.set_pull_counts()

import github
from twilio.rest import Client

class ADILabs:
    
    def __init__(self):
        self.g = github.Github("your-username", "your-key")
        self.client = Client(‘yourkey’, ‘your-key’)
        self.index = 3 # index for ADILabs org
        self.pulls = []
        self.pull_counts = {}
        
    def get_repos(self):
        count = 0
        for i in self.g.get_user().get_orgs()[self.index].get_repos():
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
        self.set_pulls_list()
        counts_check = {}
        count = 0 
        for repo in self.pulls:
            for j in repo:
                counts_check[count] = counts_check[count] + 1
            count += 1
        return self.pull_counts == counts_check
    
    def send_message(self):
        message = self.client.messages.create(
            to=""YOUR-NUMBER-HERE"", 
            from_="YOUR-TWILIO-NUMBER-HERE",
            body="You have new pull requests for ADI Labs!")
	
	
if __name__ == "__main__":
    labs = ADILabs()
    labs.get_repos()
    labs.get_pull_counts()
    while True:
        if not labs.check_counts():
            labs.send_message()

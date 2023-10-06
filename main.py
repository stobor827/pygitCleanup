import sys
from git import Git
from git import Repo

g = Git()
path = sys.argv[1]

print("start " + path)
r  = Repo(path)


def search(r, branch):
    return "search"

for h in r.branches:
    action = ""
    remote =  h.tracking_branch()
    if remote is not None:
        remoteName = remote.name
        if remote.is_valid():
            action = remoteName + " is synced with " + remote.path + ", do nothing."
        else:
            action = remoteName + " is 'gone': delete"  #search?
    else:
        #there are more efficient ways...
        action = search(r,h)

    

    print(h.name, action )
    

        



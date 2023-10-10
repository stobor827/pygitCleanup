import sys
from git import Git
from git import Repo
from git import Head
import argparse

parser = argparse.ArgumentParser(description="Inspect and clean up a repo")
parser.add_argument("path", help="path to the repo to analyze")
parser.add_argument("--destructive", help="delete dead branches", action="store_true")
args = parser.parse_args()

if( args.destructive) :
    print( "destructive mode!  branches will be deleted!")

g = Git()
path = args.path

print("start " + path)
r  = Repo(path)




if len(r.remotes) == 0:
    exit("error: no remotes on this repo!")
elif len(r.remotes) > 1:
    exit("error: more than one remote on this repo!")

if r.remotes[0].name != "origin":
    exit("error: remote is not named 'origin'")

if r.remotes[0].url.startswith("https://dev.azure.com") :
    exit("error: remote 'origin' is https azure!")
    #todo: fixup?

print( "git fetch --prune")
r.remotes[0].fetch(prune=True)


class branchInfo:
    def __init__(self, shouldDelete, message, branch):
        self.shouldDelete = shouldDelete
        self.message = message
        self.branch = branch

    def print(self):
        print( "  ",self.branch.name,  self.message, self.shouldDelete)

    shouldDelete: bool = False
    message : str = ""
    branch = None




def search(r, branch) :
    hcommit = branch.commit
    minDiffSize = 100
    minDiffCommit = ""
    for commit in r.iter_commits(rev='master'):
      diffSize = len(hcommit.diff(commit))
      if diffSize < minDiffSize:
          minDiffSize = diffSize
          minDiffCommit = commit.hexsha
      if diffSize == 0:
          return branchInfo (True, "found identical commit " + commit.hexsha, branch )

    return branchInfo(False, "did not find identical commit.  min: " + str(minDiffSize) + ", " + minDiffCommit, branch )
    #return "search"

def getInfo(h):
    remote =  h.tracking_branch()
    if remote is not None:
        remoteName = remote.name
        if remote.is_valid():
            action = branchInfo( False, remoteName + " is synced with " + remote.path, h )
        else:
            action = branchInfo( True, remoteName + " is 'gone'", h) 
    else:
        #there are more efficient ways...
        action = search(r,h)
    return action

info = list(map(getInfo,  r.branches))

print("")
save = list(filter(lambda d : not d.shouldDelete , info))
if len(save) > 0:
    print( "branches to save:")
    for elem in save:
        elem.print()

print("")
delete = list(filter(lambda d : d.shouldDelete , info))
if len(delete) > 0:
    print("branches to delete:")
    for elem in delete:
        elem.print()
        if args.destructive :
            print ("deleting branch " + elem.branch.name)
            r.delete_head(elem.branch, force=True)
    
    

    

#print(h.name, action.shouldDelete, action.message )
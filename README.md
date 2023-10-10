# pygitCleanup
Python project to analyze/cleanup stray branches in a git repo

For way too long I used a git client that encouraged me to push to remote branches without setting an upstream.  This combined with a pull-to-release workflow caused me to have a lot of orphaned branches that I wasn't sure if they were safe to delete.  

This tool scans local branches and looks for ones that are safe to delete.  
The rules are either:
  * If upstream is set, must be marked as 'gone'
  * The head of the branch must have 0 diffs to a commit in the master branch.

No deletes will happen until you pass the --destructive flag.  Debug info about which branches will be removed is printed without this flag for evaluation

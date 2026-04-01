#!/bin/bash
set -e

# Initialize a new jj repository in /home/user/octopus_sim
mkdir -p /home/user/octopus_sim
cd /home/user/octopus_sim
jj git init .
jj config set --repo user.name "Test User"
jj config set --repo user.email "test@example.com"

# Create a base commit with a file base.txt containing the text 'base'
echo "base" > base.txt
jj describe -m "base commit"

# Create three independent branches
jj bookmark create branch_a -r @
jj bookmark create branch_b -r @
jj bookmark create branch_c -r @

# In branch_a, create a file a.txt containing 'A'
jj new branch_a
echo "A" > a.txt
jj describe -m "branch_a commit"
jj bookmark set branch_a -r @

# In branch_b, create a file b.txt containing 'B'
jj new branch_b
echo "B" > b.txt
jj describe -m "branch_b commit"
jj bookmark set branch_b -r @

# In branch_c, create a file c.txt containing 'C'
jj new branch_c
echo "C" > c.txt
jj describe -m "branch_c commit"
jj bookmark set branch_c -r @

# Create a new commit that has branch_a, branch_b, and branch_c as its parents
jj new branch_a branch_b branch_c

# In this merge commit, add a file merge.txt containing 'merged'
echo "merged" > merge.txt
jj describe -m "octopus merge"

# Assign a bookmark named octopus_merge to this final merge commit
jj bookmark create octopus_merge -r @

# Output the revset of the final merge commit to /home/user/octopus_sim/merge_rev.log
jj log --no-graph -r octopus_merge -T commit_id > /home/user/octopus_sim/merge_rev.log

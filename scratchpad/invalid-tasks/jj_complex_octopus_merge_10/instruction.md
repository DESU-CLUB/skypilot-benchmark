You are participating in a training scenario for command option tradeoffs in jj. Your goal is to design and execute a multi-parent branching simulation (an octopus merge) using jj.

Here are your tasks:
1. Initialize a new jj repository in `/home/user/octopus_sim`.
2. Create a base commit with a file `base.txt` containing the text 'base'.
3. Create three independent branches (bookmarks) from the base commit named `branch_a`, `branch_b`, and `branch_c`.
4. In `branch_a`, create a file `a.txt` containing 'A'.
5. In `branch_b`, create a file `b.txt` containing 'B'.
6. In `branch_c`, create a file `c.txt` containing 'C'.
7. Create a new commit that has `branch_a`, `branch_b`, and `branch_c` as its parents (an octopus merge). Note that `jj new` accepts multiple revisions to create a merge commit.
8. In this merge commit, resolve any conflicts if they exist (they shouldn't for independent files), and add a file `merge.txt` containing 'merged'.
9. Assign a bookmark named `octopus_merge` to this final merge commit.
10. Output the revset of the final merge commit to `/home/user/octopus_sim/merge_rev.log` using `jj log --no-graph -r octopus_merge -T commit_id`.

Ensure all files are created correctly and the final commit has exactly three parents.
# Restore Working Copy Files in jj

## Background

You are a new developer who has just joined a software team that uses **jj** (Jujutsu) as its version control system. Your team lead has set up a repository for the project called `webserver` located at `/home/user/webserver`.

The repository contains a small web server project with the following files already committed:

- `README.md` — project overview
- `src/main.rs` — the main application source file
- `src/config.rs` — configuration handling
- `Cargo.toml` — Rust project manifest

The current state of the repository has two commits:
1. A commit with description **"initial project scaffold"** containing the four files above.
2. A second (currently empty) working-copy commit on top, with description **"add rate limiting feature"**, where you were supposed to implement the rate limiting feature.

## What Happened

While getting familiar with jj, you made some accidental edits. You opened several files to explore the codebase and accidentally made (and saved) changes to files you did not intend to modify. Specifically:

- You accidentally overwrote **`src/main.rs`** with some placeholder test content. The file now contains the text `TODO: placeholder - needs rewrite` instead of its original content.
- You accidentally deleted **`src/config.rs`** from the working copy.
- You intentionally edited **`README.md`** to add a note about yourself in the contributors section. You want to **keep this change**.

You now need to recover from these accidental changes.

## Your Goal

Using jj commands, you need to:

1. **Check the current state** of your working copy by running `jj status` (or `jj st`) to understand what files have been modified or deleted. Take note of which files are changed.

2. **Inspect the differences** for the files you accidentally changed by using `jj diff` to see exactly what is different between your working copy and the parent commit. Confirm that `src/main.rs` was accidentally modified and `src/config.rs` was deleted.

3. **Restore only the accidentally changed files** to their state from the parent commit. Use `jj restore` to restore `src/main.rs` and `src/config.rs` back to the content they had in the parent commit (commit with description "initial project scaffold"). Do NOT restore `README.md` — that intentional change must be preserved.

   - You should restore `src/main.rs` by running a command that specifies only that path.
   - You should restore `src/config.rs` by running a command that specifies only that path.
   - Alternatively, you may combine them into a single `jj restore` command that lists both paths.

4. **Verify the final state**: After restoring, run `jj status` again to confirm:
   - `src/main.rs` shows no changes (it should match the parent commit).
   - `src/config.rs` shows no changes (it should be present and match the parent commit).
   - `README.md` still appears as a modified file (your intentional change is preserved).

## Important jj Concepts for New Users

- In jj, the **working copy is always a commit** — there is no separate "unstaged" area like in Git.
- `jj status` (alias: `jj st`) shows what files differ between your working-copy commit and its parent.
- `jj diff` shows the actual content differences in your working copy vs. the parent commit.
- `jj restore <paths>` restores specific files in the working copy to match the parent commit's version of those files. This is similar to `git restore <paths>`.
- When you `jj restore` specific paths, only those paths are reset — other changes in the working copy are left intact.
- `jj restore` without any path arguments would reset ALL files to the parent state (which you do NOT want here, because that would undo your intentional `README.md` edit).

## Expected Final State

After completing the task:

- The working-copy commit (with description **"add rate limiting feature"**) should show only **`README.md`** as modified when you run `jj status`.
- `src/main.rs` in the working copy must contain its original content (a Rust `fn main()` that prints a startup message — specifically the line `println!("Starting webserver...");`).
- `src/config.rs` must exist in the working copy and contain its original content (a Rust struct `Config` with fields `host` and `port`).
- `README.md` must still contain the word `contributor` (from your intentional edit) — this file is intentionally different from the parent commit.
- The repository history (jj log) must still show exactly two commits: the "initial project scaffold" commit and the "add rate limiting feature" working-copy commit.

## Notes

- Do not use `jj abandon` or `jj undo` — restore the files using `jj restore` with explicit paths.
- Do not create any new commits (`jj new`, `jj commit`, etc.) as part of the restoration process.
- Work only within the existing `/home/user/webserver` repository.

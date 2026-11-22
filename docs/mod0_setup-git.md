MODULE 0 - PYTHON, SELENIUM AND GIT SETUP (MAC)


PART 0 - PYTHON AND SELENIUM


If you are on a Mac and already have Homebrew, make sure Python 3 is there:

```
brew install python
```

Get the project and create a virtual environment (keeps things clean):

```
cd ~/Documents
git clone https://github.com/vicvv/selenium-practice.git
cd selenium-practice
python3 -m venv venv
source venv/bin/activate
```

Install everything the project needs:

```
pip install -r requirements.txt
```

This installs the pinned versions of selenium, pytest and pytest-html, and also the project's own package (selenium_practice, which holds the page objects), because the last line of requirements.txt is -e .

Check it worked:

```
python -c "import selenium_practice.pages.mod5_pages; print('import OK')"
```

Every time you come back to work on this, cd into the selenium-practice folder and run source venv/bin/activate again. When you're done, type deactivate.

Starting from an empty folder instead of a clone? The minimum is: python3 -m venv venv, source venv/bin/activate, pip install selenium.



GIT + GITHUB SETUP NOTES (SSH) - MACOS


My setup: Mac, GitHub username vicvv, project folder selenium-practice, authenticated via SSH (no tokens in plain text). Default branch for this repo is "main".



PART 1 - ONE-TIME SSH SETUP (done once per machine)


1. Check for an existing SSH key:

```
ls -al ~/.ssh
```

   If "No such file or directory", you have none yet - create one.

2. Create an SSH key (use your GitHub email):

```
ssh-keygen -t ed25519 -C "your_github_email@example.com"
```

   - Press Enter to accept the default file location.
   - Passphrase is optional (Enter for none).
   - A "randomart" box means success.

3. Start the SSH agent and add the key:

```
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_ed25519
```

4. Copy the PUBLIC key to clipboard:

```
pbcopy < ~/.ssh/id_ed25519.pub
```

   Only ever share the .pub file. Never share the private key - the file with no extension.

5. Add the key to GitHub:

   - Go to https://github.com/settings/keys
   - New SSH key -> Title: a name for this computer, e.g. "MacBook - personal" -> Key type: Authentication Key
   - Paste (Cmd+V) -> Add SSH key

6. Test the connection:

```
ssh -T git@github.com
```

   - Type "yes" the first time.
   - Success looks like: "Hi vicvv! You've successfully authenticated..."
   - "does not provide shell access" is normal, NOT an error.

7. Keep your email private (recommended for public repos):

   Every commit stores the author's name and email, and on a public repo anyone can read them. On GitHub: Settings -> Emails -> tick "Keep my email addresses private", and copy the no-reply address it shows. Then set it for this repo:

```
git config user.email "<your-id>+vicvv@users.noreply.github.com"
```

   Use the exact address GitHub shows. Without --global, it applies to this repo only. Commits made on the GitHub website use it automatically once the setting is on.



PART 2 - SET UP GIT IN A PROJECT FOLDER (once per project)


1. Go into the project folder:

```
cd ~/Documents/selenium-practice
```

2. Initialise Git:

```
git init -b main
```

3. Create a .gitignore so junk (like the venv) is never committed:

```
cat > .gitignore << 'EOF'
# Python virtual environment
venv/
.venv/
# Python cache
__pycache__/
*.pyc
.pytest_cache/
# Python packaging (created by pip install -e .)
*.egg-info/
build/
dist/
# Test output
screenshots/
reports/
report.html
test-run.log
# Secrets
.env
# macOS junk
.DS_Store
# IDE settings
.vscode/
.idea/
EOF
```

4. Record the pinned packages - MUST be inside the venv:

```
source venv/bin/activate      # prompt shows (venv)
pip freeze | grep -i -E "^(selenium|pytest|pytest[-_]html)==" > requirements.txt
echo "-e ." >> requirements.txt
cat requirements.txt
```

   - Outside the venv there is no "pip" - use the venv so only project packages are listed.
   - Do not use plain pip freeze > requirements.txt in this project. After the editable install it writes a line with the full path to your own folder, which breaks for everyone else and puts your username in a public file.

5. Stage, check, and commit:

```
git add .
git status            # venv/ and *.egg-info/ should NOT appear here
git status --ignored  # venv/ SHOULD appear under "Ignored files"
git commit -m "Initial Selenium practice setup"
```



PART 3 - PUSH TO GITHUB (first time for a new repo)


1. Create an EMPTY repo on GitHub:

   - https://github.com/new
   - Name: selenium-practice
   - Do NOT add README, .gitignore, or license (keeps it empty to avoid conflicts).
   - Create repository.

2. Connect the local repo and push (SSH URL - note the "git@" prefix):

```
git remote add origin git@github.com:vicvv/selenium-practice.git
git push -u origin main
```

   -u links your local main to main on GitHub. It is needed once. After that, plain git push and git pull work.



PART 4 - EVERYDAY GIT WORKFLOW (after setup)


Each coding session:

```
cd ~/Documents/selenium-practice
source venv/bin/activate      # only needed to run Python, not for Git
git pull                      # get any changes made on GitHub first
```

After making changes:

```
git status                    # see what changed
git add .                     # stage all changes
git commit -m "describe what you did"
git push                      # send to GitHub
```

If you install or upgrade a package, update requirements.txt (inside venv) with the commands in Part 2, step 4, then:

```
git add requirements.txt
git commit -m "Update dependencies"
git push
```

Make changes in one place: either on your Mac or on the GitHub website, not both at the same time. Editing in both places gives "divergent branches" (Part 5).



PART 5 - COMMON GIT FIXES (when things go sideways)


See what's going on

```
git status                 # what's changed/staged
git log --oneline          # compact history of commits
git log --oneline -5       # last 5 commits only
git diff                   # see unstaged changes
git diff --staged          # see staged changes
```

Fix the last commit message (typo in message, already committed, NOT pushed)

```
git commit --amend -m "the corrected message"
```

   WARNING: if you already pushed it, amending rewrites history. Only amend commits you have NOT pushed.

Add a forgotten file to the last commit (not pushed yet)

```
git add forgotten_file.py
git commit --amend --no-edit
```

   --no-edit keeps the existing message.

Unstage a file (you ran "git add" but changed your mind)

```
git restore --staged filename.py
```

   The file keeps your edits; it's just no longer staged.

Discard changes to a file (throw away edits, go back to last commit)

```
git restore filename.py
```

   WARNING: this permanently deletes your unsaved edits to that file.

Discard all uncommitted changes (nuclear - back to last commit)

```
git restore .
```

   WARNING: wipes all uncommitted edits. Can't undo.

Undo the last commit but keep the changes (commit was premature)

```
git reset --soft HEAD~1
```

   The commit is removed; your changes return to "staged". Good for re-doing a commit.

Undo the last commit and unstage the changes (keep edits, start over)

```
git reset HEAD~1
```

   Changes stay in your files but become unstaged.

Move or rename a file, keeping its history

```
git mv old/path.py new/path.py
```

I accidentally committed the venv (or other junk)

   Make sure it's in .gitignore first (see Part 2, step 3), then:

```
git rm -r --cached venv
git commit -m "Stop tracking venv"
git push
```

   --cached removes it from Git but KEEPS it on your disk.

"You have divergent branches" when pulling (GitHub and your Mac both have new commits)

```
git pull --rebase
git push
```

   To make rebase the default for this repo: git config pull.rebase true

I committed a secret (token/password) - don't just delete it

   - Removing it in a new commit does NOT erase it from history.
   - Rotate/revoke the secret on the provider immediately.
   - Then ask for help cleaning history (git filter-repo or BFG).

Set up your name/email (one-time, if Git ever complains on commit)

```
git config --global user.name "Your Name"
git config --global user.email "your_github_email@example.com"
```

See / change the remote URL

```
git remote -v                 # show current remote
git remote set-url origin git@github.com:vicvv/selenium-practice.git
```



KEY THINGS TO REMEMBER


- python3 / pip3 -> outside the venv (on Mac)
- python / pip -> work inside the venv once activated ((venv) shows)
- Git works the same whether or not the venv is activated.
- Never commit venv/ - it's recreated with: pip install -r requirements.txt
- requirements.txt ends with -e . so the same command also installs the selenium_practice package.
- SSH means no token is stored in .git/config. The remote URL is git@github.com:..., not https://...
- This repo's default branch is "main".
- Run "pwd" before any "git init" or "git remote" command to be sure you're in the right folder.
- "WARNING" steps above can delete work - read before running.
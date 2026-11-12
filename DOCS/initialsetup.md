# If you are on Mac and you already have Homebrew. Make sure Python 3 is there:
brew install python

# Create a project folder + virtual environment (keeps things clean)
mkdir selenium-practice && cd selenium-practice
python3 -m venv venv
source venv/bin/activate

# Install Selenium
pip install selenium

Every time you come back to work on this, just cd selenium-practice and 
run source venv/bin/activate again. When you're done, type deactivate.

========================================================
GIT + GITHUB SETUP NOTES (SSH) — macOS
========================================================

My setup: Mac (user user), GitHub username vicvv,
project folder selenium-practice, authenticated via SSH
(no tokens in plain text). Default branch for this repo is "main".


--------------------------------------------------------
PART 1 — ONE-TIME SSH SETUP (done once per machine)
--------------------------------------------------------

1. Check for an existing SSH key:
   ls -al ~/.ssh
   (If "No such file or directory", you have none yet — create one.)

2. Create an SSH key (use your GitHub email):
   ssh-keygen -t ed25519 -C "your_github_email@example.com"
   - Press Enter to accept the default file location.
   - Passphrase is optional (Enter for none).
   - A "randomart" box means success.

3. Start the SSH agent and add the key:
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519

4. Copy the PUBLIC key to clipboard:
   pbcopy < ~/.ssh/id_ed25519.pub
   (Only ever share the .pub file. Never share the private
   key — the file with no extension.)

5. Add the key to GitHub:
   - Go to https://github.com/settings/keys
   - New SSH key -> Title: "MacBook – user"
     -> Key type: Authentication Key
   - Paste (Cmd+V) -> Add SSH key

6. Test the connection:
   ssh -T git@github.com
   - Type "yes" the first time.
   - Success looks like: "Hi vicvv! You've successfully authenticated..."
   - ("does not provide shell access" is normal, NOT an error.)


--------------------------------------------------------
PART 2 — SET UP GIT IN A PROJECT FOLDER (once per project)
--------------------------------------------------------

1. Go into the project folder:
   cd selenium-practice

2. Initialise Git:
   git init

3. Create a .gitignore so junk (like the venv) is never committed:
   cat > .gitignore << 'EOF'
   # Python virtual environment
   venv/
   .venv/
   # Python cache
   __pycache__/
   *.pyc
   # macOS junk
   .DS_Store
   # IDE settings
   .vscode/
   .idea/
   EOF

4. (Recommended) Record installed packages — MUST be inside the venv:
   source venv/bin/activate      (prompt shows (venv))
   pip freeze > requirements.txt
   (Outside the venv there is no "pip" — use the venv so only
   project packages are listed.)

5. Stage, check, and commit:
   git add .
   git status            (venv/ should NOT appear here)
   git status --ignored  (venv/ SHOULD appear under "Ignored files")
   git commit -m "Initial Selenium practice setup"


--------------------------------------------------------
PART 3 — PUSH TO GITHUB (first time for a new repo)
--------------------------------------------------------

1. Create an EMPTY repo on GitHub:
   - https://github.com/new
   - Name: selenium-practice
   - Do NOT add README, .gitignore, or license
     (keeps it empty to avoid conflicts).
   - Create repository.

2. Connect the local repo and push (SSH URL — note the "git@" prefix):
   git remote add origin git@github.com:vicvv/selenium-practice.git
   git branch -M main
   git push -u origin main


--------------------------------------------------------
PART 4 — EVERYDAY GIT WORKFLOW (after setup)
--------------------------------------------------------

Each coding session:
   cd selenium-practice
   source venv/bin/activate      (only needed to run Python, not for Git)

After making changes:
   git status                    (see what changed)
   git add .                     (stage all changes)
   git commit -m "describe what you did"
   git push                      (send to GitHub; just "git push"
                                  after the first time)

If you added new Python packages, update requirements.txt (inside venv):
   pip freeze > requirements.txt
   git add requirements.txt
   git commit -m "Update dependencies"
   git push


--------------------------------------------------------
PART 5 — COMMON GIT FIXES (when things go sideways)
--------------------------------------------------------

SEE WHAT'S GOING ON
   git status                 (what's changed/staged)
   git log --oneline          (compact history of commits)
   git log --oneline -5       (last 5 commits only)
   git diff                   (see unstaged changes)
   git diff --staged          (see staged changes)

FIX THE LAST COMMIT MESSAGE (typo in message, already committed, NOT pushed)
   git commit --amend -m "the corrected message"
   (WARNING: if you already pushed it, amending rewrites history.
    Only amend commits you have NOT pushed.)

ADD A FORGOTTEN FILE TO THE LAST COMMIT (not pushed yet)
   git add forgotten_file.py
   git commit --amend --no-edit
   (--no-edit keeps the existing message.)

UNSTAGE A FILE (you ran "git add" but changed your mind)
   git restore --staged filename.py
   (The file keeps your edits; it's just no longer staged.)

DISCARD CHANGES TO A FILE (throw away edits, go back to last commit)
   git restore filename.py
   (WARNING: this permanently deletes your unsaved edits to that file.)

DISCARD ALL UNCOMMITTED CHANGES (nuclear — back to last commit)
   git restore .
   (WARNING: wipes all uncommitted edits. Can't undo.)

UNDO THE LAST COMMIT BUT KEEP THE CHANGES (commit was premature)
   git reset --soft HEAD~1
   (The commit is removed; your changes return to "staged".
    Good for re-doing a commit.)

UNDO THE LAST COMMIT AND UNSTAGE THE CHANGES (keep edits, start over)
   git reset HEAD~1
   (Changes stay in your files but become unstaged.)

I ACCIDENTALLY COMMITTED THE VENV (or other junk)
   - Make sure it's in .gitignore first (see Part 2, step 3), then:
   git rm -r --cached venv
   git commit -m "Stop tracking venv"
   git push
   (--cached removes it from Git but KEEPS it on your disk.)

I COMMITTED A SECRET (token/password) — DON'T JUST DELETE IT
   - Removing it in a new commit does NOT erase it from history.
   - Rotate/revoke the secret on the provider immediately.
   - Then ask for help cleaning history (git filter-repo or BFG).

SET UP YOUR NAME/EMAIL (one-time, if Git ever complains on commit)
   git config --global user.name "Your Name"
   git config --global user.email "your_github_email@example.com"

SEE / CHANGE THE REMOTE URL
   git remote -v                 (show current remote)
   git remote set-url origin git@github.com:vicvv/selenium-practice.git


--------------------------------------------------------
KEY THINGS TO REMEMBER
--------------------------------------------------------

- python3 / pip3  -> outside the venv (on Mac)
- python / pip    -> work inside the venv once activated ((venv) shows)
- Git works the same whether or not the venv is activated.
- Never commit venv/ — it's recreated from requirements.txt via:
     pip install -r requirements.txt
- SSH means no token is stored in .git/config.
  The remote URL is git@github.com:..., not https://...
- This repo's default branch is "main".
  (Note: my my notes app/ExampleVendor repos use "master" — don't mix them up.)
- Run "pwd" before any "git remote" command to be sure
  you're in the right folder.
- "WARNING" steps above can delete work — read before running.
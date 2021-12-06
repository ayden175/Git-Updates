import os
import sys
from datetime import datetime
import git

class GitCommands():
    def __init__(self, command, dir=".", correction_dir="Korrekturen", correction_file_prefix="korrektur_"):
        self.dir = dir
        self.correction_dir = correction_dir
        self.correction_file_prefix = correction_file_prefix

        now = datetime.now()
        self.log_folder = "_logs"
        self.log_filename = now.strftime(f"log-%d_%m_%Y-%H_%M_%S-{command}.txt")
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)
        self.log_file = open(os.path.join(self.log_folder, self.log_filename), 'w+')


    def pull(self):
        print("Pulling all repositories...")

        for dir in os.listdir(self.dir):
            if not os.path.isdir(dir) or dir == self.log_folder:
                continue

            repo = git.cmd.Git(os.path.join(self.dir, dir))
            try:
                output = repo.pull()
            except git.exc.GitCommandError as e:
                output = str(e)

            if "Already up to date" in output:
                msg = "Already up to date"
            elif "file changed, " in output or "files changed, " in output:
                part = output.split("\n")
                msg = part[-1][1:]
            elif "error: Pulling is not possible because you have unmerged files" in output:
                msg = "Error: Conflict with committed files"
            elif "error: Your local changes" in output:
                msg = "Error: Conflict with local files"
            elif "but no such ref was fetched." in output:
                msg = "Error: No branch seems to be specified"
            else:
                msg = output

            log = f"{dir} - {msg}"
            print(log)
            self.log_file.write(log + "\n")

        self.log_file.close()


    def commit(self, number):
        print(f"Committing correction number {number}...")

        for dir in os.listdir(self.dir):
            if not os.path.isdir(dir) or dir == self.log_folder:
                continue

            repo = git.cmd.Git(os.path.join(self.dir, dir))
            folder_found = True

            # search and stage files
            staged_files = {}
            try:
                for file in os.listdir(os.path.join(self.dir, dir, self.correction_dir)):
                    if self.correction_file_prefix + number in file:
                        file_path = os.path.join(self.correction_dir, file)
                        staged_files[file_path] = file
                        repo.add(file_path)

            except FileNotFoundError:
                msg = f"Error: No folder named {self.correction_dir} was found"
                folder_found = False

            if folder_found:
                # check what was actually staged
                modified = False
                status = repo.status("--porcelain")
                committed_files = []
                for file in staged_files.keys():
                    if f"A  {file}" in status or f"M  {file}" in status:
                        committed_files.append(staged_files[file])
                        if f"M  {file}" in status:
                            modified = True

                # commit and generate message
                if len(committed_files) > 0:
                    commit_msg = f"{'Update ' if modified else ''}Korrektur Übung {number}"
                    repo.commit("-m " + commit_msg)
                    msg = f"Committed {'update for ' if modified else ''}{', '.join(committed_files)}"

                elif len(staged_files) > 0:
                    file_is_committed = False
                    show_output = repo.show("--name-only", "--oneline", "HEAD")
                    for file in staged_files.keys():
                        if file in show_output:
                            file_is_committed = True
                            break

                    if file_is_committed:
                        msg = f"Already committed {', '.join(staged_files.values())}"
                    else:
                        msg = f"Already up to date: {', '.join(staged_files.values())}"

                else:
                    msg = "Nothing to commit was found"

            log = f"{dir} - {msg}"
            print(log)
            self.log_file.write(log + "\n")

        self.log_file.close()


    def push(self):
        print("Pushing all commits...")

        for dir in os.listdir(self.dir):
            if not os.path.isdir(dir) or dir == self.log_folder:
                continue

            repo = git.cmd.Git(os.path.join(self.dir, dir))

            try:
                output = repo.push("--porcelain")
            except git.exc.GitCommandError as e:
                output = str(e)

            if "[up to date]" in output:
                msg = "Nothing to push"
            elif "[rejected]" in output:
                msg = "Error: Conflicting changes"
            elif "error: src refspec" in output:
                msg = "Error: No branch seems to be specified"
            elif "Done" in output:
                msg = "Successful push"
            else:
                msg = output

            log = f"{dir} - {msg}"
            print(log)
            self.log_file.write(log + "\n")

        self.log_file.close()


    def clean(self):
        choice = input("This will delete all uncommited changes, this action cannot be reverted. Are you sure? [yes/N]\n")
        if choice != "yes":
            return

        print("Deleting all uncommited changes...")

        for dir in os.listdir(self.dir):
            if not os.path.isdir(dir) or dir == self.log_folder:
                continue

            repo = git.cmd.Git(os.path.join(self.dir, dir))

            status = repo.status("--porcelain")
            try:
                repo.restore(".")
                output_clean = repo.clean("-fdx")
            except git.exc.GitCommandError as e:
                output_clean = str(e)

            if "is unmerged" in output_clean:
                msg = "Error: Merge in progress"
            elif "error: pathspec '.' did not match any file(s) known to git" in output_clean:
                msg = "Error: No branch seems to be specified"
            elif not status:
                msg = "Already clean"
            elif not "M" in status and output_clean:
                msg = "Deleted untracked files"
            elif output_clean:
                msg = "Restored files and deleted untracked files"
            else:
                msg = "Restored files"

            log = f"{dir} - {msg}"
            print(log)
            self.log_file.write(log + "\n")

        self.log_file.close()


    def show(self):
        print("Showing latest commit...")

        for dir in os.listdir(self.dir):
            if not os.path.isdir(dir) or dir == self.log_folder:
                continue

            repo = git.cmd.Git(os.path.join(self.dir, dir))

            try:
                output = repo.show("-q")
                lines = output.split("\n")
                author = lines[1].split(" <")[0][8:]
                date = lines[2].split(" +")[0][8:]
                commit_msg = lines[4][4:]

                msg = f"{date}, {author}: {commit_msg}"

            except git.exc.GitCommandError:
                msg = "No commits yet"

            log = f"{dir} - {msg}"
            print(log)
            self.log_file.write(log + "\n")

        self.log_file.close()

if __name__ == "__main__":
    commands = ["pull", "commit", "push", "clean", "show"]

    if len(sys.argv) > 1:
        command = sys.argv[1]
    else:
        command = ""

    while not command in commands:
        if command != "":
            print("Command not recognized, please try again.")
        command = input("Do you want to pull, commit, clean, push or show the last commit?\n")

    args = []
    if command == "commit":
        if len(sys.argv) > 2:
            args.append(sys.argv[2])
        else:
            args.append(input("Which correction do you want to commit?\n"))

    git_commands = GitCommands(command=command, dir=".", correction_dir="Korrekturen", correction_file_prefix="korrektur_")
    getattr(git_commands, command)(*args)

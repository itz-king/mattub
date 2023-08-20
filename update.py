from subprocess import run as srun
from os import ospath

UPSTREAM_REPO,UPSTREAM_BRANCH="https://github.com/itz-king/mattub","main"
if ospath.exists(".git"):
        srun(["rm", "-rf", ".git"])
with open('.env') as f:
    env=f.read()
update = srun(
        [
            f"git init -q \
                     && git config --global user.email evendeadiamthehero04@gmail.com \
                     && git config --global user.name evendeadiamthehero04 \
                     && git add . \
                     && git commit -sm update -q \
                     && git remote add origin {UPSTREAM_REPO} \
                     && git fetch origin -q \
                     && git reset --hard origin/{UPSTREAM_BRANCH} -q"
        ],
        shell=True,
    )

if update.returncode == 0:
        print("Successfully Updated The Bot !!!")
        with open('env','w') as f:
            f.write(env)
else:
        print(
            "Something went wrong while updating, check UPSTREAM_REPO if valid or not!"
        )
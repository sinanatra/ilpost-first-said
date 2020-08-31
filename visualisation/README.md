### Setup

This repo is my own yarn starterkit, to start create a bare clone of the repository:

`git clone --bare git@github.com:sinanatra/yarn-starterkit.git `

Mirror-push to the new repository:

`cd yarn-starterkit.git`

` git push --mirror  git@github.com:NEWREPOSITORY`

Remove the temporary local repository you created earlier:

`cd ..`

`rm -rf yarn-starterkit.git`

Then clone the new repository launch `yarn` to install the dependencies and `yarn watch` to launch the server

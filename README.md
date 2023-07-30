# Fork for Amy

Original documentation can be found here: [Amy Github](https://github.com/carpentries/amy). All documentation applies.

## Fork changes

This is a living list of changes which this fork contains.

- Added management command to import/change Tag objects
- Added different default list of curriculum in seed scripts
- Renamed Events to Schools
- Renamed Organisations to Hosts 
- Renamed Memberships to Sponsors 
- Couple of other small renames
- Changed bulk import to also import affiliation, position, and country.

## Building docker

Building the docker image is the same as described in Amy documentation at present:

```
$ LAST_COMMIT=`git rev-parse --short HEAD`
$ docker build -t amy:latest -t amy:${LAST_COMMIT} --label commit=${LAST_COMMIT} -f docker/Dockerfile .
```

## Deployment

Deployment is presently done manually (vimming into file and updating version of amy image, then running `docker compose up -d`). However, this can be fully automated (and will be) in a production setting using Github Actions runner on VM. In short:

1. Use ssh to enter machine
2. Goto `/data/amy-deployment`
3. Update tag in `docker-compose.yml`
4. `docker compose up -d`

Presently, the test environment is running with DigitalOcean in Amsterdam.

### Deploying changes to tags, curriculi, etch

Most of these changes are (intentionally) present within the management commands. Calling these management commands must be called from Amy's virtual environment.

In order to apply these changes to the existing env, do the following:

- Do a deployment, as noted above. Simply update the tag of the docker containers for amy, the rqworker and rqscheduler, and `docker compose up -d`
- Once all container are up:
- `docker exec -it <amy container name> bash`
- `source /venv/amy/bin/activate`
- `python manage.py <management_command_name>`

The name of the management command is the same as the filename, minus `.py`. You can also request `python manage.py help` to get a list of management commands.

## Development

- Be very careful with model changes/migrations; Django manages it's own migrations, so your migrations cannot be on top in this construction. The current renaming stuff will cause tests to fail (since Amy has a check to confirm all migrations are applied, and technically these changes would "change" certain table names but that's wholly optional). If you can - make management commands for the changes you want to run, or update existing files.

<img src="https://github.com/tvanerven/materialsfrontend/raw/main/eu_logo.png" width="64" height="47">This project has received funding from the European Union’s Horizon 2020 research and innovation programme under grant agreement No 101017536. The funding was awarded through the RDA (https://www.rd-alliance.org/) Open Call mechanism (https://eoscfuture-grants.eu/provider/research-data-alliance) based on evaluations of external, independent experts.



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

Deployment is presently done manually (vimming into file and updating version of amy image, then running `docker compose up -d`). However, this can be fully automated (and will be) in a production setting using Github Actions runner on VM.

Presently, the test environment is running with DigitalOcean in Amsterdam.

## Development

- Be very careful with model changes/migrations; Django manages it's own migrations, so your migrations cannot be on top in this construction. The current renaming stuff will cause tests to fail (since Amy has a check to confirm all migrations are applied, and technically these changes would "change" certain table names but that's wholly optional). If you can - make management commands for the changes you want to run, or update existing files.

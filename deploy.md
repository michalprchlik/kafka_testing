# Initial steps

Make sure, you completed [Linux - initial configuration](https://github.kyndryl.net/amtools/SAM_development_board/wiki/Linux---intial-configuration) and [Linux - deploy backend and frontend](https://github.kyndryl.net/amtools/SAM_development_board/wiki/Openshift---deploy-backend-and-frontend) steps in advance

# Deployment

### Clone git repository

Clone repository to your local machine. Check [changelog](https://github.kyndryl.net/amtools/SAM_development_board/wiki/Changelog) for latest version. You will use this version in `git checkout` command.

```
cd /sam_at_kyndryl/code
git clone git@github.kyndryl.net:amtools/sam-at-kyndryl-loader-aic.git
cd sam-at-kyndryl-loader-aic
git checkout 1.0.0
```

### Configure AIC loader

Update `config/config.env` with connection information to SFS, backend

```
SFS_URL=sfs_url:443
SFS_AUTHENTICATION_TYPE=password/token
SFS_LOGIN=sfs_login
SFS_PASSWORD=sfs_password
SFS_TOKEN=sfs_token
BACKEND_URL=backend_url:443
ORGANIZATION_LIST=xxx
ARCHIVE_FILES_AFTER_DOWNLOAD=false
```

- `SFS_URL` - URL for SFS in format `https://<SFS_URL>:443`
- `SFS_AUTHENTICATION_TYPE` which authentication method for SFS connection will be used. Possible values: 
  - `password` - `SFS_LOGIN` and `SFS_PASSWORD` will be used to authenticate to SFS. 
  - `token` - authentication with `SFS_TOKEN` will be used.
- `SFS_LOGIN` - username on SFS. This value will be used only for `SFS_AUTHENTICATION_TYPE=password`
- `SFS_PASSWORD` - password for user on SFS. This value will be used only for `SFS_AUTHENTICATION_TYPE=password`
- `SFS_TOKEN` - token to authenticate on SFS. Token has to be configured in SFS config files. This value will be used only for `SFS_AUTHENTICATION_TYPE=token`
- `BACKEND_URL` - URL of backend REST API. 
    - If backend container `sam_backend_dev`/`sam_backend_production` runs on the same computer as AIC loader, it will use HTTP connection to access REST API and the value will be `http://localhost:8184`
    - If backend container `sam_backend_dev`/`sam_backend_production` runs on a different computer than AIC loader, it will use HTTPS connection to access REST API and the value will be `https://<IP_OF_BACKEND_SERVER>:8084`
- `ORGANIZATION_LIST` - list of Organizations (GSMA codes) to be downloaded from SFS. Possible values: 
  - `*` - all Organizations will be processed. 
  - `XXX` - only `XXX` organization will be processed. 
  - `XXX,YYY,ZZZ` - 3 different Organization will be processed
  - there is no option to exclude an Organization
- `ARCHIVE_FILES_AFTER_DOWNLOAD` - enables/disables automatic archivation of downloaded scan files from SFS. Possible values:
  - `true` - files will be archived on SFS. Folowing script's executions will not process same data again. 
  - `false` - archiving of scan files is disabled

### Set permission on *.env file

To protect configuration `config/config.env` file, set up permissions on the file

```
chmod 660 /sam_at_kyndryl/code/sam-at-kyndryl-loader-aic/config/config.env
```

### SFS URL requires entry in /etc/hosts

In case, SFS is defined with domain name and not IP address, you will have to modify `podman run` command in [Makefile](https://github.kyndryl.net/amtools/sam-at-kyndryl-loader-aic/blob/dev/Makefile). Add new parameter `--add-host` in format `--add-host=host:ip`. 

For example: SFS runs with DNS name `sfs.kyndryl.com` on IP `1.1.1.1`, the parameter should look like `--add-host=sfs.kyndryl.com:1.1.1.1` and the first part of `podman run` command in Makefile will look like:

```
run-loader:
	podman build -t aic_loader -f aic_loader.containerfile .
	podman run \
	-d \
	--name=sam_loader_aic \
	-v /sam_at_kyndryl/data/standalone:/home/appuser/standalone:Z \
	-v /sam_at_kyndryl/data/gw_cache:/home/appuser/gw_cache:Z \
        --add-host=sfs.kyndryl.com:1.1.1.1 \
        ...
```

### Run container for AIC loader

Below command will start AIC loader in container. If configured correctly, it will connect to SFS configured in `config/config.env` file, downloads data and it will send scan data to backed REST API

```
make run-loader
```

# Multiple AIC loaders

If your deployment contains multiple SFS servers connected to one ILMT server, you should run multiple AIC loaders. One for every SFS. To achieve correct behavior, you should rename AIC loader's directory after you `git clone` the repository. You should also rename container's name, co it will contain name of SFS

### Example

Let's say, we have 2 SFS - Alita and Mickey_mouse. The commands will be slightly different than in above guide

```
cd /sam_at_kyndryl/code
git clone git@github.kyndryl.net:amtools/sam-at-kyndryl-loader-aic.git
mv sam-at-kyndryl-loader-aic sam-at-kyndryl-loader-aic-alita
cd sam-at-kyndryl-loader-aic-alita
git checkout 1.0.0
```

Update `config/config.env` with correct credentials and URL to Alita SFS

Update container's name by editing [Makefile](https://github.kyndryl.net/amtools/sam-at-kyndryl-loader-aic/blob/dev/Makefile) so it will look like this:

```
run-loader:
	podman build -t aic_loader -f aic_loader.containerfile .
	podman run \
	-d \
	--name=sam_loader_aic_alita \
...
```

Start the loader

```
make run-loader
```

And the same will be done also with Mickey_mouse SFS

```
cd /sam_at_kyndryl/code
git clone git@github.kyndryl.net:amtools/sam-at-kyndryl-loader-aic.git
mv sam-at-kyndryl-loader-aic sam-at-kyndryl-loader-aic-mickey-mouse
cd sam-at-kyndryl-loader-aic-mickey-mouse
git checkout 1.0.0
```
Update `config/config.env` with correct credentials and URL to Mickey_mouse SFS

Update container's name by editing [Makefile](https://github.kyndryl.net/amtools/sam-at-kyndryl-loader-aic/blob/dev/Makefile) so it will look like this:

```
run-loader:
	podman build -t aic_loader -f aic_loader.containerfile .
	podman run \
	-d \
	--name=sam_loader_aic_mickey_mouse \
...
```

Start the loader

```
make run-loader
```

# Post installation configuration

No crontab entry for loader is needed. Once the loader starts running, it sleeps for 30 minutes after finishing and then starts again.
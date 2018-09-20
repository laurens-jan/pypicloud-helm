# Helm chart for pypicloud
This helm chart installs pypicloud. It uses Google Cloud Storage as default backend, and by default redis for caching.

By default two users are created. An `admin` with read/write priviledges, and a `user` with read priviledges.

## Installing

### Setup google cloud storage bucket
- Create service account 'pypicloud', download json access key
 - create bucket %GKE_PROJECT%-pypicloud
 - give service account 'storage admin' access to bucket %GKE_PROJECT%-pypicloud
- Create a secret from the json access key:
 + `kubectl create secret generic pypicloud-gcs -n <NAMESPACE> --from-file=service_key.json`
 + This secret will be mounted in the pod at /etc/pypicloud-secret

### Setup credentials
Create a secret with fields userAdmin, userUser, sessionEncryptKey, sessionValidateKey
__secret-env.yaml__
`
apiVersion: v1
kind: Secret
metadata:
  name: pypicloud-env
type: Opaque
data:
  userUser: <FILL_OUT, see below>
  userAdmin: <FILL_OUT, see below>
  sessionEncryptKey: <FILL_OUT, see https://pypicloud.readthedocs.io/en/latest/topics/configuration.html#session-encrypt-key>
  sessionValidateKey: <FILL_OUT, see https://pypicloud.readthedocs.io/en/latest/topics/configuration.html#session-encrypt-key>
`

#### Generate a certificate for userUser and userAdmin
__Create a hashed password:__
`
pip install pypicloud
python
>> import pypicloud.scripts
>> pypicloud.scripts.gen_password()
`

__Base64 encode the hashed password:__
`echo -n "THEHASHEDPASSWORD" | base64`

#### Upload the secret
`kubectl apply -f secret-env.yaml`

### Create a settings.yaml
To see which values are available see also values.yaml

__settings.yaml__
`
env:
  - name: PROJECT_ID
    value: <GKE PROJECT NAME>
  - name: REGION
    value: <GKE REGION>
gcsSecret: pypicloud-gcs
envSecret: pypicloud-env
`

### Modify config.ini
Walk through `config\config.ini` to see if all settings are applicable. Environment substitution is applied before running the server. (e.g. $USER_ADMIN is replaced by the environment variable USER_ADMIN)
All files in this folder will be mounted within the pod at /etc/pypicloud/

### Deploy the helm chart
`helm upgrade --install pypicloud pypicloud -n <NAMESPACE> -f settings.yaml`

## Using google cloud build to upload to pypi repository
An example `cloudbuild.yaml` is provided which can be used in any repository with google cloud build. A build trigger based on tag can be created. This tag can in turn be read by `setup.py` in order to create a version based on a git tag.
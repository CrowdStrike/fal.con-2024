# Lab 1: Installing the Collection

## Installation

To install the collection, you can use the `ansible-galaxy` command line tool. This tool is installed with Ansible by default.

> [!NOTE]
> To view the full installation documentation, including how to install a specific version of the collection, see the [CrowdStrike Falcon Collection Installation Guide](https://github.com/CrowdStrike/ansible_collection_falcon?tab=readme-ov-file#installing-this-collection).

```bash
ansible-galaxy collection install crowdstrike.falcon
```

The modules in the CrowdStrike Falcon Ansible collection are powered by FalconPy! The Event-Driven Ansible source plugin is powered by the aiohttp Python library.

Let's make sure we install the python dependencies for the collection.

```bash
pip install --user crowdstrike-falconpy aiohttp
```

## Testing the Installation

To test the installation, we can run Ansible against a simple playbook `get-token.yml` that uses the `crowdstrike.falcon.auth` module to get an OAuth2 token.

```bash
ansible-playbook get-token.yml -v
```

> [!NOTE]
> In this directory, we also have a `ansible.cfg` file that sets the stdout callback to `yaml` for easier reading of the output.

You should see output similar to the following:

```yaml
PLAY [Check if CrowdStrike Colletion is working] ************************************************

TASK [Generate Authentication Credentials (access token and cloud region)] **********************
ok: [localhost] => changed=false
  auth:
    access_token: <ACCESS_TOKEN>
    cloud: us-1

PLAY RECAP **************************************************************************************
localhost: ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

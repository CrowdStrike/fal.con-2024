# Lab 2: Combatting Shadow IT with Dynamic Inventories

## Overview

In this lab, you will learn how to leverage the Falcon Discover API via the `crowdstrike.falcon.falcon_discover` Ansible
dynamic inventory to combat Shadow IT. This lab will demonstrate how to use the Falcon Discover dynamic inventory to identify all the assets in your environment, and how to use the filters and dynamic inventory features of Ansible to target specific assets for remediation. In our case, we will be deploying the Falcon sensor against unmanaged assets.

## Objectives

By the end of this lab, you will be able to:

- Use the Falcon Discover Dynamic Inventory to identify assets in your environment
- Use Ansible filters to target specific assets
- Group assets using Ansible's dynamic inventory
- Modify host variables in Ansible's dynamic inventory
- Use Ansible to deploy the Falcon sensor against unmanaged assets

## Steps

1. Navigate to the ~/labs/lab2 directory

    ```bash
    cd ~/labs/lab2
    ```

1. Review the `demo.falcon_discover.yml` inventory file

    ```bash
    less demo.falcon_discover.yml
    ```

    > If you are not familiar with Ansible dynamic inventories, you can read more about them [here](https://docs.ansible.com/ansible/latest/user_guide/intro_dynamic_inventory.html).

The `ansible-inventory` command is a nifty utility Ansible provides to help you understand what Ansible sees from an inventory perspective.

In our case, we will use it to help us visualize our Falcon Discover dynamic inventory.

3. Run the `ansible-inventory` command to view the assets identified by the Falcon Discover dynamic inventory

    ```bash
    ansible-inventory -i demo.falcon_discover.yml --graph | less
    ```

4. Run the `ansible-inventory` command this time with the `--list` option to see a more detailed view of the assets identified by the Falcon Discover dynamic inventory

    ```bash
    ansible-inventory -i demo.falcon_discover.yml --list | less
    ```

### Filter Assets

#### View all AWS assets in our environment

Now that we know how to view our inventory hosts, let's start to play with filter. In this example, we are going to return only AWS assets.

Uncomment the following line in the `demo.falcon_discover.yml` file:

```yaml
# filter: "cloud_provider:'AWS'"
```

Save the file and run the `ansible-inventory` command to view the filtered assets

```bash
ansible-inventory -i demo.falcon_discover.yml --list | less
```

#### View all the 'ansible' lab VMs in our environment

The previous filter showed us all AWS assets, let's take a look at all the 'ansible' lab vm's in the environment.

***Recomment the previous line*** and uncomment the following line in the `demo.falcon_discover.yml` file:

```yaml
# filter: hostname:*'*-ansible'
```

Save the file and run the `ansible-inventory` command to view the filtered assets

```bash
ansible-inventory -i demo.falcon_discover.yml --list | less
```

***Recomment the previous line*** and save the file before moving on to the next section.

### Grouping Assets

Now that we have seen how to filter assets, let's group them to make it easier to target specific assets.

> [!NOTE]
> Groups in dynamic inventories come in 2 different flavors: `keyed_groups` and `groups`. `keyed_groups` are groups that are based on a key in the host's variables, while `groups` are groups that are based on a filter. In this lab, we'll explore both.

#### Keyed Groups

##### Group assets by `cloud_provider`

Under the `keyed_groups` section in the `demo.falcon_discover.yml` file, uncomment the following lines:

```yaml
# - prefix: cloud
#   key: cloud_provider
```

Save the file and run the `ansible-inventory` command to view the grouped assets

```bash
ansible-inventory -i demo.falcon_discover.yml --graph | less
```

#### Conditional Groups

##### Group assets by `entity_type`

`groups` are created using Jinja2 conditionals. Let's group our assets by their `entity_type`.

Under the `groups` section in the `demo.falcon_discover.yml` file, uncomment the following lines:

```yaml
# unmanaged_assets: "entity_type == 'unmanaged'"
# managed_assets: "entity_type == 'managed'"
```

This creates 2 groups that contains all the unmanaged and managed assets in our environment. Save the file and run the `ansible-inventory` command to view the grouped assets

```bash
ansible-inventory -i demo.falcon_discover.yml --graph | less
```

### Modify Host Variables

The compose section of the `demo.falcon_discover.yml` file allows us to modify the host variables. In this section, we can add or modify variables for each host using Jinja2 templating.

#### View host variables for a specific host

Before we modify the host variables, let's first view the host variables for a specific host.
Run the `ansible-inventory` command to view the host variables for a specific host

```bash
ansible-inventory -i demo.falcon_discover.yml --list -l ip-172-17-0-20.us-west-2.compute.internal
```

#### Set the ansible_host to the local IP address

Under the `compose` section in the `demo.falcon_discover.yml` file, uncomment the following lines:

```yaml
# ansible_host: local_ip_addresses[0]
```

This sets the `ansible_host` variable to the first local IP address of the host. Save the file and run the `ansible-inventory` command to view the modified host variables

```bash
ansible-inventory -i demo.falcon_discover.yml --list -l ip-172-17-0-20.us-west-2.compute.internal
```

#### Set the ansible_user to 'ec2-user'

Under the `compose` section in the `demo.falcon_discover.yml` file, uncomment the following lines:

```yaml
# ansible_user: ec2-user
```

This sets the `ansible_user` variable to 'ec2-user'. Save the file and run the `ansible-inventory` command to view the modified host variables across all hosts

```bash
ansible-inventory -i demo.falcon_discover.yml --list | less
```

### Narrowing the Scope

Now that we have seen how to filter, group, and modify host variables, let's use Ansible to deploy the Falcon sensor against unmanaged assets. Specifically, for this lab we will want to ensure that you are targeting the correct assets before proceeding.

> [!WARNING]
> Duplicate hostnames are not allowed in Ansible. If you have duplicate hostnames in your environment, you will need to modify the `demo.falcon_discover.yml` file to ensure that each host has a unique hostname. See the below for examples on how to accomplish this.

In this lab, we all have a unique alias assigned to our lab VMs. For example, on your `ansible` VM you will see the hostname as `<your-alias>-ansible`.

You also have 2 unmanaged assets in your environment with the following hostnames:

- `<your-alias>-sketchy-cat1`
- `<your-alias>-sketchy-cat2`

Since the Falcon Discover API can't read OS level information about the unmanaged assets, it instead is using the aws hostname as the hostname for the unmanaged assets. This means that everyone in the lab will have the same unmanaged assets in their environment.

- `ip-172-17-0-20.us-west-2.compute.internal` (aka **sketchy-cat1**)
- `ip-172-17-0-30.us-west-2.compute.internal` (aka **sketchy-cat2**)

So how do we target the correct assets?

#### Dealing with duplicates

In order to allow duplicate hostnames, we can append a unique identifier to the hostname to make it unique.

Uncomment the following line in the `demo.falcon_discover.yml` file:

```yaml
# allow_duplicates: true
```

What this does is that if the hostnames already exist in the inventory, it will append a unique identifier (*the Asset ID*) to the hostname to make it unique. Save the file and run the `ansible-inventory` command to view the assets with the unique identifiers

```bash
ansible-inventory -i demo.falcon_discover.yml --graph | less
```

#### Modify the keyed_groups to group assets by `cloud_account_id`

To clean it up, we can use another unique identifier to group the assets. In our case, we will use the `cloud_account_id` since everyone has a unique AWS account ID in the lab.

***Recomment the previous change*** and then under the `keyed_groups` section in the `demo.falcon_discover.yml` file, uncomment the following lines:

```yaml
# - prefix: sketchy
#   key: cloud_account_id
```

Save the file and run the `ansible-inventory` command to view the new grouped assets

```bash
ansible-inventory -i demo.falcon_discover.yml --graph | less
```

Look at all those unique groups! But which one is yours?

We've added a couple of command aliases to help you identify your unique AWS account information as well as creating the final filter for the unmanaged assets.

To view your AWS account information, run the following command:

```bash
awsinfo
```

You can see your account id which would be the `cloud_account_id` in the grouped assets.

Copy your AWS account id and run the following command to view your assets:

```bash
ansible-inventory -i demo.falcon_discover.yml --graph sketchy_<your-aws-account-id>
```

### Putting it all together

Let's deploy the Falcon sensor against the unmanaged assets in our environment.

Run the following command to view the filters you can use to help target the unmanaged assets in your environment:

```bash
discover-filters
```

Either one can be used to filter down. However, for this lab we will use the first filter as we want to be able to see all the assets in our AWS account and use the groups we created earlier to target the unmanaged assets.

Add the following line to the `demo.falcon_discover.yml` file:

```yaml
filter: "cloud_account_id:'<your-aws-account-id>'"
```

Save the file and run the `ansible-inventory` with the `unmanaged_assets` group to view the filtered assets

```bash
ansible-inventory -i demo.falcon_discover.yml --list -l unmanaged_assets
```

Now that we have confirmed that we are targeting the correct assets, let's make sure we can connect to the unmanaged assets.

Run the following command to test the connection to the unmanaged assets:

```bash
ansible -i demo.falcon_discover.yml unmanaged_assets -m ping
```

You should see a response like this:

```bash
ip-172-17-0-20.us-west-2.compute.internal | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3.7"
    },
    "changed": false,
    "ping": "pong"
}
ip-172-17-0-30.us-west-2.compute.internal | SUCCESS => {
    "ansible_facts": {
        "discovered_interpreter_python": "/usr/bin/python3.7"
    },
    "changed": false,
    "ping": "pong"
}
```

### Deploy the Falcon Sensor

In this directory there is a playbook called `deploy-falcon.yml` that will deploy the Falcon sensor to the unmanaged assets in our environment.

Let's take a peek at the playbook:

```bash
cat deploy-falcon.yml
```

Run the following command to deploy the Falcon sensor to the unmanaged assets in our environment:

```bash
ansible-playbook -i demo.falcon_discover.yml deploy-falcon.yml
```

#### Validate the deployment

Sweet! You've just deployed the Falcon sensor to the unmanaged assets in your environment. You can now view the assets in the Falcon UI or we can use the dynamic inventory to check for the assets with the Falcon sensor installed (aka managed assets).

Run the `ansible-inventory` with the `managed_assets` group to view the filtered assets

```bash
ansible-inventory -i demo.falcon_discover.yml --list -l managed_assets | less
```

> [!NOTE]
> If you don't see the managed assets, you may need to wait a few minutes for the sensor to check in and for the API to update.

Congratulations! You have successfully deployed the Falcon sensor to the unmanaged assets in your environment.

## Bonus

Run the following command using the `crowdstrike.falcon.falconctl_info` module to view the sensor information for sketchy-cat assets:

```bash
ansible -i demo.falcon_discover.yml '*sketchy-cat*' -m crowdstrike.falcon.falconctl_info -b
```

Look at the tags ;)

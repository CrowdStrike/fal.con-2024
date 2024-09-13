# Lab 4: Modules, Plugins, and more

## Overview

In this lab, you will learn how to leverage the CrowdStrike Falcon collection modules and plugins for Ansible within your environment, moving outside of traditional sensor deployment.

## Objectives

By the end of this lab, you will be able to:

- Understand where to find the documentation for the CrowdStrike Falcon modules and plugins
- Understand the different CrowdStrike Falcon modules and plugins for Ansible
- Use the CrowdStrike Falcon modules and plugins to automate tasks

## Steps

1. Navigate to the `labs/lab4` directory to begin the lab.

    ```bash
    cd ~/labs/lab4
    ```

1. Review the structure of the lab directory by typing the `tree` command

    ```terminal
    .
    ├── README.md
    ├── ansible.cfg
    ├── examples
    │   ├── host-hide-inventory.yml
    │   ├── host-hide-lookup.yml
    │   └── host-unhide-inventory.yml
    ├── inventory
    ├── modules
    │   ├── auth.yml
    │   ├── kernel_support_info1.yml
    │   ├── kernel_support_info2.yml
    │   ├── sensor_download.yml
    │   └── sensor_download_info.yml
    └── plugins
        ├── demo.falcon_hosts.yml
        ├── host_ids.yml
        └── maintenance_token.yml
    ```

The lab directory is broken out into the following sections:

- **modules**: Contains example playbooks demonstrating the use of the CrowdStrike Falcon modules.
- **plugins**: Contains example playbooks demonstrating the use of the CrowdStrike Falcon plugins.
- **examples**: Contains example playbooks demonstrating ways to take advantage of the CrowdStrike Falcon modules and plugins.

The inventory file contains a static inventory for the lab environment that consists of:

- `localhost` - The local machine running the Ansible playbook
- `sketchy_cats` - A group that contains your two `sketchy-cat` hosts

### Documentation

Before we dive into the modules and plugins, let's take a look at the documentation for the CrowdStrike Falcon modules, plugins, and other resources.

#### GitHub Repository

The CrowdStrike Falcon Ansible collection is available on GitHub at https://github.com/CrowdStrike/ansible_collection_falcon

This is the primary source of truth for the CrowdStrike Falcon Ansible collection. You can find the latest documentation, release notes, and other resources here.

#### Ansible Galaxy

The CrowdStrike Falcon Ansible collection is also available on Ansible Galaxy at https://galaxy.ansible.com/ui/repo/published/crowdstrike/falcon

#### Red Hat Ansible Automation Hub

As a certified Ansible collection, the CrowdStrike Falcon Ansible collection is also available on Automation Hub at https://console.redhat.com/ansible/automation-hub/repo/published/crowdstrike/falcon/

#### CLI via `ansible-doc`

You can also use the `ansible-doc` command to view the documentation for the CrowdStrike Falcon modules and plugins.

To list all the available modules and lookup plugins in the collection by type, use the following commands:

```bash
ansible-doc -l crowdstrike.falcon -t module
ansible-doc -l crowdstrike.falcon -t lookup
```

> [!NOTE]
> :disappointed:
> Unfortunately there is no way to list ALL the plugins in the collection at once. You will need to list them by type.

To see the documentation for the crowdstrike.falcon.sensor_download module:

```bash
ansible-doc crowdstrike.falcon.sensor_download
```

> For more information on the `ansible-doc` command, see the [Ansible documentation](https://docs.ansible.com/ansible/latest/cli/ansible-doc.html).

### Explore the CrowdStrike Falcon Modules

> [!NOTE]
> The following examples are just to demonstrate a subset of the CrowdStrike Falcon modules available in the collection. For a complete list of modules, see any of the documentation sources mentioned above.

#### Auth Module

Manage token authentication for the CrowdStrike Falcon API.

>This module is particularly useful if you plan on making multiple API calls within a play. It is not mandatory to use with any of the other modules as all modules and plugins support both direct auth (credentials) and the auth object generated by this module.

Review the `auth.yml` module playbook in the `modules` directory.

```bash
cat modules/auth.yml
```

Execute the `auth.yml` module playbook.

```bash
ansible-playbook modules/auth.yml -v
```

Review the temporary file created by the `auth.yml` module playbook.

```bash
cat /tmp/falcon_token.json | jq .
```

#### Kernel Support Info Module

Get information about kernels supported by the Falcon Sensor for Linux. This module is useful for determining if the Falcon Sensor is compatible with a particular kernel versions.

> [!IMPORTANT]
> This does not reflect systems running in User Mode.

##### Example 1

Review the `kernel_support_info1.yml` module playbook in the `modules` directory.

```bash
cat modules/kernel_support_info1.yml
```

> Notice how we use the `auth` object from the previous playbook to authenticate with the CrowdStrike Falcon API.

In this example, we will target **sketchy-cat2** and set the kernel and architecture from the gathered facts. Next, we will pass that information to the `kernel_support_info` module to see what sensor versions are supported for sketchy. Finally we list all the support information for Ubuntu 20 kernels that start with 5.8

Execute the `kernel_support_info1.yml` module playbook.

```bash
ansible-playbook modules/kernel_support_info1.yml -v | tee output.txt
```

##### Example 2

Review the `kernel_support_info2.yml` module playbook in the `modules` directory.

```bash
cat modules/kernel_support_info2.yml
```

This example shows how to leverage Ansible's powerful Jinja2 templating to further refine results. Let's face it, sometimes FQL (falcon query language) can be confusing/frustrating. But if you just ask for everything and then refine with Ansible, the world is a better place ;)

Execute the `kernel_support_info2.yml` module playbook.

> [!TIP]
> You can use Ansible's Jinja2 filters to further refine the output.
> For example, you can use the `selectattr` filter to filter the output based on a specific attribute.

```bash
ansible-playbook modules/kernel_support_info2.yml | tee output.txt
```

#### Sensor Download Info Module

Get information about available Falcon Sensor Installers. Typically used as an input for the `crowdstrike.falcon.sensor_download` module we will visit next.

Review the `sensor_download_info.yml` module playbook in the `modules` directory.

```bash
cat modules/sensor_download_info.yml
```

In this example, we are getting all the available Windows sensor installers, and then printing out the 2 most recent installers.

Execute the `sensor_download_info.yml` module playbook.

```bash
ansible-playbook modules/sensor_download_info.yml | tee output.txt
```

#### Sensor Download Module

Downloads the Falcon Sensor Installer.

> [!IMPORTANT]
> This module will not install the Falcon Sensor. It will only download the installers to the **local** machine only.
>
> To install the Falcon sensor, use the `crowdstrike.falcon.falcon_install` role.

Review the `sensor_download.yml` module playbook in the `modules` directory.

```bash
cat modules/sensor_download.yml
```

In this example, we are doing the following:

1. Setup a version decrement variable: **n_minus** to mimic downloading N-1 sensor.
1. Build out our filter based on `sketchy-cat1`
1. Use the `sensor_download_info` module to get our list of installers
1. Validate our list and then download the **n_minus** version to the /tmp directory

Execute the `sensor_download.yml` module playbook.

```bash
ansible-playbook modules/sensor_download.yml -v | tee output.txt
```

Review the `output.txt`.

```bash
less output.txt
```

Awesome! You have succesfully downloaded a sensor installer!

Now go ahead and run the Ansible playbook again and see if anything changes. It shouldn't since Ansible is all about idempotency (*things dont need to change if they're already in the right state*) and the CrowdStrike Falcon Ansible modules follow this principle.

```bash
ansible-playbook modules/sensor_download.yml -v | tee output.txt
```

### Explore the CrowdStrike Falcon Plugins

> [!NOTE]
> There is a distinction between modules and plugins in Ansible. Modules are standalone scripts that can be used by Ansible to automate tasks. Plugins are pieces of code that extend Ansible's core functionality. Plugins can be lookups, filters, callbacks, inventories, etc.
>
> Currently, the CrowdStrike Falcon Ansible collection contains lookup and inventory plugins.

#### Host IDs Lookup Filter Plugin

Fetch host IDs. This plugin is extremely useful as input to the other **host** modules.

Review the `host_ids.yml` plugin playbook in the `plugins` directory.

```bash
cat plugins/host_ids.yml
```

Execute the `host_ids.yml` plugin playbook.

```bash
ansible-playbook plugins/host_ids.yml | tee output.txt
```

#### Maintenance Token Lookup Filter Plugin

Fetch the maintenance token. This plugin will fetch the maintenance token for specified hosts, or it can also retrieve the bulk maintenance token (*if applicable in your environment*).

>Maintenance tokens are used to uninstall the Falcon Sensor from a host.

Review the `maintenance_token.yml` plugin playbook in the `plugins` directory.

```bash
cat plugins/maintenance_token.yml
```

> [!TIP]
> You can use the `crowdstrike.falcon.host_ids` lookup plugin to get the host IDs for the hosts you want to retrieve the maintenance token for.

Execute the `maintenance_token.yml` plugin playbook.

```bash
ansible-playbook plugins/maintenance_token.yml | tee output.txt
```

#### Falcon Hosts Inventory Plugin

This dynamic inventory queries asset details from the CrowdStrike Falcon Hosts API.

> [!NOTE]
> The difference between this inventory plugin and the `crowdstrike.falcon.falcon_discover` inventory plugin is that this plugin will only work with **managed** assets that already have the sensor installed.

Review the `demo.falcon_hosts.yml` inventory playbook in the `plugins` directory.

```bash
vim plugins/demo.falcon_hosts.yml
```

Run the `ansible-inventory` command to see the inventory generated by the `demo.falcon_hosts.yml` inventory plugin.

```bash
ansible-inventory -i plugins/demo.falcon_hosts.yml --list -l sketchy | less
```

### Example: Hiding hosts from the Falcon console

A very common use case is to hide hosts from the Falcon console, especially hosts that are generally considered ephemeral or stale because they have not checked in for a long time.

> [!TIP]
> If you manage hosts with our Ansible collection, you can leverage the `crowdstrike.falcon.falcon_uninstall` role to automatically hide hosts after uninstalling the sensor by setting `falcon_remove_host: true`.

#### Using lookup plugin

1. Open up the Falcon console and navigate to `Host setup and management` --> `Host management`.
1. Select `Tags` and filter by your alias.

Review the `host-hide-lookup.yml` playbook in the `examples` directory.

```bash
cat examples/host-hide-lookup.yml
```

Execute the `host-hide-lookup.yml` playbook.

```bash
\ansible-playbook examples/host-hide-lookup.yml -v | tee output.txt
```

> [!NOTE]
> If you noticed that we are using a leading backslash (`\`) before the `ansible-playbook` command, this is to prevent the helper alias we have for `ansible-playbook` from running. This is because the `unbuffer` command does not play nicely with the `ansible.builtin.pause` module. The `unbuffer` command is useful for this lab to get colorized output from the `ansible-playbook` command and view it in the tee output file.

1. Navigate back to the Falcon console and refresh the page.
1. Selecte the `Hidden hosts` tab.
1. Apply the same filter as before.
1. Go back to the `ansible` vm and continue running the playbook by pressing `Enter`.
1. When the playbook finishes, refresh the Falcon console page again and see if the hosts are now back in the `Hosts` tab.

#### Using a dynamic inventory

In this example, we will use the `crowdstrike.falcon.falcon_hosts` inventory plugin to generate a dynamic inventory of hosts and hide them from the Falcon console. We will take advantage of the inventory caching features to ensure that we don't lose our aid's.

> [!IMPORTANT]
> When a host is hidden, is it also hidden from the context of our dynamic inventories. This means that if you hide a host, it will not show up in the inventory generated by the `crowdstrike.falcon.falcon_hosts` or `crowdstrike.falcon.falcon_discover` inventory plugins.

Execute the inventory file to validate the inventory.

```bash
ansible-inventory -i plugins/demo.falcon_hosts.yml --list -l sketchy
```

Review the `host-hide-inventory.yml` playbook in the `examples` directory.

```bash
cat examples/host-hide-inventory.yml
```

Execute the `host-hide-inventory.yml` playbook.

```bash
ansible-playbook -i plugins/demo.falcon_hosts.yml examples/host-hide-inventory.yml -v | tee output.txt
```

> [!TIP]
> This version shows how to loop through the AIDs and hide them one by one. This can be slow if you have a large number of hosts to hide. If you do choose to go this route, this is where generating and using the `crowdstrike.falcon.auth` token can be useful to prevent repeated API authentication calls.

Review the `host-unhide-inventory.yml` playbook in the `examples` directory.

```bash
cat examples/host-unhide-inventory.yml
```

Execute the `host-unhide-inventory.yml` playbook.

```bash
ansible-playbook -i plugins/demo.falcon_hosts.yml examples/host-unhide-inventory.yml -v | tee output.txt
```

Run it again to ensure they are in the correct state (*idempotency*).

```bash
ansible-playbook -i plugins/demo.falcon_hosts.yml examples/host-unhide-inventory.yml -v | tee output.txt
```

## End of Lab

Congratulations! You have completed the lab. You have learned how to leverage the CrowdStrike Falcon modules and plugins for Ansible within your environment, moving outside of the traditional sensor deployment philosophy.

Go out there and automate all the things!
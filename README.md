# ansible-jhipster-devops
A sample jhipster project managed by Vagrant and Ansible within a complete continuous delivery process.


## Getting started

This README file is inside a folder that contains a Vagrantfile (hereafter this folder shall be called the `vagrant_root`), which tells Vagrant how to set up your Continuous Delivery Platform.

To use the vagrant file, you will need to have done the following:

  1. Download and Install [VirtualBox](https://www.virtualbox.org/wiki/Downloads).
  2. Download and Install [Vagrant](https://www.vagrantup.com/downloads.html).
  4. Install the vagrant [hostmanager](https://github.com/smdahlen/vagrant-hostmanager) plugin: `$ vagrant plugin install hostmanager`.
  4. Install [Ansible](http://docs.ansible.com/intro_installation.html) **version >= 1.8**.
  5. Open a shell prompt and cd into the folder containing the `Vagrantfile`.

Once all of that is done, you can simply type in `vagrant up`, and Vagrant will create all the VMs, and configure them.

Otherwise, if you want to spin up a specific VM, just type `vagrant up <vm_name>`. For example, to run the Continuous Integration Platform VM that includes Jenkins, Gitlab, Artifactory and Docker-registry:

    $ vagrant up cip-vm


## Troubleshooting

If you keep using the default vagrant base box [`deb/jessie-amd64`](https://vagrantcloud.com/deb/boxes/jessie-amd64) and you see several warning messages like `Warning: Remote connection disconnect. Retrying...` when you spin up a virtual machine, try to enable the GUI of the corresponding Virtualbox VM to see what is happening.

To turn on the GUI you have to put this in your vagrant config `Vagrantfile`:

    cfg.vm.provider "virtualbox" do |v|
      v.gui = true
      ...
    end

If you see in the output screen a message like `a start job is running for dev-disk-by x2duuid...`, you can fix the connection timeout issue as follow:

  1. Get the correct swap UUID after the VM is up: `$ sudo blkid | grep swap`.
  2. Update the /etc/fstab file with the correct swap UUID: `$ sudo nano /etc/fstab`.
  3. Reboot the VM.


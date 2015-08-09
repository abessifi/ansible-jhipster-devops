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

Otherwise, if you want to spin up a specific VM, just type `vagrant up <vm_name>`. For example, to run the Continuous Integration Platform VM that includes Jenkins, Gitlab and Artifactory:

    $ vagrant up cip-vm


## Services setup

#### Continuous Integration Platform


#### The Registry

In this lab we are using a dedicated virtual machine, `registry`, to host the [Docker registry 2.0 service](https://docs.docker.com/registry/) and [Artifactory](http://www.jfrog.com/artifactory/). In fact, it is a good idea to use this registry to control where your images/artifacts are being stored and distribute them into your inhouse development and test workflow.

##### - Docker registry

To spin up the docker registry service:

	$ vagant up docker-registry

The above command runs a VM and configures, for the first time, a Docker registry container binded to `http://localhost:5000`.
For security reasons, the Docker Registry 2.0 is set up with username/password authentication and SSL using the official [Docker Registry image](https://registry.hub.docker.com/u/library/registry/) and a custom configured nginx as a proxy server.

The registry is reachable on `https://registry.local/v2/` and default credentials are :

	username: docker
	password: changeit

#### GitLab container

GitLab is a self hosted solution which helps you to manage projects, issues, merge requests and easily browse your source code. It's a fast, secure and stable solution.

The [GitLab container](https://hub.docker.com/r/sameersbn/gitlab/) will host the jhipster-sample-app application (to be used like Github) to manage source code and for the development workflow.

To run the Continuous Integration Platform VM that includes Gitlab :

       $ vagrant up cip-vm

The GitLab container is reachable on `http://cip-vm.local:10080` and  the default username and password are :
    
       username: root
       password: 5iveL!fe



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


# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = "2"

DOMAIN = 'local'
CIP_NODE_IP = '192.168.33.40'
JH_DEV_NODE_IP = '192.168.33.41'
DOCKER_REGISTRY_IP = '192.168.33.42'
CIP_DATA_DISK = './.vagrant/machines/cip-vm/cip_data_disk.vdi'
CIP_DATA_DISK_SIZE = 20*1024
DOCKER_REGISTRY_DATA_DISK = './.vagrant/machines/docker-registry/registry_data_disk.vdi'
DOCKER_REGISTRY_DATA_DISK_SIZE = 20*1024

def create_data_disk(vbox_config, local_disk_path, disk_size)

  unless File.exist?(local_disk_path)
    # Create a disk for data storage
    vbox_config.customize ['createhd', '--filename', local_disk_path, '--size', disk_size]
    # Attach the created disk to the virtual machine 
    vbox_config.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 
                           1, '--device', 0, '--type', 'hdd', '--medium', local_disk_path]
  end
end

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
	# Debian boxes are available in https://vagrantcloud.com/deb
	# Actual stable release is Debian Jessie
	config.vm.box = 'deb/jessie-amd64'
	# Disable automatique box update
	config.vm.box_check_update = false
	# Disabling the default /vagrant share
	config.vm.synced_folder ".", "/vagrant" , disabled: true
	# Update /etc/hosts in all VMs
	config.hostmanager.enabled = true
	config.hostmanager.manage_host = true
	config.hostmanager.include_offline = true
  
  # Continuous Integration Platform VM
  config.vm.define "cip-vm" do |cfg|
    cfg.vm.hostname = "cip-vm.#{DOMAIN}"
    cfg.vm.network "private_network", ip: CIP_NODE_IP
    cfg.hostmanager.aliases = "cip-vm"
    cfg.vm.provider "virtualbox" do |v|
      v.name = 'cip-vm'
      v.memory = 1536
      v.cpus = 2
      create_data_disk v, CIP_DATA_DISK, CIP_DATA_DISK_SIZE
	  end
  	cfg.vm.provision :ansible do |ansible|
	    ansible.playbook = 'provisioning/cip-setup.yml'
	  end
  end

  # Setup a docker-registry virtual machine to store docker images
  config.vm.define "docker-registry" do |cfg|
    cfg.vm.hostname = "docker-registry.#{DOMAIN}"
    cfg.vm.network "private_network", ip: DOCKER_REGISTRY_IP
    cfg.hostmanager.aliases = "docker-registry"
    cfg.vm.provider "virtualbox" do |v|
      v.name = 'docker-registry'
      create_data_disk v, DOCKER_REGISTRY_DATA_DISK, DOCKER_REGISTRY_DATA_DISK_SIZE
	end
  	cfg.vm.provision :ansible do |ansible|
      ansible.playbook = 'provisioning/docker-registry-setup.yml'
    end
  end

  # Setup a Jhipster Development environement
  config.vm.define "jhipster-dev" do |cfg|
    cfg.vm.hostname = "jhipster-dev.#{DOMAIN}"
    cfg.vm.network "private_network", ip: JH_DEV_NODE_IP
    cfg.hostmanager.aliases = "jhipster-dev"
    cfg.vm.provider "virtualbox" do |v|
      v.name = 'jhipster-dev'
      v.memory = 768
	  end
  	cfg.vm.provision :ansible do |ansible|
      ansible.playbook = 'provisioning/jhipster-dev-setup.yml'
    end
  end

  # Setup a Jhipster QA environement

  # Setup a Jhipster producation environement

end

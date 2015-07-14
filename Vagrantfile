# -*- mode: ruby -*-
# vi: set ft=ruby :

DOMAIN = 'local'
CIP_NODE_IP = '192.168.33.40'
CIP_DATA_DISK = './.vagrant/machines/cip-vm/cip_data_disk.vdi'

VAGRANTFILE_API_VERSION = "2"

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
      unless File.exist?(CIP_DATA_DISK)
		    # Create the a second 20GiB disk for data storage
        v.customize ['createhd', '--filename', CIP_DATA_DISK, '--size', 20 * 1024]
 	      # Attach the created disk to the virtual machine 
		    v.customize ['storageattach', :id, '--storagectl', 'SATA Controller', '--port', 
                   1, '--device', 0, '--type', 'hdd', '--medium', CIP_DATA_DISK]
      end
	  end
  	cfg.vm.provision :ansible do |ansible|
	    ansible.playbook = 'provisioning/cip-setup.yml'
	  end
  end

  # Setup a Jhipster Development environement

  # Setup a Jhipster QA environement

  # Setup a Jhipster producation environement

end

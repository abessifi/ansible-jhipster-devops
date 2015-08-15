from ansible.runner.return_data import ReturnData
from ansible import utils
import urllib2 as urllib
import re, base64, json
from docker import Client
from docker.errors import APIError, NotFound
from requests import ConnectionError

class ImageNameFormatException(Exception): pass

class ActionModule(object):

    def __init__(self, runner):
        self.runner = runner

    def _merge_args(self, module_args, complex_args):
        args = {}
        if complex_args:
            args.update(complex_args)
        kv = utils.parse_kv(module_args)
        args.update(kv)

        return args
    
    def parse_image_name(self, docker_image):
        """
        Check if the Docker image name format is correct or not.
        Example of supported formats : foo/bar:latest, foo/bar:x.x.x, foo:x.x.x
        """
        index = 1
        items = []
        try:
            m = re.search('(.*)/(.*):(.+)', docker_image)
            if m:
                index += 1
            else:
                m = re.search('(.*):(.+)', docker_image)
            items = m.group(index,(index+1))
        except AttributeError:
            raise ImageNameFormatException("Docker image name format not correct !")
        return items

    def _image_exists(self, image_name, image_version, registry_fqdn, username, password):
        """
        Check if the givin docker image name/version exists on the 
        local Docker registry.
        """
        try:
            request = urllib.Request("https://{1}/v2/{0}/tags/list".format(image_name,
                                registry_fqdn))
            base64string = base64.encodestring("{}:{}".format(username, password))
            request.add_header("Authorization", "Basic %s" % base64string)
            response = urllib.urlopen(request)
            data = json.load(response)
        except urllib.HTTPError as error:
            msg = json.loads(error.read())
            if error.code == 404 and \
            'repository name not known' in msg['errors'][0].get('message'):
                return False
        if image_version in data['tags']:
            return True

        return False

    def run(self, conn, tmp, module_name, module_args, inject, complex_args=None, **kwargs):
        """
        This function is ran automatically by Ansible when the 'update_registry'
        action is performed. It is used to determine if a given Docker image is
        already synced to the local private registry or not (sync it otherwise).
        """

        args = self._merge_args(module_args, complex_args)
        docker_image=args.get('docker_image')
        registry_fqdn=args.get('registry_fqdn')
        docker_http_server_port=args.get('docker_http_server_port')
        registry_access_username = args.get('username')
        registry_access_password = args.get('password')
        docker_image_name, docker_image_version = self.parse_image_name(docker_image)
        new_image_name = "{}:443/{}".format(registry_fqdn, docker_image_name)
        image_push_status="[update_registry][ERROR] Image '{}' not synced with the private registry.".format(docker_image)
        tagged = synced = False

        # Check if the docker image is already in the private
        # docker registry
        if not self._image_exists(docker_image_name, docker_image_version, 
                                  registry_fqdn, registry_access_username, 
                                  registry_access_password):
            try:
                # Connect to the remote private Docker registry
                client = Client(base_url="http://{}:{}".format(registry_fqdn,
                                       docker_http_server_port), 
                                       version=args.get('docker_server_version'))
                # Pull the image from dockerhub
                for output in client.pull(docker_image, stream=True):
                    print(json.dumps(json.loads(output), indent=4))
                # Tag the image
                tagged = client.tag(image=docker_image, repository=new_image_name,
                                        tag=docker_image_version, force=True)
                # Push the downloaded image to the private Docker registry
                for output in client.push(new_image_name, stream=True):
                    print(json.dumps(json.loads(output), indent=4))
                # Remove the tagged image
                client.remove_image("{}:{}".format(new_image_name, docker_image_version))
                # Remove the base image from the local Docker repository
                client.remove_image(docker_image)
                synced = True
            except (APIError, NotFound) as error:
                print error.explanation
            except ConnectionError as error:
                print error
        else:
            synced = True

        if synced:
            image_push_status="[update_registry][INFO] Image '{}' correctly synced with the private registry.".format(docker_image)
            
        print image_push_status

        return ReturnData(conn=conn,
                          comm_ok=True,
                          result=dict(failed=False, changed=False, msg=image_push_status))

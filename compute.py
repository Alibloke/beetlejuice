# Create compute node
import pyrax

pyrax.set_setting("identity_type", "rackspace")
pyrax.set_default_region('{region}')
pyrax.set_credentials(file)

cs = pyrax.cloudservers

image = pyrax.images.get('88928a0a-f94c-47e3-ad7d-27b735af1a15')

flavor = cs.flavors.get('performance2-30')

server = cs.servers.create('transcoder', image.id, flavor.id)

pyrax.utils.wait_for_build(server, verbose=True)

# Build script to Install HandbrakeCLI

pacman -Sy handbrake-cli --no-prompt

# Delete node

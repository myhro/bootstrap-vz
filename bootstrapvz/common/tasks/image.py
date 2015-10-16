from bootstrapvz.base import Task
from bootstrapvz.common import phases
from bootstrapvz.common.tools import log_check_call
import os


class MoveImage(Task):
	description = 'Moving volume image'
	phase = phases.image_registration

	@classmethod
	def run(cls, info):
		image_name = info.manifest.image['name'].format(**info.manifest_vars)
		filename = image_name + '.' + info.volume.extension

		destination = os.path.join(info.manifest.bootstrapper['workspace'], filename)
		import shutil
		shutil.move(info.volume.image_path, destination)
		info.volume.image_path = destination
		import logging
		log = logging.getLogger(__name__)
		log.info('The volume image has been moved to ' + destination)


class CreateImageTarball(Task):
	description = 'Creating tarball with image'
	phase = phases.image_registration
	predecessors = [MoveImage]

	@classmethod
	def run(cls, info):
		image_name = info.manifest.image['name'].format(**info.manifest_vars)
		filename = image_name + '.' + info.volume.extension

		# Ensure that we do not use disallowed characters in image name
		image_name = image_name.lower()
		image_name = image_name.replace('.', '-')
		image_name = image_name.replace(' ', '-')

		tarball_name = image_name + '.tar.gz'
		tarball_path = os.path.join(info.manifest.bootstrapper['workspace'], tarball_name)

		# Store image information so it can be referenced later
		info.image = {
		    'name': image_name,
		    'tarball_name': tarball_name,
		    'tarball_path': tarball_path,
		}

		log_check_call(['tar', '--sparse', '-C', info.manifest.bootstrapper['workspace'],
		                '-caf', tarball_path, filename])

from bootstrapvz.base import Task
from bootstrapvz.common import phases
from bootstrapvz.common.tools import log_check_call
import os


class MoveImage(Task):
	description = 'Moving volume image'
	phase = phases.image_registration

	@classmethod
	def run(cls, info):
		destination = os.path.join(info.manifest.bootstrapper['workspace'], info.image['filename'])
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
		if not info.image.get('tarball_name', False):
			tarball_name = info.image['name'] + '.tar.gz'
			info.image['tarball_name'] = tarball_name

		tarball_path = os.path.join(info.manifest.bootstrapper['workspace'], info.image['tarball_name'])
		info.image['tarball_path'] = tarball_path

		log_check_call(['tar', '--sparse', '-C', info.manifest.bootstrapper['workspace'],
		                '-caf', tarball_path, info.image['filename']])

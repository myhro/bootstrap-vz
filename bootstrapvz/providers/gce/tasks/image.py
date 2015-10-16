from bootstrapvz.base import Task
from bootstrapvz.common import phases
from bootstrapvz.common.tasks import image
from bootstrapvz.common.tools import log_check_call


class UploadImage(Task):
	description = 'Uploading image to GCS'
	phase = phases.image_registration
	predecessors = [image.CreateImageTarball]

	@classmethod
	def run(cls, info):
		log_check_call(['gsutil', 'cp', info.image['tarball_path'],
		                info.manifest.image['gcs_destination'] + info.image['tarball_name']])


class RegisterImage(Task):
	description = 'Registering image with GCE'
	phase = phases.image_registration
	predecessors = [UploadImage]

	@classmethod
	def run(cls, info):
		image_description = info._gce['lsb_description']
		if 'description' in info.manifest.image:
			image_description = info.manifest.image['description']
		log_check_call(['gcutil', '--project=' + info.manifest.image['gce_project'],
		                'addimage', info.image['name'],
		                info.manifest.image['gcs_destination'] + info.image['tarball_name'],
		                '--description=' + image_description])

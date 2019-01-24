
def user_directory_path(instance, filename):
	# File will be uploaded to MEDIA_ROOT/simulation/user_<id>/simulation_<id>/<filename>
	return 'simulation/user_{0}/simulation_{1}/{2}'.format(instance.user.id, instance.id, filename)

def file_directory_path(instance, filename):
	# File will be uploaded to MEDIA_ROOT/simulation/user_<id>/simulation_<id>/<filename>
	return 'simulation/user_{0}/simulation_{1}/{2}'.format(instance.simulation.user.id, instance.simulation.id, filename)

def output_directory_path(instance, filename):
	# File will be uploaded to MEDIA_ROOT/simulation/user_<id>/simulation_<id>/output/<filename>
	return 'simulation/user_{0}/simulation_{1}/output/{2}'.format(instance.simulation.user.id, instance.simulation.id, filename)

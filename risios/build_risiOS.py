from rbuild import KickStartBuilder
import rbuild as Base

builder = KickStartBuilder.KickStartBuilder.new_from_yaml("risios/project.yml")
#builder.download_flattened_kickstart()
builder.build_iso()

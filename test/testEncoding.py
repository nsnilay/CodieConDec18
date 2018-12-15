import inception_blocks_v2
import fr_utils

FRmodel = inception_blocks_v2.faceRecoModel(input_shape=(3, 96, 96))

encoding = fr_utils.img_path_to_encoding("crop_frame.jpg", FRmodel)
print(encoding)
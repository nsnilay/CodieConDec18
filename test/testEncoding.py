from keras import backend as K
K.set_image_data_format('channels_first')

import inception_blocks_v2
import fr_utils


def myMainMethod():


    FRmodel = inception_blocks_v2.faceRecoModel(input_shape=(3, 96, 96))

    encoding = fr_utils.img_path_to_encoding("crop_frame.jpg", FRmodel)
    print(encoding)

if __name__ == '__main__':
    myMainMethod()

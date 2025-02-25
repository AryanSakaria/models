# Lint as: python3
# Copyright 2020 The TensorFlow Authors All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Extracts DELG features for images from Revisited Oxford/Paris datasets.

Note that query images are cropped before feature extraction, as required by the
evaluation protocols of these datasets.

The types of extracted features (local and/or global) depend on the input
DelfConfig.

The program checks if features already exist, and skips computation for those.
"""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import time

from absl import app
from absl import flags
import numpy as np
import tensorflow as tf

from google.protobuf import text_format
from delf import delf_config_pb2
from delf import datum_io
from delf import feature_io
from delf import utils
from delf.python.datasets.matterport import dataset
from delf import extractor

FLAGS = flags.FLAGS

flags.DEFINE_string(
    'delf_config_path', '/tmp/delf_config_example.pbtxt',
    'Path to DelfConfig proto text file with configuration to be used for DELG '
    'extraction. Local features are extracted if use_local_features is True; '
    'global features are extracted if use_global_features is True.')


flags.DEFINE_enum('image_set', 'query', ['query', 'index'],
                  'Whether to extract features from query or index images.')


# Extensions.
_DELG_GLOBAL_EXTENSION = '.delg_global'
_DELG_LOCAL_EXTENSION = '.delg_local'
_IMAGE_EXTENSION = '_rgb.png'

# Pace to report extraction log.
_STATUS_CHECK_ITERATIONS = 50


def main(argv):
  if len(argv) > 1:
    raise RuntimeError('Too many command-line arguments.')

  # Read list of images from dataset file.
  #Change folder directory
  mp3d_folder = "/home/aryan/RRC_proj/x-view-scratch/data_collection/x-view/mp3d"
  for scene in os.listdir(mp3d_folder):
    dataset_file_path = os.path.join(mp3d_folder, scene)
    print('Reading list of images from dataset file...')
    query_list, index_list = dataset.ReadDatasetFile(
        dataset_file_path)
    if FLAGS.image_set == 'query':
      image_list = query_list
      output_features_dir = os.path.join(dataset_file_path,"dbow", "features","query")
    else:
      image_list = index_list
      output_features_dir = os.path.join(dataset_file_path,"dbow", "features","index")
    num_images = len(image_list)
    # print(query_list)
    print('done! Found %d images' % num_images)
    for i in image_list:
      print(i)


    # Parse DelfConfig proto.
    config = delf_config_pb2.DelfConfig()
    with tf.io.gfile.GFile('r50delg_gld_config.pbtxt', 'r') as f:
      text_format.Parse(f.read(), config)

    # Create output directory if necessary.
    if not tf.io.gfile.exists(output_features_dir):
      tf.io.gfile.makedirs(output_features_dir)

    extractor_fn = extractor.MakeExtractor(config)

    # start = time.time()
    for i in range(num_images):
      # if i == 0:
      #   print('Starting to extract features...')
      # elif i % _STATUS_CHECK_ITERATIONS == 0:
      #   elapsed = (time.time() - start)
      #   print('Processing image %d out of %d, last %d '
      #         'images took %f seconds' %
      #         (i, num_images, _STATUS_CHECK_ITERATIONS, elapsed))
      #   start = time.time()

      image_name = image_list[i]
      input_image_filename = os.path.join(dataset_file_path,"dbow", "images",
                                          str(image_name) + _IMAGE_EXTENSION)
      # print(input_image_filename, os.path.isfile(input_image_filename))

      # Compose output file name and decide if image should be skipped.
      should_skip_global = True
      should_skip_local = True
      if config.use_global_features:
        output_global_feature_filename = os.path.join(
            output_features_dir, str(image_name) + _DELG_GLOBAL_EXTENSION)
        print(output_global_feature_filename)
        if not tf.io.gfile.exists(output_global_feature_filename):
          should_skip_global = False
      if config.use_local_features:
        output_local_feature_filename = os.path.join(
            output_features_dir, str(image_name) + _DELG_LOCAL_EXTENSION)
        print(output_local_feature_filename)
        if not tf.io.gfile.exists(output_local_feature_filename):
          should_skip_local = False
      if should_skip_global and should_skip_local:
        print('Skipping %s' % image_name)
        continue

      pil_im = utils.RgbLoader(input_image_filename)
      resize_factor = 1.0
    #   if FLAGS.image_set == 'query':
    #     # Crop query image according to bounding box.
    #     original_image_size = max(pil_im.size)
    #     bbox = [int(round(b)) for b in ground_truth[i]['bbx']]
    #     pil_im = pil_im.crop(bbox)
    #     cropped_image_size = max(pil_im.size)
    #     resize_factor = cropped_image_size / original_image_size

      im = np.array(pil_im)

    #   # Extract and save features.
      extracted_features = extractor_fn(im, resize_factor)
      if config.use_global_features:
        global_descriptor = extracted_features['global_descriptor']
        datum_io.WriteToFile(global_descriptor, output_global_feature_filename)
      if config.use_local_features:
        locations = extracted_features['local_features']['locations']
        descriptors = extracted_features['local_features']['descriptors']
        feature_scales = extracted_features['local_features']['scales']
        attention = extracted_features['local_features']['attention']
        feature_io.WriteToFile(output_local_feature_filename, locations,
                               feature_scales, descriptors, attention)


if __name__ == '__main__':
  app.run(main)

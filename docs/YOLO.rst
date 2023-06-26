======================
HOW TO RUN YOLO COMMANDS
======================

Yolo Processing
---------------

Processes input directory of images and outputs the corresponding YOLO output with red box around fish in a given image or video. Note that height and width are optional arguments if you would like to customize output size, though this may affect YOLO performance greatly. 

To run the command: 

.. code-block:: bash

   make yolo input_path="path_to_input" weights="path_to_weights" height="?" width="?"


Yolo Segmentation
-----------------

Processes yolo image same way as previous command but segments the red YOLO boxes into separate images for each fish in a given image or video. Height and width are optional parameters. 

To run the command:

.. code-block:: bash

   make segment input_path="path_to_input" weights="path_to_weights" height="?" width="?" output_path="path_to_output"


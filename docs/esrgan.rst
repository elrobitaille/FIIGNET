======================
HOW TO RUN ESRGAN
======================

ESRGAN Enhancer
---------------

Processes the image using an ESRGAN (Enhanced Super-Resolution Generative Adversarial Network) to enhance the quality of the image by filling in any details of the fish that may be off due to low resolution or quality.

Clone the A-ESRGAN Repo:

.. code-block:: bash

   git clone https://github.com/stroking-fishes-ml-corp/A-ESRGAN

To run the command:

.. code-block:: bash

   make esrgan input_dir="/path/to/input" output_dir="/path/to/output"


from tensorflow.keras import layers
import tensorflow as tf


def capacity_thresholding_layer(*args, **kwargs):
    """
    Return a Lambda layer that clips predictions in the last 48 hours to the capacity.

    The layer takes 3 input tensors in this order:
    - prediction: [?, 1]
    - capacity: [?, 1]
    - hours_before_departure: [?, 1]
    :param args:
    :param kwargs:
    :return:
    """

    return layers.Lambda(
        lambda x: tf.where_v2(x[2] <= 48, tf.minimum(x[0], x[1]), x[0]), *args, **kwargs
    )
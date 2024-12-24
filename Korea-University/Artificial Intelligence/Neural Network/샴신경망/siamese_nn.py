
import tensorflow as tf
import utils
import numpy as np
from keras.layers import Input, Lambda
from keras.models import Model

faces_dir = '샴신경망/att_faces/'

# Import Training and Testing Data
(X_train, Y_train), (X_test, Y_test) = utils.get_data(faces_dir)
num_classes = len(np.unique(Y_train))

# Convert labels to float32
Y_train = Y_train.astype('float32')

# Create Siamese Neural Network
input_shape = X_train.shape[1:]
shared_network = utils.create_shared_network(input_shape)
input_top = Input(shape=input_shape)
input_bottom = Input(shape=input_shape)
output_top = shared_network(input_top)
output_bottom = shared_network(input_bottom)
distance = Lambda(utils.euclidean_distance, output_shape=(1,))([output_top, output_bottom])
model = Model(inputs=[input_top, input_bottom], outputs=distance)

# Train the model
training_pairs, training_labels = utils.create_pairs(X_train, Y_train, num_classes=num_classes)
training_labels = training_labels.astype('float32')  # Convert labels to float32
model.compile(loss=utils.contrastive_loss, optimizer='adam', metrics=[utils.accuracy])
model.fit([training_pairs[:, 0], training_pairs[:, 1]], training_labels,
          batch_size=128,
          epochs=10)

# Save the model
model.save('샴신경망/siamese_nn.h5')

import os, argparse, time
from .utils import *
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Dropout
from tensorflow.keras.layers import LSTM
from tensorflow.keras.callbacks import ModelCheckpoint, ReduceLROnPlateau, TensorBoard
from tensorflow.keras.optimizers import SGD, RMSprop, Adagrad, Adadelta, Adam, Adamax, Nadam
import easydict

OUTPUT_SIZE = 129 # 0-127 notes + 1 for rests

def parse_args():

    args = easydict.EasyDict({
        "data_dir": "/content",
        "experiment_dir": ".",
        "rnn_size": 16,
        "num_layers":2,
        "learning_rate":None,
        "window_size":20,
        "batch_size":16,
        "num_epochs":10,
        "dropout":0,
        "optimizer":"adam",
        "grad_clip":5.0,
        "message":"m",
        "n_jobs":1,
        "max_files_in_ram":25
        })

    return args

# create or load a saved model
# returns the model and the epoch number (>1 if loaded from checkpoint)
def get_model(args, experiment_dir=None):

    epoch = 0

    if not experiment_dir:
        model = Sequential()
        for layer_index in range(args.num_layers):
            kwargs = dict()
            kwargs['units'] = args.rnn_size
            # if this is the first layer
            if layer_index == 0:
                kwargs['input_shape'] = (args.window_size, OUTPUT_SIZE)
                if args.num_layers == 1:
                    kwargs['return_sequences'] = False
                else:
                    kwargs['return_sequences'] = True
                model.add(LSTM(**kwargs))
            else:
                # if this is a middle layer
                if not layer_index == args.num_layers - 1:
                    kwargs['return_sequences'] = True
                    model.add(LSTM(**kwargs))
                else: # this is the last layer
                    kwargs['return_sequences'] = False
                    model.add(LSTM(**kwargs))
            model.add(Dropout(args.dropout))
        model.add(Dense(OUTPUT_SIZE))
        model.add(Activation('softmax'))
    else:
        model, epoch = load_model_from_checkpoint(experiment_dir)

    # these cli args aren't specified if get_model() is being
    # being called from sample.py
    if 'grad_clip' in args and 'optimizer' in args:
        kwargs = { 'clipvalue': args.grad_clip }

        if args.learning_rate:
            kwargs['lr'] = args.learning_rate

        # select the optimizers
        if args.optimizer == 'sgd':
            optimizer = SGD(**kwargs)
        elif args.optimizer == 'rmsprop':
            optimizer = RMSprop(**kwargs)
        elif args.optimizer == 'adagrad':
            optimizer = Adagrad(**kwargs)
        elif args.optimizer == 'adadelta':
            optimizer = Adadelta(**kwargs)
        elif args.optimizer == 'adam':
            optimizer = Adam(**kwargs)
        elif args.optimizer == 'adamax':
            optimizer = Adamax(**kwargs)
        elif args.optimizer == 'nadam':
            optimizer = Nadam(**kwargs)
        else:
            log(
                'Error: {} is not a supported optimizer. Exiting.'.format(args.optimizer),
                True)
            exit(1)
    else: # so instead lets use a default (no training occurs anyway)
        optimizer = Adam()

    model.compile(loss='categorical_crossentropy',
                  optimizer=optimizer,
                  metrics=['accuracy'])
    return model, epoch

def get_callbacks(experiment_dir, checkpoint_monitor='val_acc'):

    callbacks = []

    # save model checkpoints
    filepath = os.path.join(experiment_dir,
                            'checkpoints',
                            'checkpoint-epoch_{epoch:03d}.hdf5'
                            )

    callbacks.append(ModelCheckpoint(filepath,
                                     monitor=checkpoint_monitor,
                                     verbose=1,
                                     save_best_only=False,
                                     mode='max'))

    callbacks.append(ReduceLROnPlateau(monitor='val_loss',
                                       factor=0.5,
                                       patience=3,
                                       verbose=1,
                                       mode='auto',
                                       epsilon=0.0001,
                                       cooldown=0,
                                       min_lr=0))


    callbacks.append(TensorBoard(log_dir=os.path.join(experiment_dir, 'tensorboard-logs'),
                                histogram_freq=0,
                                write_graph=True,
                                write_images=False))

    return callbacks


def main():

    args = parse_args()
    args.verbose = True

    try:
    	midi_files = [os.path.join(args.data_dir, path) \
                      for path in os.listdir(args.data_dir) \
                      if '.mid' in path or '.midi' in path]

    except OSError as e:
        log('Error: Invalid --data_dir, {} directory does not exist. Exiting.', args.verbose)
        exit(1)

    log(
        'Found {} midi files in {}'.format(len(midi_files), args.data_dir),
        args.verbose
    )

    if len(midi_files) < 1:
        log(
            'Error: no midi files found in {}. Exiting.'.format(args.data_dir),
            args.verbose
        )
        exit(1)

    # create the experiment directory and return its name
    experiment_dir = create_experiment_dir(args.experiment_dir, args.verbose)
    #experiment_dir = args.experiment_dir

    # write --message to experiment_dir
    if args.message:
        with open(os.path.join(experiment_dir, 'message.txt'), 'w') as f:
            f.write(args.message)
            log('Wrote {} bytes to {}'.format(len(args.message),
                os.path.join(experiment_dir, 'message.txt')), args.verbose)

    val_split = 0.1 # use 15 percent for validation
    val_split_index = int(float(len(midi_files)) * val_split)

    # use generators to lazy load train/validation data, ensuring that the
    # user doesn't have to load all midi files into RAM at once
    train_generator = get_data_generator(midi_files[0:val_split_index],
                                               window_size=args.window_size,
                                               batch_size=args.batch_size,
                                               num_threads=args.n_jobs,
                                               max_files_in_ram=args.max_files_in_ram)

    val_generator = get_data_generator(midi_files[val_split_index:],
                                             window_size=args.window_size,
                                             batch_size=args.batch_size,
                                             num_threads=args.n_jobs,
                                             max_files_in_ram=args.max_files_in_ram)

    model, epoch = get_model(args)
    if args.verbose:
        print(model.summary())

    save_model(model, experiment_dir)
    log('Saved model to {}'.format(os.path.join(experiment_dir, 'model.json')),
              args.verbose)

    callbacks = get_callbacks(experiment_dir)

    print('fitting model...')
    # this is a somewhat magic number which is the average number of length-20 windows
    # calculated from ~5K MIDI files from the Lakh MIDI Dataset.
    magic_number = 827
    start_time = time.time()
    model.fit_generator(train_generator,
                        steps_per_epoch=len(midi_files),
                        epochs=args.num_epochs,
                        validation_data=val_generator,
                        validation_steps=len(midi_files) * 0.1,
                        verbose=1,
                        callbacks=callbacks,
                        initial_epoch=epoch)
    log('Finished in {:.2f} seconds'.format(time.time() - start_time), args.verbose)

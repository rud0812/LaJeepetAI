import argparse, os, pdb, pretty_midi, easydict, time, random
from .train import *
from .utils import *

file_prefix = os.path.dirname(__file__)

def parse_args(length):

    args = easydict.EasyDict({
          "experiment_dir": ".",
          "save_dir": "outputs",
          #"midi_instrument": "Acoustic Grand Piano",
          "midi_instrument":"Electric Piano 2",
          "num_files":1,
          "file_length":length,
          "prime_file":"Daddy Yankee - Gasolina 2.mid",
          "data_dir":"content",
          })

    return args

def get_experiment_dir(experiment_dir):

	if experiment_dir == 'experiments/default':
		dirs_ = [os.path.join('experiments', d) for d in os.listdir('experiments') \
		         if os.path.isdir(os.path.join('experiments', d))]
		experiment_dir = max(dirs_, key=os.path.getmtime)

	if not os.path.exists(os.path.join(file_prefix, experiment_dir, 'model.json')):
		log('Error: {} does not exist. ' \
			      'Are you sure that {} is a valid experiment?' \
			      'Exiting.'.format(os.path.join(experiment_dir), 'model.json',
			                        experiment_dir), True)
		exit(1)

	return experiment_dir

def main_test(length=1000):
    args = parse_args(length)
    args.verbose = True

    # prime file validation
    if args.prime_file and not os.path.exists(os.path.join(file_prefix, args.data_dir, args.prime_file)):
    	log('Error: prime file {} does not exist. Exiting.'.format(args.prime_file),
    		      True)
    	exit(1)
    else:
    	if not os.path.isdir(os.path.join(file_prefix, args.data_dir)):
    		log('Error: data dir {} does not exist. Exiting.'.format(args.prime_file),
    		      True)
    		exit(1)

    midi_files = [ args.prime_file ] if args.prime_file else \
                 [ os.path.join(args.data_dir, f) for f in os.listdir(args.data_dir) \
                 if '.mid' in f or '.midi' in f ]

    experiment_dir = get_experiment_dir(args.experiment_dir)
    log('Using {} as --experiment_dir'.format(experiment_dir), args.verbose)

    if not args.save_dir:
        args.save_dir = os.path.join(file_prefix, 'outputs')

    if not os.path.isdir(os.path.join(file_prefix, args.save_dir)):
        os.makedirs(os.path.join(file_prefix, args.save_dir))
        log('Created directory {}'.format(args.save_dir), args.verbose)

    model, epoch = get_model(args, experiment_dir=experiment_dir)
    log('Model loaded from {}'.format(os.path.join(experiment_dir, 'model.json')),
              args.verbose)

    window_size = model.layers[0].get_input_shape_at(0)[1]
    seed_generator = get_data_generator(midi_files,
                                              window_size=window_size,
                                              batch_size=16,
                                              num_threads=1,
                                              max_files_in_ram=10)

    # validate midi instrument name
    try:
    	# try and parse the instrument name as an int
    	instrument_num = int(args.midi_instrument)
    	if not (instrument_num >= 0 and instrument_num <=127):
    		log('Error: {} is not a supported instrument. Number values must be ' \
    			      'be 0-127. Exiting'.format(args.midi_instrument), True)
    		exit(1)
    	args.midi_instrument = pretty_midi.program_to_instrument_name(instrument_num)
    except ValueError as err:
    	# if the instrument name is a string
    	try:
    		# validate that it can be converted to a program number
    		_ = pretty_midi.instrument_name_to_program(args.midi_instrument)
    	except ValueError as er:
    		log('Error: {} is not a valid General MIDI instrument. Exiting.'\
    			      .format(args.midi_instrument), True)
    		exit(1)

    # generate 10 tracks using random seeds
    log('Loading seed files...', args.verbose)
    X, y = next(seed_generator)
    generated = generate(model, X, window_size,
    	                       args.file_length, args.num_files, args.midi_instrument)


    path = file_prefix + "/content/drums"
    drums = glob.glob('{}/*.mid*'.format(path))
    print(len(drums))

    rand = random.randint(0,32)

    mid_drums = pretty_midi.PrettyMIDI(drums[rand])

    mid_final = pretty_midi.PrettyMIDI()

    #if generated[0].get_end_time() > mid_drums.get_end_time():
    #  for instrument in mid_drums.instruments:
    #    mid_drums.instruments.append(mid_drums.instruments)

    mid_final.instruments = generated[0].instruments + mid_drums.instruments

    filename = time.time()
    file = os.path.join(file_prefix, args.save_dir, '{}.mid'.format(filename))
    mid_final.write(file.format(filename))
    log('wrote midi file to {}'.format(file), True)

    return str(filename) + '.mid'

import keras.models as km
import keras.layers as kl
import numpy as np
import os

from config import WORK_DIR

def model_compile(network, **kwargs):
    model = getattr(km, network['model'])()
    for layer in network['layers']:
        l = getattr(kl, layer['layer'])
        model.add(l(**layer['kwargs']))
    model.compile(loss=network['loss'],
                  optimizer=network['optimizer'],
                  metrics=network['metrics'])
    return model


def model_fit(network, x, y, _id, batch_size=None,
              epochs=1, verbose=False, **kwargs):
    # fit(x=None, y=None, batch_size=None, epochs=1, verbose=1,
    # callbacks=None, validation_split=0.0, validation_data=None,
    # shuffle=True, class_weight=None, sample_weight=None,
    # initial_epoch=0, steps_per_epoch=None, validation_steps=None)
    model = model_compile(network)
    model.fit(np.array(x), np.array(y), batch_size=batch_size,
              epochs=epochs, verbose=verbose)
    _model_save(model, _id)


def model_evaluate(network, x, y, _id, fit_id, batch_size=None, **kwargs):
    # evaluate(x=None, y=None, batch_size=None,
    # verbose=1, sample_weight=None, steps=None)
    model = _model_load(fit_id)
    model.compile(loss=network['loss'],
                  optimizer=network['optimizer'],
                  metrics=network['metrics'])
    e = model.evaluate(np.array(x), np.array(y), batch_size=batch_size)
    return e


def model_predict(network, x, _id, fit_id, batch_size=None, **kwargs):
    # predict(x, batch_size=None, verbose=0, steps=None)
    model = _model_load(fit_id)
    model.compile(loss=network['loss'],
                  optimizer=network['optimizer'],
                  metrics=network['metrics'])
    p = model.predict(np.array(x), batch_size=batch_size)
    return p.tolist()


def _model_save(model, name):
    model_yaml = model.to_yaml()
    with open(os.path.join(WORK_DIR, '{}.yaml'.format(name)), 'w') as yaml_file:
        yaml_file.write(model_yaml)
    model.save_weights('{}.h5'.format(name))


def _model_load(name):
    with open(os.path.join(WORK_DIR, '{}.yaml'.format(name)), 'r') as yaml_file:
        model_yaml = yaml_file.read()
    model = km.model_from_yaml(model_yaml)
    model.load_weights('{}.h5'.format(name))
    return model

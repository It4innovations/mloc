import keras.models as km
import keras.layers as kl
import numpy as np


def model_compile(model_spec):
    model = getattr(km, model_spec['model'])()
    for layer in model_spec['layers']:
        l = getattr(kl, layer['layer'])
        model.add(l(**layer['kwargs']))
    model.compile(loss=model_spec['loss'],
                  optimizer=model_spec['optimizer'],
                  metrics=model_spec['metrics'])
    return model


def model_fit(model_spec, x, y, network_id, _id, batch_size=None, epochs=1, **kwargs):
    # fit(x=None, y=None, batch_size=None, epochs=1, verbose=1,
    # callbacks=None, validation_split=0.0, validation_data=None,
    # shuffle=True, class_weight=None, sample_weight=None,
    # initial_epoch=0, steps_per_epoch=None, validation_steps=None)
    model = model_compile(model_spec)
    model.fit(np.array(x), np.array(y), batch_size=batch_size, epochs=epochs)
    _model_save(model, _id)


def model_evaluate(model_spec, x, y, fit_id, batch_size=None, **kwargs):
    # evaluate(x=None, y=None, batch_size=None,
    # verbose=1, sample_weight=None, steps=None)
    model = _model_load(fit_id)
    model.compile(loss=model_spec['loss'],
                  optimizer=model_spec['optimizer'],
                  metrics=model_spec['metrics'])
    e = model.evaluate(np.array(x), np.array(y), batch_size=batch_size)
    return e


def model_predict(model_spec, x, fit_id, network=None, batch_size=None, **kwargs):
    # predict(x, batch_size=None, verbose=0, steps=None)
    model = _model_load(fit_id)
    model.compile(loss=model_spec['loss'],
                  optimizer=model_spec['optimizer'],
                  metrics=model_spec['metrics'])
    p = model.predict(np.array(x), batch_size=batch_size)
    return p.tolist()


def _model_save(model, name):
    model_yaml = model.to_yaml()
    with open('{}.yaml'.format(name), 'w') as yaml_file:
        yaml_file.write(model_yaml)
    model.save_weights('{}.h5'.format(name))


def _model_load(name):
    with open('{}.yaml'.format(name), 'r') as yaml_file:
        model_yaml = yaml_file.read()
    model = km.model_from_yaml(model_yaml)
    model.load_weights('{}.h5'.format(name))
    return model

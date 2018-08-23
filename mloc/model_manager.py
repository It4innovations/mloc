import keras.models as km
import keras.layers as kl
import numpy as np
import pickle


def model_compile(network, **kwargs):
    model = getattr(km, network['model'])()
    for layer in network['layers']:
        l = getattr(kl, layer['layer'])
        model.add(l(**layer['kwargs']))
    model.compile(loss=network['loss'],
                  optimizer=network['optimizer'],
                  metrics=network['metrics'])
    return model


def model_fit(network, x, y, batch_size=None,
              epochs=1, verbose=False, **kwargs):
    # fit(x=None, y=None, batch_size=None, epochs=1, verbose=1,
    # callbacks=None, validation_split=0.0, validation_data=None,
    # shuffle=True, class_weight=None, sample_weight=None,
    # initial_epoch=0, steps_per_epoch=None, validation_steps=None)
    model = model_compile(network)
    model.fit(np.array(x), np.array(y), batch_size=batch_size,
              epochs=epochs, verbose=verbose)
    res = {
        'model_json': model.to_json(),
        'model_weights': pickle.dumps(model.get_weights())
    }
    return res


def model_evaluate(network, x, y, model, batch_size=None, **kwargs):
    # evaluate(x=None, y=None, batch_size=None,
    # verbose=1, sample_weight=None, steps=None)
    model.compile(loss=network['loss'],
                  optimizer=network['optimizer'],
                  metrics=network['metrics'])
    e = model.evaluate(np.array(x), np.array(y), batch_size=batch_size)
    return {'result': e}


def model_predict(network, x, model, batch_size=None, **kwargs):
    # predict(x, batch_size=None, verbose=0, steps=None)
    model.compile(loss=network['loss'],
                  optimizer=network['optimizer'],
                  metrics=network['metrics'])
    p = model.predict(np.array(x), batch_size=batch_size)
    return {'result': p.tolist()}


def model_build(model_json, model_weights):
    model = km.model_from_json(model_json)
    model.set_weights(pickle.loads(model_weights))

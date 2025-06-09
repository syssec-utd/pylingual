def nonce_solid(name, n_inputs, n_outputs):
    """Creates a solid with the given number of (meaningless) inputs and outputs.

    Config controls the behavior of the nonce solid."""

    @solid(name=name, inputs=[InputDefinition(name='input_{}'.format(i)) for i in range(n_inputs)], outputs=[OutputDefinition(name='output_{}'.format(i)) for i in range(n_outputs)])
    def solid_fn(context, **_kwargs):
        for i in range(200):
            time.sleep(0.02)
            if i % 1000 == 420:
                context.log.error('Error message seq={i} from solid {name}'.format(i=i, name=name))
            elif i % 100 == 0:
                context.log.warning('Warning message seq={i} from solid {name}'.format(i=i, name=name))
            elif i % 10 == 0:
                context.log.info('Info message seq={i} from solid {name}'.format(i=i, name=name))
            else:
                context.log.debug('Debug message seq={i} from solid {name}'.format(i=i, name=name))
        return MultipleResults.from_dict({'output_{}'.format(i): 'foo' for i in range(n_outputs)})
    return solid_fn
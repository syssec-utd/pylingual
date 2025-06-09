def passthrough_context_definition(context_params):
    """Create a context definition from a pre-existing context. This can be useful
        in testing contexts where you may want to create a context manually and then
        pass it into a one-off PipelineDefinition

        Args:
            context (ExecutionContext): The context that will provided to the pipeline.
        Returns:
            PipelineContextDefinition: The passthrough context definition.
        """
    check.inst_param(context_params, 'context', ExecutionContext)
    context_definition = PipelineContextDefinition(context_fn=lambda *_args: context_params)
    return {DEFAULT_CONTEXT_NAME: context_definition}
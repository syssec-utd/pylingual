from ewokscore.task import Task as EwoksTask

class _LiveSlicePlaceHolder(EwoksTask, input_names=('data',), output_names=('data',)):

    def run(self):
        self.outputs.data = self.inputs.data
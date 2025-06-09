def read_as_binary(self):
    """Read and return the dataset contents as binary."""
    return self.workspace._rest.read_intermediate_dataset_contents_binary(self.workspace.workspace_id, self.experiment.experiment_id, self.node_id, self.port_name)
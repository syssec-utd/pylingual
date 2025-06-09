import numpy as np
import pandas as pd
import torch

class Dataloader:
    """class of Dataloader, which is responisble for:
    - loading data from csv file
    - transform data (e.g. standardize, normalize, differentiate) and save the parameters for inverse transformation
    - convert to tensor"""

    def __init__(self, path=None, diff_data=False, std_data=False, norm_data=False, kw_timestep='Time', col_label='Condition'):
        """Load data from csv as pandas dataframe and convert to tensor.

        Args:
            path (str): Path to csv file.
            diff_data (bool): Differentiate data.
            std_data (bool): Standardize data.
        """
        if path is not None:
            df = pd.read_csv(path)
            self.n_col_data = [index for index in range(len(df.columns)) if kw_timestep in df.columns[index]][0]
            if not isinstance(col_label, list):
                col_label = [col_label]
            dataset = torch.FloatTensor(df.to_numpy()[:, self.n_col_data:])
            labels = torch.zeros((dataset.shape[0], len(col_label)))
            for (i, l) in enumerate(col_label):
                labels[:, i] = torch.FloatTensor(df[l])
            if diff_data:
                dataset = dataset[:, 1:] - dataset[:, :-1]
            self.dataset_min = None
            self.dataset_max = None
            if norm_data:
                dataset_min = torch.min(dataset)
                dataset_max = torch.max(dataset)
                dataset = (dataset - dataset_min) / (dataset_max - dataset_min)
                self.dataset_min = dataset_min
                self.dataset_max = dataset_max
            self.dataset_mean = None
            self.dataset_std = None
            if std_data:
                dataset_mean = dataset.mean(dim=0).unsqueeze(0)
                dataset_std = dataset.std(dim=0).unsqueeze(0)
                self.dataset_mean = dataset_mean
                self.dataset_std = dataset_std
                dataset = (dataset - dataset_mean) / dataset_std
            dataset = torch.concat((labels, dataset), 1)
            self.dataset = dataset
            self.labels = labels

    def get_data(self, sequence_length=None, windows_slices=False, stride=1, pre_pad=0, shuffle=True):
        """returns the data as a tensor"""
        if windows_slices:
            data = torch.zeros((self.dataset.shape[0], self.dataset.shape[-1] + pre_pad))
            data[:, :self.labels.shape[1]] = self.labels
            data[:, pre_pad + self.labels.shape[-1]:] = self.dataset[:, self.labels.shape[-1]:]
            if sequence_length < 0 or sequence_length + stride > self.dataset.shape[1]:
                raise ValueError(f'If windows slices are used, the sequence_length must be positive and smaller than len(data) (={self.dataset.shape[1] - self.labels.shape[1]}) + stride (={stride}).')
            dataset = self.windows_slices(data, sequence_length, stride=stride)
        elif windows_slices is False and sequence_length:
            if sequence_length == -1:
                sequence_length = self.dataset.shape[1] - self.labels.shape[1]
            if sequence_length < 0 or sequence_length > self.dataset.shape[1] - self.labels.shape[1]:
                raise ValueError(f'If windows slices are not used, the sequence_length must be smaller than len(data) (={self.dataset.shape[1] - self.labels.shape[1]}).')
            dataset = self.dataset[:, :sequence_length + self.labels.shape[1]]
        else:
            dataset = self.dataset
        if shuffle:
            dataset = dataset[torch.randperm(dataset.shape[0])]
        return dataset

    def get_labels(self):
        return self.labels

    def dataset_split(self, dataset=None, train_size=0.8, test_size=None, shuffle=True):
        """Split dataset into train and test set. Returns the indices of the split."""
        if dataset is None:
            dataset = self.dataset
        if test_size is None:
            test_size = 1 - train_size
        if train_size + test_size > 1:
            raise ValueError(f'train_size + test_size (={train_size}+{test_size}) must be >= 1.')
        train_size = int(train_size * dataset.shape[0])
        test_size = int(test_size * dataset.shape[0])
        if shuffle:
            indices = torch.randperm(dataset.shape[0])
            dataset = dataset[indices]
        else:
            indices = torch.arange(dataset.shape[0])
        train_dataset = dataset[:train_size]
        test_dataset = dataset[train_size:train_size + test_size]
        train_idx = indices[:train_size]
        test_idx = indices[train_size:train_size + test_size]
        return (train_dataset, test_dataset, train_idx, test_idx)

    def downsample(self, target_sequence_length):
        """Downsample data to target_sequence_length"""
        step_size = self.dataset.shape[1] // target_sequence_length
        self.dataset = torch.concat((self.labels, self.dataset[:, self.labels.shape[1]::step_size]), dim=1)

    def get_mean(self):
        return self.dataset_mean

    def get_std(self):
        return self.dataset_std

    def windows_slices(self, sequence, window_size, stride=5):
        """Create a moving window of size window_size with stride stride.
        The last window is padded with 0 if it is smaller than window_size.

        Args:
            sequence (iterable): Input sequence.
            window_size (int): Size of the window.
            stride (int): Stride of the window.

        Returns:
            torch.Tensor: Tensor of windows.
        """
        n_labels = self.labels.shape[1]
        sequence = sequence[:, n_labels:]
        windows = torch.zeros(((sequence.shape[1] - window_size) // stride, sequence.shape[0], window_size + n_labels))
        last_index = sequence.shape[1] - (window_size + stride) + 1
        for i in range(0, last_index, stride):
            windows[-((sequence.shape[1] - window_size - i) // stride)] = torch.cat((self.labels, sequence[:, i:i + window_size]), dim=-1)
        if sequence.shape[1] < last_index + stride + window_size:
            last_window = torch.zeros_like(windows[-1])
            last_window[:, :n_labels] = self.labels
            last_window[:, n_labels:n_labels + sequence.shape[1] - i - window_size] = sequence[:, i + window_size:]
            windows[-1] = last_window
        return windows.view(-1, n_labels + window_size)

    def inverse_norm(self, data):
        """Inverse normalize data. Used also for generated samples by the generator."""
        if not isinstance(data, torch.Tensor):
            dataset_max = self.dataset_max.detach().cpu().numpy()
            dataset_min = self.dataset_min.detach().cpu().numpy()
        else:
            dataset_max = self.dataset_max
            dataset_min = self.dataset_min
        data = data * (dataset_max - dataset_min) + dataset_min
        return data

    def inverse_std(self, data):
        """Inverse standardize data. Used also for generated samples by the generator."""
        if not isinstance(data, torch.Tensor):
            dataset_mean = self.dataset_mean.detach().cpu().numpy()
            dataset_std = self.dataset_std.detach().cpu().numpy()
        else:
            dataset_mean = self.dataset_mean
            dataset_std = self.dataset_std
        data = data * dataset_std + dataset_mean
        return data

    @staticmethod
    def inverse_diff(data, dim):
        """Inverse differentiate data. Used also for generated samples by the generator."""
        if isinstance(data, torch.Tensor):
            data = torch.cumsum(data, dim=dim)
        else:
            data = np.cumsum(data, axis=dim)
        return data

    def to_csv(self, path):
        """Save data to csv file"""
        if self.dataset is None:
            raise ValueError('Dataset is None. Please load data first.')
        pd.DataFrame(self.dataset.detach().cpu().numpy()).to_csv(path)
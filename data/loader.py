from halfkp_libs.halfkp_lib import Half_KP_Converter
from halfkp_libs.chess_lib import Chess_Lib
from torch.utils.data import Dataset, DataLoader
import os

class Chess_Dataset(Dataset):

    def __init__(self, data_path):
        self.pos_fen = []
        self.eval = []
        self.mate = []
        self.hkp_converter = Half_KP_Converter()
        self.load_data(data_path)

    def __len__(self):
        return len(self.mate)

    def __getitem__(self, idx):
        return self.pos_fen[idx], self.eval[idx], self.mate[idx]

    def load_data(self, data_path):
        with open(data_path, 'r') as file:
            lines = file.readlines()
        for line in lines:
            values = line.strip().split(';')
            fen = values[0]
            fen_tensor = self.hkp_converter.fen2tensor(fen)
            eval = values[1]
            mate = abs(int(values[2]))
            new_eval = Chess_Lib.get_eval_value(eval, mate)
            self.pos_fen.append(fen_tensor)
            self.pos_fen.append(new_eval)
            self.pos_fen.append(mate)

def fetch_dataloader(types = ['train', 'val', 'test'], batch_size = 1, dir = "/content/drive/MyDrive/ai_chess/krk/data", num_workers = 1, pin_memory = True, data_file_name = "KRk.csv"):
    """
    Fetches the DataLoader object for each type in types from data_dir.

    Args:
        types: (list) has one or more of 'train', 'val', 'test' depending on which data is required
        data_dir: (string) directory containing the dataset
        params: (Params) hyperparameters

    Returns:
        data: (dict) contains the DataLoader object for each type in types
    """
    dataloaders = {}

    for split in ['train', 'val', 'test']:
        if split in types:
            path = os.path.join(dir, split, data_file_name)

            # use the train_transformer if training data, else use eval_transformer without random flip
            if split == 'train':
                dl = DataLoader(Chess_Dataset(path), batch_size=batch_size, shuffle=True,
                                        num_workers=num_workers,
                                        pin_memory=pin_memory)
            else:
                dl = DataLoader(Chess_Dataset(path), batch_size=batch_size, shuffle=False,
                                num_workers=num_workers,
                                pin_memory=pin_memory)

            dataloaders[split] = dl

    return dataloaders

import pandas as pd
import numpy as np
import os


class DataManager:
    def __init__(self, metadata_path, images_base_path, smart_sort=False):
        self.current_index = 0
        self.df = pd.read_csv(metadata_path)
        if smart_sort:
            self.df = self.sort_by_certainty()
        else:
            self.df = pd.
        self.images_base_path = images_base_path

    def sort_by_certainty(self):
        pred_cols = [x for x in self.df.columns if x.startswith('class')]
        self.df['certainty'] = self.df[pred_cols].var(axis='columns')
        return self.df.sort_values(by='certainty', ascending=True)

    def current_data(self):
        data = self.df.iloc[self.current_index].copy()
        data['image_path'] = '/images/' + data['image_path']
        return data

    # TODO: this presumes that all possible labels have surfaced
    def unique_labels(self):
        return self.df['label'].unique()

    def change_label(self, new_label):
        self.df.at[self.current_index, 'label'] = new_label

    def use_predicted_label(self):
        self.df.at[self.current_index, 'label'] = self.df.at[self.current_index, 'prediction']

    def next_image(self):
        self.current_index = min(self.current_index + 1, len(self.df) - 1)

    def previous_image(self):
        self.current_index = max(self.current_index - 1, 0)

    def delete_image(self):
        os.remove(os.path.join(self.images_base_path, self.df.at[self.current_index, 'image_path']))
        self.df = self.df.drop(self.df.index[self.current_index])
        self.df = self.df.reset_index(drop=True)
        self.current_index = min(self.current_index, len(self.df) - 1)

    def save_changes(self):
        self.df.to_csv('new_metadata.csv', index=False)

    def get_progress(self):
        return {
            'current': self.current_index + 1,
            'total': len(self.df)
        }

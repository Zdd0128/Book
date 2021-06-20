from conf import settings

import pickle
import os


def select_data(cls, username):
    class_name = cls.__name__
    user_data_path = os.path.join(
        settings.DB_PATH, class_name
    )

    if os.path.exists(user_data_path):
        user_path = os.path.join(
            user_data_path, username
        )

        if os.path.exists(user_path):
            with open(user_path, 'rb') as f:
                obj = pickle.load(f)
                return obj


def save_data(obj):
    class_name = obj.__class__.__name__
    user_data_path = os.path.join(
        settings.DB_PATH, class_name
    )
    if not os.path.exists(user_data_path):
        os.mkdir(user_data_path)

    user_path = os.path.join(
        user_data_path, obj.user
    )

    with open(user_path, 'wb') as f:
        pickle.dump(obj, f)

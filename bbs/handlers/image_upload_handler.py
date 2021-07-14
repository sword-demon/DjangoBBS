import json
import time

from utils.tools import get_random_set


class ImageUploadHandler:
    # 只允许以下后缀的
    _allowed_ext = ['png', 'jpg', 'jpeg', 'gif']

    def save(self, file, folder, file_prefix):
        # 构建文件夹存储规则
        folder_name = "media/uploads/images/" + folder + "/" + str(time.time())

        file_name = file.name
        print(file_name)
        # 获取后缀
        ext = file_name.rsplit('.')[0]
        if ext not in self._allowed_ext:
            return False

        # 组装filename
        file_name = file_prefix + "_" + str(time.time()) + get_random_set(10) + "." + ext

        return json.dumps({
            'path': file_name
        })

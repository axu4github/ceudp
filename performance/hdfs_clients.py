# -*- coding: UTF-8 -*-

import os
from performance.settings import settings
# from hdfs.client import Client, HdfsError
from hdfs.client import HdfsError
from ceudp.utilities.loggables import Loggable
from performance.utils import Utils


class HDFSClient(Loggable):
    """hdfs client"""

    hdfs_root_dir = settings.HDFS_ROOT_DIR
    unstructured_data_root_dir = settings.HDFS_UNSTRUCTURED_DATA_DIR

    def __init__(self, hdfs_url=settings.HDFS_WEB_URL, **kwargs):
        super(HDFSClient, self).__init__()
        # self.hdfs_client = Client(hdfs_url, **kwargs)
        self.hdfs_client = settings.HDFS_CLIENT

    def makedirs(self, hdfs_dir, **kwargs):
        hdfs_real_path = self.get_real_path(hdfs_dir)
        if self.hdfs_client.status(hdfs_real_path, strict=False) is None:
            return self.hdfs_client.makedirs(hdfs_real_path, **kwargs)

    def status(self, hdfs_path, repath=True, **kwargs):
        try:
            hdfs_real_path = hdfs_path
            if repath:
                hdfs_real_path = self.get_real_path(hdfs_path)

            return self.hdfs_client.status(hdfs_real_path, **kwargs)
        except HdfsError as e:
            raise Exception("HDFS File is not exist: {0}".format(hdfs_path))

    def upload(self, hdfs_path, local_path, **kwargs):
        hdfs_real_path = self.get_real_path(hdfs_path)
        self.log_debug("upload hdfs_path {0}".format(hdfs_real_path))
        self.log_debug("upload local_path {0}".format(local_path))
        if hdfs_real_path.endswith("/"):
            self.hdfs_client.makedirs(hdfs_real_path)
            file_name = os.path.basename(local_path)
            hdfs_path = "{0}{1}".format(hdfs_path, file_name)
            hdfs_real_path = "{0}{1}".format(hdfs_real_path, file_name)

        if not os.path.exists(local_path):
            raise Exception("LocalPath ({0}) not exists.".format(local_path))

        response = self.hdfs_client.upload(
            hdfs_real_path, local_path, **kwargs)
        file_info = self.list(response, repath=False)
        file_info = file_info["docs"][0]
        file_info.update({
            'showPath': hdfs_path,
            'realPath': hdfs_real_path,
            'localPath': local_path,
        })

        # self.create_index(file_info)

        return response

    def delete(self, hdfs_path, repath=True, **kwargs):
        try:
            hdfs_real_path = hdfs_path
            if repath:
                hdfs_real_path = self.get_real_path(hdfs_path)

            # self.delete_index(hdfs_real_path)
            return self.hdfs_client.delete(hdfs_real_path, **kwargs)
        except HdfsError as e:
            raise Exception("HDFS Dir is not emtpy: {0}".format(hdfs_path))

    def list(self, hdfs_path, status=True, repath=True):
        try:
            hdfs_real_path = hdfs_path
            if repath:
                hdfs_real_path = self.get_real_path(hdfs_path)

            file_status = self.hdfs_client.status(hdfs_real_path)

            items = []
            if file_status['type'] == 'FILE':
                file_status.update(
                    {"realPath": hdfs_real_path, "showPath": hdfs_path})
                items.append([hdfs_path, file_status])
            else:
                items = self.hdfs_client.list(hdfs_real_path, status=True)
                for item in items:
                    if not hdfs_path.endswith("/"):
                        hdfs_path += "/"

                    if not hdfs_real_path.endswith("/"):
                        hdfs_real_path += "/"

                    showPath = hdfs_path + item[0]
                    realPath = hdfs_real_path + item[0]
                    item[1].update(
                        {"showPath": showPath, "realPath": realPath})

            docs = []
            for item in items:
                doc = item[1]
                doc.update({
                    "filename": os.path.basename(item[0]),
                })

                docs.append(doc)

            return {"numFound": len(docs), "docs": docs}
        except HdfsError as e:
            raise Exception("HDFS File is not exist: {0}".format(hdfs_path))

    def download(self, hdfs_path, local_path, overwrite=True, repath=True, **kwargs):
        try:
            hdfs_real_path = hdfs_path
            if repath:
                hdfs_real_path = self.get_real_path(hdfs_path)

            self.log_debug(
                "Fucntion-download (hdfs_path, local_path) : ({0}, {1})".format(hdfs_real_path, local_path))

            self.hdfs_client.download(
                hdfs_real_path, local_path, overwrite=overwrite, **kwargs)

            return local_path
        except HdfsError as e:
            raise Exception("HDFS File is not exist: {0}".format(hdfs_path))

    def write(self, hdfs_path, data=None, filename=None, overwrite=True, **kwargs):
        try:
            # 判断hdfs_path路径是否存在文件名
            if os.path.basename(hdfs_path) == '':
                hdfs_path = "{0}{1}".format(hdfs_path, filename)

            hdfs_real_path = self.get_real_path(hdfs_path)

            return self.hdfs_client.write(hdfs_real_path, data=data,
                                          overwrite=overwrite, **kwargs)
        except Exception as e:
            raise e

    def is_file(self, hdfs_path):
        return "FILE" == self.status(hdfs_path)['type']

    def get_real_path(self, path):
        return "{0}{1}".format(self.unstructured_data_root_dir, path)

    def create_index(self, file_info):
        doc = file_info
        doc.update({
            'id': file_info['realPath'],
            'filename': os.path.basename(file_info['realPath']),
            'fileContents': Utils.get_contents(file_info['localPath']),
            'fileExtension': Utils.file_extension(file_info['realPath']),
        })

        settings.SOLR_CONNECTION.add([doc])
        settings.SOLR_CONNECTION.commit()

    def delete_index(self, id):
        response = settings.SOLR_CONNECTION.search(
            {'q': 'id:"{0}"'.format(id)}).result.response

        if response.numFound > 0:
            settings.SOLR_CONNECTION.delete({'q': 'id:"{0}"'.format(id)})

    def search(self, contents, start=0, limit=10):
        """
        response example:
        {
            "start": 0,
            "numFound": 1,
            "docs": [
                {
                    "file_name": "people.txt",
                    "file_extension": ".txt",
                    "real_path": "/queryengine/unstructured_datas/test_search/people.txt",
                    "show_path": "/test_search/people.txt",
                    "local_path": "/Users/axu/code/axuProject/queryengine//queryengine/fixtures/people.txt",
                    "file_size": 32,
                    "_version_": 1569332496748773376,
                    "id": "/queryengine/unstructured_datas/test_search/people.txt"
                }
            ]
        }
        """
        return settings.SOLR_CONNECTION.search(
            {'q': 'fileContents:"{0}"'.format(contents), 'start': start, 'rows': limit}).result.response.dict

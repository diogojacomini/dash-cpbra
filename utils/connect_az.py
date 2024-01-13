from conf.variables import CONNECTION_STRING
from azure.storage.blob import BlobServiceClient
from pandas import read_csv
import io
import json


class AzureStore():

    def __init__(self) -> None:
        self.CONNECTION_STRING = CONNECTION_STRING
        self.connect()

    def connect(self):
        self.client = BlobServiceClient.from_connection_string(self.CONNECTION_STRING)

    def get_container(self, container_name):
        return self.client.get_container_client(container_name)

    def get_file(self, container_name, filename):
        return self.client.get_blob_client(container=container_name, blob=filename)

    def read_lake(self, container_name, filename):
        """
        Lê um arquivo de um contêiner no Azure Blob Storage.

        Args:
            container_name (str): O nome do contêiner no Azure Blob Storage.
            filename (str): O nome do arquivo a ser lido.

        Returns:
            DataFrame or dict or None: Os dados lidos do arquivo, dependendo do tipo do arquivo.
                                    Retorna None em caso de erro.
        """
        file_client = self.get_file(container_name, filename)
        try:
            data = file_client.download_blob()
            content = data.readall()

            if filename.endswith('.csv'):
                return read_csv(io.StringIO(content.decode('utf-8')))

            elif filename.endswith('.json'):
                return json.loads(content)
            
            elif filename.endswith('.ipynb'):
                #logging.warning("read_lake:ipynb")
                return content#data.readall()#.decode('utf-8') 
            else:
                pass
                #logging.warning("read_lake: Warning! Tipo de arquivo diferente de csv ou json.")
                #logging.warning("Se novo tipo de arquivo for adicionado, é preciso atualizar a function: read_lake")

        except Exception as error_read_lake:
            #logging.error('read_lake: error_read_lake: {0}'.format(str(error_read_lake)))
            return None
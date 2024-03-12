from pathlib import Path

SHAREPOINT_AUTHORITY = "https://login.microsoftonline.com/organizations/oauth2/v2.0/token"
SHAREPOINT_CLIENT_ID = '688f3485-f34a-4c4c-80ff-396f3ce3d7ea'
SP_ROOT = "stateofwa.sharepoint.com"
SP_FOLDER_BASE_PATH = '/General'
SHAREPOINT_SCOPES = ['Files.ReadWrite.All', 'Sites.ReadWrite.All', 'offline_access']
DSSU_SUFFIX = r'sites/DOH-DataScienceSupport'

basepath = Path(__file__).parent 

DOWNLOAD_PATH = basepath / 'data//docs'

LOG_FILE = basepath / 'util//logging//log.txt'


DOCTOKEN_CACHE_PATH = basepath / 'data//docs//document_token_cache.pickle'

CORPUS_PATH = basepath / 'data//app//corpus/dssu_docs.mm'
DICTIONARY_PATH = basepath / 'data//app//dictionary/dssu_docs.dict'
MODEL_PATH = basepath / 'data//app//model/'
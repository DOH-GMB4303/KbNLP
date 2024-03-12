import kbnlp.configs as cfg
from kbnlp.util.preprocesser import Preprocesser

from itertools import chain
from O365 import Account
from pathlib import Path
import logging
import re
import PyPDF2
import docx

logger = logging.getLogger(__name__)

print(__name__)


class SPFetch(object):
    SHAREPOINT_SCOPES = ["basic", "onedrive_all", "sharepoint_dl"]

    def __init__(self, sp_folder_suffix=cfg.DSSU_SUFFIX):
        self.sp_folder_suffix = sp_folder_suffix
        self.account = Account(
            cfg.SHAREPOINT_CLIENT_ID,
            scopes=self.SHAREPOINT_SCOPES,
            auth_flow_type="public",
        )
        self.check_get_authenticate()
        self.conn = self.account.sharepoint()
        self.folder = list(
            self.conn.get_site(cfg.SP_ROOT, sp_folder_suffix)
            .get_default_document_library()
            .get_child_folders()
        )
        self.documents = chain.from_iterable(self.get_documents(f) for f in self.folder)
        self.processed_docs = self._process()

        self.doc_dict = 'Iterate first to generate this'

    def __repr__(self):
        return f"SPFetch(r'{self.sp_folder_suffix}')"

    def __iter__(self):
        return self.processed_docs

    def check_get_authenticate(self):
        if not self.account.is_authenticated:
            self.account.authenticate()
        return self.account.is_authenticated

    @staticmethod
    def alr_downloaded(docname):
        with open(cfg.LOG_FILE, "r") as f:
            return docname in f.read()

    def _log_fobj(self, fobj):
        with open(cfg.LOG_FILE, "a") as f:
            f.write(fobj.name + "\n")

    def get_documents(self, folder):
        for fobj in folder.get_items():
            if fobj.is_file:
                if fobj.name.endswith(("docx", "pdf")) and not self.alr_downloaded(
                    fobj.name
                ):
                    fobj.download(cfg.DOWNLOAD_PATH)
                    self._log_fobj(fobj)
                    fpath = (Path(cfg.DOWNLOAD_PATH) / fobj.name).absolute().resolve()
                    yield fpath
                    fpath.unlink(missing_ok=True)
                    continue
            if fobj.is_folder:
                yield from self.get_documents(fobj)
            else:
                continue

    def _process(self):
        doc_dict = {}
        for docpath in self.documents:
            docpath.name
            if docpath:
                raw_text = MultiReader.read_document(docpath)
                # yield tokens
                yield (output := Preprocesser.process(raw_text))
                doc_dict[docpath.name] = output
        self.doc_dict = doc_dict
class MultiReader:
    @staticmethod
    def read_document(fpath):
        if fpath.suffix == ".docx":
            return MultiReader.clean_text(MultiReader._read_docx(fpath))
        if fpath.suffix == ".txt":
            pass
        if fpath.suffix == ".pdf":
            return MultiReader.clean_text(MultiReader._read_pdf(fpath))

    def __call__(self, fpath):
        return self.read_document(fpath)

    @staticmethod
    def _read_pdf(fpath):
        with open(fpath, "rb") as f:
            pdf = PyPDF2.PdfFileReader(f)
            text = ""
            for page in pdf.pages:
                text += page.extractText()
        return text

    @staticmethod
    def clean_text(text):
        pattern = r"\n[0-9]|\no|\n|\s{2,}"
        try:
            text = re.sub(pattern, " ", text)
        except:
            print("Error in cleaning text")
        finally:
            return text

    @staticmethod
    def _read_docx(fpath):
        import docx

        try:
            doc = docx.Document(fpath)
        except:
            return
        full_text = []
        for paragraph in doc.paragraphs:
            full_text.append(paragraph.text)
        return "\n".join(full_text)


if __name__ == "__main__":
    spdocs = SPFetch()
    for doc in spdocs:
        pass
    spdocs.doc_dict

import sys
from pathlib import Path

from PyQt5 import QtCore, QtGui, QtWidgets

from .database import init_db, insert_certificate, fetch_certificates
from .ocr import extract_text_from_file
from .rules import RuleConfig, RuleEngine
from .models import CertificateOfInsurance


class UploadWidget(QtWidgets.QWidget):
    file_loaded = QtCore.pyqtSignal(Path, str)

    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        self.button = QtWidgets.QPushButton('Upload COI')
        self.preview = QtWidgets.QLabel('No file loaded')
        self.preview.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(self.button)
        layout.addWidget(self.preview)
        self.button.clicked.connect(self.open_file)

    def open_file(self):
        path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Select COI', '', 'PDF Files (*.pdf);;Images (*.png *.jpg *.jpeg)')
        if path:
            text = extract_text_from_file(path) or ''
            pixmap = QtGui.QPixmap(path)
            if pixmap.isNull():
                self.preview.setText('Preview not available')
            else:
                self.preview.setPixmap(pixmap.scaled(200, 200, QtCore.Qt.KeepAspectRatio))
            self.file_loaded.emit(Path(path), text)


class RuleConfigWidget(QtWidgets.QWidget):
    config_changed = QtCore.pyqtSignal(RuleConfig)

    def __init__(self):
        super().__init__()
        layout = QtWidgets.QFormLayout(self)
        self.limit_edit = QtWidgets.QLineEdit()
        self.desc_edit = QtWidgets.QLineEdit()
        self.insured_edit = QtWidgets.QLineEdit()
        layout.addRow('Policy Limits (comma separated)', self.limit_edit)
        layout.addRow('Description Language', self.desc_edit)
        layout.addRow('Additional Insured (comma separated)', self.insured_edit)
        for edit in (self.limit_edit, self.desc_edit, self.insured_edit):
            edit.textChanged.connect(self.emit_config)

    def emit_config(self):
        config = RuleConfig(
            policy_limits=[s.strip() for s in self.limit_edit.text().split(',') if s.strip()],
            description_language=[self.desc_edit.text()] if self.desc_edit.text() else [],
            additional_insured=[s.strip() for s in self.insured_edit.text().split(',') if s.strip()],
        )
        self.config_changed.emit(config)


class ResultWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        layout = QtWidgets.QVBoxLayout(self)
        self.result_label = QtWidgets.QLabel('No results')
        layout.addWidget(self.result_label)

    def show_result(self, coi: CertificateOfInsurance):
        if coi.matched:
            text = f'COI {coi.id} PASSED'
        else:
            text = f'COI {coi.id} FAILED: {"; ".join(coi.mismatches)}'
        self.result_label.setText(text)


def main():
    init_db()
    app = QtWidgets.QApplication(sys.argv)

    splitter = QtWidgets.QSplitter()
    upload = UploadWidget()
    rules = RuleConfigWidget()
    results = ResultWidget()

    splitter.addWidget(upload)
    splitter.addWidget(rules)
    splitter.addWidget(results)
    splitter.setSizes([200, 200, 200])

    engine = RuleEngine(RuleConfig())

    def process_file(path: Path, text: str):
        cid = insert_certificate('Tenant', str(path))
        coi = CertificateOfInsurance(id=cid, tenant='Tenant', file_path=str(path), raw_text=text)
        coi = engine.evaluate(coi)
        results.show_result(coi)

    def update_config(config: RuleConfig):
        engine.config = config

    upload.file_loaded.connect(process_file)
    rules.config_changed.connect(update_config)

    main_window = QtWidgets.QMainWindow()
    main_window.setWindowTitle('COI Tracker Prototype')
    main_window.setCentralWidget(splitter)
    main_window.resize(800, 600)
    main_window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

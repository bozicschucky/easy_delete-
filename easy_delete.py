import os
import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QHBoxLayout, QWidget, QFileDialog, QProgressBar, QDateEdit, QMessageBox, QDesktopWidget
from PyQt5.QtCore import QDate
import sys
from utils import count_files_and_folders, delete_files_and_folders_with_progress

class CleanupTool(QMainWindow):
    def __init__(self):
        super().__init__()

        # Get screen size
        screen = QDesktopWidget().screenGeometry()
        # Set window size to 25% & 15% of the screen size
        width = int(screen.width() * 0.25)
        height = int(screen.height() * 0.15)

        self.setWindowTitle("File and Folder Cleanup Tool")
        self.setGeometry(100, 100, width, height)
        self.setFixedSize(width, height)
        self.center()
        self.initUI()

    def center(self):
        # Get the screen geometry
        screen = QDesktopWidget().screenGeometry()
        # Get window geometry
        size = self.geometry()
        # Calculate center position
        x = (screen.width() - size.width()) // 2
        y = (screen.height() - size.height()) // 2
        # Move window to center
        self.move(x, y)

    def initUI(self):
        layout = QVBoxLayout()

        # Folder path and browse button in the same row
        folder_layout = QHBoxLayout()
        self.folder_path_entry = QLineEdit(self)
        self.folder_path_entry.setPlaceholderText("Select folder path")
        self.folder_path_entry.setFixedWidth(int(0.45 * self.width()))
        folder_layout.addWidget(self.folder_path_entry)

        self.browse_button = QPushButton("Browse", self)
        self.browse_button.setFixedWidth(int(0.25 * self.width()))
        self.browse_button.clicked.connect(self.browse_folder)
        folder_layout.addWidget(self.browse_button)

        layout.addLayout(folder_layout)

        # Date picker and label in the same row
        date_layout = QHBoxLayout()
        self.date_label = QLabel("Select the date threshold:")
        date_layout.addWidget(self.date_label)

        self.delete_date_entry = QDateEdit(self)
        self.delete_date_entry.setDisplayFormat('yyyy-MM-dd')
        self.delete_date_entry.setDate(QDate.currentDate())
        self.delete_date_entry.setFixedWidth(int(0.45 * self.width()))
        date_layout.addWidget(self.delete_date_entry)

        layout.addLayout(date_layout)

        # Start button
        self.start_button = QPushButton("Start Deletion", self)
        self.start_button.setFixedWidth(int(0.25 * self.width()))
        self.start_button.clicked.connect(self.start_deletion)
        layout.addWidget(self.start_button)

        # Progress bar
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Status label
        self.status_label = QLabel("")
        layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Folder")
        self.folder_path_entry.setText(folder_path)

    def start_deletion(self):
        folder_path = self.folder_path_entry.text()
        delete_date = selected_date = self.delete_date_entry.date()
        # Convert QDate to Python datetime, setting time to midnight (00:00:00)
        date_threshold = datetime.datetime(
            selected_date.year(),
            selected_date.month(),
            selected_date.day()
        )

        if not folder_path or not delete_date:
            QMessageBox.critical(
                self, "Error", "Please provide both folder path and date threshold.")
            return

        if not os.path.exists(folder_path):
            QMessageBox.critical(
                self, "Error", "❌ The provided folder path does not exist.")
            return

        total_items = count_files_and_folders(folder_path)
        if total_items == 0:
            QMessageBox.information(
                self, "Info", "The folder is already empty. Nothing to delete.")
            return

        confirm = QMessageBox.question(
            self, "Confirmation",
            f'''Are you sure you want to delete all files older than {
                selected_date.toString('yyyy-MM-dd')}?\nThis action is irreversible.''',
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm == QMessageBox.Yes:
            self.progress_bar.setValue(0)
            self.progress_bar.setVisible(True)
            deleted_files, deleted_dirs = delete_files_and_folders_with_progress(
                self, folder_path, date_threshold, self.progress_bar, self.status_label)
            self.progress_bar.setValue(100)
            self.status_label.setText("")
            QMessageBox.information(
                self,
                "Success",
                f"✅ Deletion process completed.\nTotal files deleted: {
                    len(deleted_files)}\nTotal empty folders deleted: {len(deleted_dirs)}"
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CleanupTool()
    window.show()
    sys.exit(app.exec_())

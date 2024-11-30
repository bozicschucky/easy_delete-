import datetime
import os
from tkinter import messagebox
from PyQt5.QtWidgets import QApplication, QMessageBox


def count_files_and_folders(folder_path):
    total_items = 0
    for _, dirs, files in os.walk(folder_path):
        total_items += len(files) + len(dirs)
    return total_items


def delete_files_and_folders_with_progress(window, folder_path, date_threshold, progress_bar, status_label):
    deleted_files = []
    deleted_dirs = []
    items_processed = 0
    total_items = count_files_and_folders(folder_path)

    for root_dir, dirs, files in os.walk(folder_path, topdown=False):
        for name in files:
            file_path = os.path.join(root_dir, name)
            try:
                file_mtime = datetime.datetime.fromtimestamp(
                    os.path.getmtime(file_path))
                if file_mtime < date_threshold:
                    os.remove(file_path)
                    deleted_files.append(file_path)
            except Exception as e:
                messagebox.warning(
                    window, "Warning", f"⚠️ Failed to delete file {file_path}: {e}")
            items_processed += 1
            progress_bar.setValue(int((items_processed / total_items) * 100))
            status_label.setText(f"Currently deleting: {file_path}")
            QApplication.processEvents()

        for name in dirs:
            dir_path = os.path.join(root_dir, name)
            try:
                if not os.listdir(dir_path):  # Check if the directory is empty
                    os.rmdir(dir_path)
                    deleted_dirs.append(dir_path)
            except Exception as e:
                QMessageBox.warning(
                    window, "Warning", f"⚠️ Failed to delete folder {dir_path}: {e}")
            items_processed += 1
            progress_bar.setValue(int((items_processed / total_items) * 100))
            status_label.setText(f"Currently deleting: {dir_path}")
            QApplication.processEvents()

    return deleted_files, deleted_dirs

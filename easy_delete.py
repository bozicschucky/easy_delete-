import streamlit as st
import os
import datetime


def count_files_and_folders(folder_path):
    total_items = 0
    for root, dirs, files in os.walk(folder_path):
        total_items += len(files) + len(dirs)
    return total_items


def delete_files_and_folders_with_progress(folder_path, date_threshold, progress_bar, status_text):
    deleted_files = []
    deleted_dirs = []
    items_processed = 0
    total_items = count_files_and_folders(folder_path)

    for root, dirs, files in os.walk(folder_path, topdown=False):
        for name in files:
            file_path = os.path.join(root, name)
            try:
                file_mtime = datetime.datetime.fromtimestamp(
                    os.path.getmtime(file_path))
                if file_mtime < date_threshold:
                    os.remove(file_path)
                    deleted_files.append(file_path)
            except Exception as e:
                st.warning(f"⚠️ Failed to delete file {file_path}: {e}")
            items_processed += 1
            progress_bar.progress(items_processed / total_items)
            status_text.text(f"Currently deleting: {file_path}")

        for name in dirs:
            dir_path = os.path.join(root, name)
            try:
                if not os.listdir(dir_path):  # Check if the directory is empty
                    os.rmdir(dir_path)
                    deleted_dirs.append(dir_path)
            except Exception as e:
                st.warning(f"⚠️ Failed to delete folder {dir_path}: {e}")
            items_processed += 1
            progress_bar.progress(items_processed / total_items)
            status_text.text(f"Currently deleting: {dir_path}")

    return deleted_files, deleted_dirs


# Streamlit UI
st.title("File and Folder Cleanup Tool with Progress")
st.markdown(
    "This tool helps you delete files and folders older than a specific date, with a progress tracker.")

# Inputs
folder_path = st.text_input("Enter the folder path to scan:")
folder_path = r"{}".format(folder_path)
delete_date = st.date_input("Select the date threshold:")
delete_button = st.button("Start Deletion")

if delete_button and folder_path and delete_date:
    st.session_state.confirmation = True

if st.session_state.get('confirmation', False):
    st.warning(
        "Are you sure you want to delete the files? This action is irreversible.")

    col1, col2 = st.columns([1, 1])
    with col1:
        confirm_yes = st.button("Yes, delete")
    with col2:
        confirm_no = st.button("No, cancel")

    if confirm_yes:
        st.session_state.confirmation = False
        try:
            date_threshold = datetime.datetime.combine(
                delete_date, datetime.datetime.min.time())
            if not os.path.exists(folder_path):
                st.error("❌ The provided folder path does not exist.")
            else:
                total_items = count_files_and_folders(folder_path)
                if total_items == 0:
                    st.info("The folder is already empty. Nothing to delete.")
                else:
                    st.info(f"⏳ Starting deletion process for {total_items} items...")
                    # Initialize progress bar
                    progress_bar = st.progress(0)
                    status_text = st.empty()  # Placeholder for current file being deleted
                    deleted_files, deleted_dirs = delete_files_and_folders_with_progress(
                        folder_path, date_threshold, progress_bar, status_text
                    )
                    progress_bar.progress(1.0)  # Set progress bar to 100%
                    progress_bar.empty()  # Clear the progress bar
                    st.success("✅ Deletion process completed.")
                    st.write(f"**Total files deleted:** {len(deleted_files)}")
                    st.write(
                        f"**Total empty folders deleted:** {len(deleted_dirs)}")
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    elif confirm_no:
        st.session_state.confirmation = False
        st.info("Deletion process terminated by user.")

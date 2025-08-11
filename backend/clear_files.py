import os

def delete_all_files_in_folder(folder_path):
    if not os.path.exists(folder_path):
        return [], [f"Folder does not exist: {folder_path}"]

    deleted_files = []
    errors = []

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            try:
                os.remove(file_path)
                deleted_files.append(filename)
            except Exception as e:
                errors.append(f"Error deleting {filename}: {str(e)}")

    return deleted_files, errors

def clear_all_uploads():
    folders = [
        "./uploads/candidate/cv/",
        "./uploads/candidate/jd/",
        "./uploads/hr/cv/",
        "./uploads/hr/jd/"
    ]

    all_deleted = []
    all_errors = []

    for folder in folders:
        deleted, errors = delete_all_files_in_folder(folder)
        all_deleted.extend(deleted)
        all_errors.extend(errors)

    return {"deleted_files": all_deleted, "errors": all_errors}

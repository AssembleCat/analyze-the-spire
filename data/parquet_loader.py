import os


def get_file_paths(root_path='default', reverse=False):
    """
    Get all .parquet file paths in the root folder, sorted by year, month, and file name.

    Args:
        root_path (str): The root directory containing the files.

    Returns:
        list: A list of sorted .parquet file paths.
        :param root_path: root folder path
        :param reverse: default is False, but if True is given, the most recent data is returned.
    """
    if root_path == 'default':
        root_path = 'C:/Users/groov/AnalyzeTheSpire/CompressedData'

    file_paths = []
    for year in sorted(os.listdir(root_path), reverse=reverse):
        year_path = os.path.join(root_path, year)
        if os.path.isdir(year_path):
            for month in sorted(os.listdir(year_path), reverse=reverse):
                month_path = os.path.join(year_path, month)
                if os.path.isdir(month_path):
                    for file in sorted(os.listdir(month_path), reverse=reverse):
                        if file.endswith('.parquet'):
                            file_paths.append(os.path.join(month_path, file))
    return file_paths


if __name__ == "__main__":
    root_folder_path = input("Enter the root folder path: ").strip()
    
    if os.path.exists(root_folder_path):
        parquet_paths = get_file_paths(root_folder_path)
        print(f"Found .parquet files: {len(parquet_paths)} count")
        for path in parquet_paths:
            print(path)
    else:
        print("Invalid root folder path. Check and try again.")

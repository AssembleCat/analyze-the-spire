
def get_character_list():
    return ['ironclad', 'silent', 'defect', 'watcher']

def get_character_type(value):
    match value:
        case "ironclad" | "IRONCLAD" | "THE_IRONCLAD":
            return "ironclad"
        case "silent" | "SILENT" | "THE_SILENT":
            return "silent"
        case "defect" | "DEFECT" | "THE_DEFECT":
            return "defect"
        case "watcher" | "WATCHER" | "THE_WATCHER":
            return "watcher"

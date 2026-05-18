def run_save_note(print_line_func, start_y, filename, text_to_save):
    current_y = start_y
    if not text_to_save.strip():
        print_line_func("ABORTED: BUFFER EMPTY", current_y)
        return current_y
    
    if not filename.endswith(".txt"):
        filename += ".txt"
        
    try:
        with open(filename, "a") as f:
            f.write(text_to_save + "\n")
        print_line_func(f"SAVED TO {filename.upper()}", current_y)
    except:
        print_line_func("FS WRITE ERROR", current_y)
    return current_y

def run_read_notes(print_line_func, start_y, filename):
    current_y = start_y
    
    if not filename.endswith(".txt"):
        filename += ".txt"
        
    print_line_func(f"READING {filename.upper()}:", current_y)
    try:
        with open(filename, "r") as f:
            lines = f.readlines()
        if not lines:
            current_y += 15
            print_line_func("NO RECORDS FOUND", current_y)
            return current_y
        for line in lines[-4:]:
            current_y += 15
            print_line_func(line.strip(), current_y)
    except:
        current_y += 15
        print_line_func("FILE NOT FOUND", current_y)
    return current_y
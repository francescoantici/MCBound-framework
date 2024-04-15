def write_log(fp:str, text:str=None):
    # Write to file or print
    if text:
        with open(fp, "a") as f:
            f.write(text)
    else:
        print(text)
    
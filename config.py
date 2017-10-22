def read_config():
    config = dict()
    with open('_config.txt', 'r') as f:
        for line in f:
            if line[0] != '#':
                (key, sep, val) = line.partition('=')
                # if the line does not contain '=', it is invalid and hence ignored
                if len(sep) != 0:
                    val = val.strip()
                    config[key.strip()] = int(val) if str.isdecimal(val) else val
                print(config)
    with open('_config.csv', 'r') as f:
        for line in f:
            if line[0] != '#':
                (key, sep, val) = line.partition('=')
                # if the line does not contain '=', it is invalid and hence ignored
                if len(sep) != 0:
                    val = val.strip()
                    config[key.strip()] = int(val) if str.isdecimal(val) else val
    print(config)

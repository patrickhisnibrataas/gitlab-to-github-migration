import configparser

# Read config file
configuration = configparser.ConfigParser()
configuration.read('config.ini')

# Check if config is valid
if configuration.has_section('gitlab') is False:
    raise Exception('Section gitlab not found')
if configuration.has_option('gitlab', 'token') is False:
    raise Exception('Key token in section gitlab not found')
if configuration.has_option('gitlab', 'user') is False:
    raise Exception('Key user in section gitlab not found')
if configuration.has_option('gitlab', 'email') is False:
    raise Exception('Key email in section gitlab not found')

if configuration.has_section('github') is False:
    raise Exception('Section github not found')
if configuration.has_option('github', 'token') is False:
    raise Exception('Key token in section github not found')
if configuration.has_option('github', 'user') is False:
    raise Exception('Key user in section github not found')
if configuration.has_option('github', 'email') is False:
    raise Exception('Key email in section github not found')
if configuration.has_option('github', 'name') is False:
    raise Exception('Key name in section github not found')

def config_value(section, key):
    if configuration.has_section(section) is False:
        raise Exception(f'Section {section} not found')

    if configuration.has_option(section, key) is False:
        raise Exception(f'Key {key} in section {section} not found')

    return configuration[section][key]
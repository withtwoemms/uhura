import yaml

from collections import OrderedDict


### UTILITY METHODS #######################################
def load_yaml(yaml_path='config.yml'):
    '''
    A helper function that returns a dict of a yaml file
    '''
    with open(yaml_path) as stream:
        return ordered_load(stream)

def ordered_load(stream, Loader=yaml.Loader, object_pairs_hook=OrderedDict):
    class OrderedLoader(Loader):
        pass
    def construct_mapping(loader, node):
        loader.flatten_mapping(node)
        return object_pairs_hook(loader.construct_pairs(node))
    OrderedLoader.add_constructor(
        yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
        construct_mapping)
    return yaml.load(stream, OrderedLoader)

def retry(function, args, retries=0, limit=2):
    if retries < limit: return
    try:
        function(args[0], args[1], arg[2])
    except:
        retries += 1
        retry(function, args, retries)
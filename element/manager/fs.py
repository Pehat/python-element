import os

class FsManager(object):
    """
    This class handle loading of definition from the Filesystem
    """
    def __init__(self, path, manager):
        self.path = path
        self.loader = manager

    def retrieve(self, id):
        return self.loader.load("%s/%s" % (self.path, self.get_id(id)))

    def exists(self, id):
        return os.path.isfile("%s/%s" % (self.path, self.get_id(id)))

    def get_id(self, id):
        if os.path.isfile("%s/%s" % (self.path, id)):
            return id

        return "%s.yml" % id
        
    def find(self, type=None, types=None, tag=None, tags=None, category=None, path=None):
        """
        Of course this is not optimized at all

            supported options:
                - path: the path to look up
                - type: the node type

        """
        options = options = {}

        lookup_path = self.path
        if path:
            lookup_path = "%s/%s" % (self.path, path)

        lookup_types = types or []
        if type:
            lookup_types.append(type)

        lookup_tags = tags or []
        if tag:
            lookup_tags.append(tag)

        nodes = []
        for (path, dirs, files) in os.walk(lookup_path):
            for file in files:
                filename = os.path.realpath("%s/%s" % (path, file))

                if filename[0:len(self.path)] != self.path:
                    # security issue, try to access path outside the self.path
                    continue

                node = self.loader.load(filename)

                if not node:
                    continue

                node['id'] = filename[(len(self.path)+1):] # no starting slash

                if node['id'][-4:] == '.yml':
                    node['id'] = node['id'][:-4]

                if 'type' not in node or (len(lookup_types) > 0 and node['type'] not in lookup_types):
                    continue

                if len(lookup_tags) > 0 and 'tags' not in node:
                    continue

                if 'tags' in node and len(lookup_tags) > 0:
                    for tag in lookup_tags:
                        if tag not in node['tags']:
                            continue

                if category and 'category' not in node and category != node['category']:
                    continue

                nodes.append(node)

        return nodes

    def find_one(self, options=None, selector=None, **kwargs):
        return find(**kwargs)[0]

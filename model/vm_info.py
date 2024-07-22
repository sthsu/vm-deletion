class VMInfo:
    def __init__(self, resource_group_name: str, name: str):
        self.resource_group_name = resource_group_name
        self.name = name

    def as_dict(self):
        return {
            'name': self.name,
            'resource_group_name': self.resource_group_name
        }
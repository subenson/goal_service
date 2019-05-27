class RelatedEntityNotFoundException(Exception):
    def __init__(self):
        super().__init__("related_entity_not_found")

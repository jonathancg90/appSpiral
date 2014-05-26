class InsertHelperMixin(object):
    """
    Mixin for provide initial data to the given entity.
    """
    entity = None
    requirements = {
        # model name: 'verbose name'
    }
    #TODO would be cool to have something like passing to the objects_to_insert
    #TODO a dictionary where the key is the name of the Many 2 Many field
    #TODO and the value is an array of objects that follow the relation.
    objects_to_insert = []
    validate_table_content = True

    def __init__(self):
        pass

    def pass_requirements(self):
        if self.requirements is None: return True
        return True  # TODO verify the requirements before inserting data.

    def insert_data(self):
        if self.entity is None:
            message = "## Provide valid entity class name please ##"
            print message
            return message
        if not self.pass_requirements():
            requirements = self.requirements
            message = "You need to insert the data of the following " +\
                  "entities: %s" % requirements.values()

            return message

        if not self.table_is_empty():
            message = "%s table already contains data." % self.entity.__name__
            return message

        if self.pass_requirements() and self.insert_objects():
            message = "%s data was successfully inserted." % self.entity.__name__
        else:
            message = "Some error had occurred."

        return message

    def table_is_empty(self):
        if not self.validate_table_content: return True
        count = self.entity.objects.all().count()
        return False if count else True

    def insert_objects(self):
        try:
            for obj_to_insert in self.objects_to_insert:
                self.entity.objects.create(**obj_to_insert)
            return True
        except Exception as e:
            print e
            return False
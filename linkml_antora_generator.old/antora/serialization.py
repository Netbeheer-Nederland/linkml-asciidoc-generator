def write(AntoraComponentVersion) -> None:
    _init_output_dir()
    _create_component_version_descriptor()

    if len(self.schemas) == 1:
        self._create_module(self.schemas[0], name="ROOT")
    else:
        for schema in self.schemas:
            self._create_module(schema)

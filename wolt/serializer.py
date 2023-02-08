from marshmallow import Schema, fields, ValidationError, validates_schema


class EventSerializer(Schema):
    type = fields.Str()
    value = fields.Int(min_value=0, max_value=86399)


class DaySerializer(Schema):
    monday = fields.List(fields.Nested(EventSerializer))
    tuesday = fields.List(fields.Nested(EventSerializer))
    wednesday = fields.List(fields.Nested(EventSerializer))
    thursday = fields.List(fields.Nested(EventSerializer))
    friday = fields.List(fields.Nested(EventSerializer))
    saturday = fields.List(fields.Nested(EventSerializer))
    sunday = fields.List(fields.Nested(EventSerializer))

    class Meta:
        ordered = True

    @validates_schema
    def validate(self, data, **kwargs):
        """
        Check for the following cases:
            1) If there are two consecutive events of the same type --> raise error.
            2) If first and last event types of the week are the same, or
            3)     there is only one event in the whole week --> raise error.
        """
        first_event_type = None
        previous_event_type = None
        for _, events in data.items():
            for event in events:
                if event["type"] == previous_event_type:
                    raise ValidationError(
                        f'Cannot have two consecutive "{event["type"]}" times.'
                    )
                else:
                    previous_event_type = event["type"]

                if first_event_type is None:
                    first_event_type = event["type"]

        if first_event_type == previous_event_type:
            raise ValidationError(
                "You must start and end a week with events of distinct types."
            )
        return data

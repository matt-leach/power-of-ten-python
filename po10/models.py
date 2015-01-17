from schematics import models
from schematics import types


class Athlete(models.Model):
    name = types.StringType()
    coach = types.StringType()
    clubs = types.StringType(serialized_name='Club:')
    gender = types.StringType(serialized_name='Gender:')
    age_group = types.StringType(serialized_name='Age Group:')
    county = types.StringType(serialized_name='County:')
    region = types.StringType(serialized_name='Region:')
    nation = types.StringType(serialized_name='Nation:')
    date_of_birth = types.StringType(serialized_name='Date of Birth:')
    
    def __repr__(self):
        return "< Athlete: %s >" % self.name
    
    
# File: models.py
# Author: Kenneth Tong (ktong22@bu.edu), 4/3/2025
# Description: Model for voters and setting their
# fields via reading a text file

from django.conf import settings
from django.db import models

class Voter(models.Model):
    last_name = models.TextField()
    first_name = models.TextField()
    street_number = models.IntegerField()
    street_name = models.TextField()
    apartment_number = models.TextField()
    zip_code = models.IntegerField()
    date_of_birth = models.DateField()
    date_of_registration = models.DateField()
    party_affiliation = models.CharField(max_length=2)
    precinct_number = models.IntegerField()
    
    # Election participation
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()
    
    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.party_affiliation})"

def load_data():
    Voter.objects.all().delete()

    filename = '/Users/Kenny/Downloads/newton_voters.csv'
    f = open(filename)
    f.readline() # discard headers

    for line in f:
        fields = line.split(',')

        try:
            def str_to_bool(value): # Is this a true boolean or not
                    if isinstance(value, str):
                        return value.strip().upper() == 'TRUE'
                    return bool(value)
            
            voter = Voter(
                last_name=fields[1],
                first_name=fields[2],
                street_number=fields[3],
                street_name=fields[4],
                apartment_number=fields[5],
                zip_code=fields[6],
                date_of_birth=fields[7],
                date_of_registration=fields[8],
                party_affiliation=fields[9],
                precinct_number=fields[10],
                v20state=str_to_bool(fields[11]),
                v21town=str_to_bool(fields[12]),
                v21primary=str_to_bool(fields[13]),
                v22general=str_to_bool(fields[14]),
                v23town=str_to_bool(fields[15]),
                voter_score=fields[16]
            )
            voter.save()
            print(f'Voter Created: {voter}')
        except Exception as e:
           print(f"Error processing: {fields}")
    print(f'Done. Created {len(Voter.objects.all())} Results.')
import os
from pyairtable import Api

class MusicReview:
    def __init__(self):
        self.api = Api(os.environ['AIRTABLE_KEY'])
        self.table = self.api.table('appGwuLCFe7slzXQb', 'tblsPDQYfiTtzyfHM')

    def get_music_ratings(self, sort="ASC", max_records=10):
        if not sort:
            return self.table.all(max_records=max_records)
        elif sort == "ASC":
            rating = ["Rating"]
        elif sort == "DESC":
            rating = ["-Rating"]
        
        table = self.table.all(sort=rating, max_records=max_records)
        return table

    def add_music_rating(self, music_title, music_rating, notes=None):
        fields = {'Book': music_title, 'Rating': music_rating, 'Notes': notes}
        self.table.create(fields=fields)


if __name__ == '__main__':
    br = MusicReview()
    get_music_ratings = br.get_music_ratings(sort="DESC", max_records=1)
    print(get_music_ratings)
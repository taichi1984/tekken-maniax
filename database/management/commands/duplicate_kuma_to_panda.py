from django.core.management.base import BaseCommand
from database.models import Move
from guide.models import Character

class Command(BaseCommand):
    help = '特定のレコードを修正して複製します'

    def handle(self, *args, **kwargs):
        kuma = Character.objects.filter(id=25).get()
        panda = Character.objects.filter(id=27).get()
        records_to_duplicate = Move.objects.filter(character=kuma)
        
        duplicates = []
        for record in records_to_duplicate:
            record.pk = None
            record.character = panda
            duplicates.append(record)

        Move.objects.bulk_create(duplicates)

        self.stdout.write(self.style.SUCCESS('正常に複製されました'))
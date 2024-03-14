from django.core.management.base import BaseCommand
from database.models import Move
from database.models import MoveType
from guide.models import Character

class Command(BaseCommand):
    help = '特定のレコードを修正して複製します'

    def handle(self, *args, **kwargs):
        panda = Character.objects.filter(id=27).get()
        mt_hunting = MoveType.objects.filter(id=92).get()
        mt_sit = MoveType.objects.filter(id=93).get()
        mt_roll = MoveType.objects.filter(id=94).get()
        mtp_hunting = MoveType.objects.filter(id=95).get()
        mtp_sit = MoveType.objects.filter(id=96).get()
        mtp_roll = MoveType.objects.filter(id=97).get()
        

        records = Move.objects.filter(character=panda,move_type=mt_hunting)
        
        for record in records:
            record.move_type = mtp_hunting
            record.save()

        records2 = Move.objects.filter(character=panda,move_type=mt_sit)
        
        for record in records2:
            record.move_type = mtp_sit
            record.save()
        
        records3 = Move.objects.filter(character=panda,move_type=mt_roll)
        for record in records3:
            record.move_type = mtp_roll
            record.save()


        self.stdout.write(self.style.SUCCESS('正常に変更されました'))
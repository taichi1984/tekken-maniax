from django.db import models
from guide.models import Character

# Create your models here.

#
#　キャラクターの状態を表す。Guideからの借り物。characterに関しては全キャラのものは総合とする。
#

class State(models.Model):
    id = models.AutoField(primary_key=True,auto_created=True)
    character = models.ForeignKey(Character, on_delete=models.SET_NULL, default="",null=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ThrowTech(models.Model):
    id = models.AutoField(primary_key=True,auto_created=True)
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class HitLevel(models.Model):
    id = models.AutoField(primary_key=True,auto_created=True)
    name = models.CharField(max_length=10)

    def __str__(self):
        return self.name

class MoveType(models.Model):
    id = models.AutoField(primary_key=True,auto_created=True)
    character = models.ForeignKey(Character, on_delete=models.SET_NULL, default="",null=True)
    name = models.CharField(max_length=50)
    order = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.id) + " : " + self.name

class Move(models.Model):
    id = models.AutoField(primary_key=True,auto_created=True)
    name_jp = models.CharField(max_length=30,default="")
    name_jp_ruby = models.CharField(max_length=100,default="",null=True, blank=True)
    name_en = models.CharField(max_length=100,default="",null=True, blank=True)
    character = models.ForeignKey(Character,on_delete=models.SET_NULL,default="",null=True)
    move_type = models.ForeignKey(MoveType,on_delete=models.SET_NULL,default="",null=True)
    command_jp = models.CharField(max_length=30,default="",null=True, blank=True)
    command_en = models.CharField(max_length=30,default="",null=True, blank=True)
    damage = models.IntegerField(null=True, blank=True)
    guard_damage = models.IntegerField(null=True,blank=True)
    guard_damage_heat = models.IntegerField(null=True,blank=True)
    hit_level = models.ForeignKey(HitLevel,on_delete=models.SET_NULL,default="",null=True)
    frame_startup = models.IntegerField(null=True, blank=True)
    frame_active = models.IntegerField(null=True, blank=True)
    frame_recovery = models.IntegerField(null=True, blank=True)
    frame_block = models.IntegerField(null=True, blank=True)
    frame_hit = models.IntegerField(null=True, blank=True)
    frame_crouch_hit = models.IntegerField(null=True, blank=True)
    frame_counter = models.IntegerField(null=True, blank=True)
    state_player = models.ForeignKey(State,on_delete=models.SET_NULL,default="",related_name="moves_player",null=True, blank=True)
    state_enemy_guard = models.ForeignKey(State,on_delete=models.SET_NULL,default="",related_name="moves_enemy_guard",null=True, blank=True)
    state_enemy_hit = models.ForeignKey(State,on_delete=models.SET_NULL,default="",related_name="moves_enemy_hit",null=True, blank=True)
    state_enemy_counter = models.ForeignKey(State,on_delete=models.SET_NULL,default="",related_name="moves_enemy_counter",null=True, blank=True)
    state_enemy_crouch_hit = models.ForeignKey(State,on_delete=models.SET_NULL,default="",related_name="moves_enemy_crouch_hit",null=True, blank=True)
    state_enemy_air = models.ForeignKey(State,on_delete=models.SET_NULL,default="",related_name="moves_enemy_air",null=True, blank=True)
    crouch_status = models.BooleanField(default=False)
    crouch_status_startup = models.IntegerField(null=True, blank=True)
    jump_status = models.BooleanField(default=False)
    jump_status_startup = models.IntegerField(null=True, blank=True)
    power_crash = models.BooleanField(default=False)
    power_crash_startup = models.IntegerField(null=True, blank=True)
    tornado = models.BooleanField(default=False)
    homing = models.BooleanField(default=False)
    heat_engager = models.BooleanField(default=False)
    diminish = models.BooleanField(default=False)
    is_throw = models.BooleanField(default=False)
    throw_tech = models.ForeignKey(ThrowTech, on_delete=models.SET_NULL, default="",null=True)
    throw_tech_frame = models.IntegerField(null=True, blank=True)
    state_after_throw_tech_player = models.ForeignKey(State,on_delete=models.SET_NULL,default="",related_name="moves_throw_tech_player",null=True, blank=True)
    state_after_throw_tech_enemy = models.ForeignKey(State,on_delete=models.SET_NULL,default="",related_name="moves_throw_tech_enemy",null=True, blank=True)
    parent_move = models.ForeignKey('self',on_delete=models.SET_NULL,default="",null=True, blank=True)
    is_combo_guard = models.BooleanField(default=False)
    is_combo_hit = models.BooleanField(default=False)
    is_combo_counter = models.BooleanField(default=False)
    is_combo_crouch_hit = models.BooleanField(default=False)
    is_heat_related = models.BooleanField(default=False)
    is_10ren = models.BooleanField(default=False)
    is_rage_related = models.BooleanField(default=False)
    is_crouch_move = models.BooleanField(default=False)
    is_basic_move = models.BooleanField(default=False)
    
    note = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.name_jp
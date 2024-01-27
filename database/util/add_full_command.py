def add_full_command_jp(queryset):
    for query in queryset:
        parent_move = query.parent_move
        full_command_jp = query.command_jp

        while parent_move:
            full_command_jp = f"{parent_move.command_jp} > {full_command_jp}"
            parent_move = parent_move.parent_move
            
        query.full_command_jp = full_command_jp
    
    for query in queryset:
        if query.state_enemy_hit:
            if (query.state_enemy_hit.name == "足側仰向けダウン" 
            or query.state_enemy_hit.name == "足側うつ伏せダウン" 
            or query.state_enemy_hit.name == "頭側うつ伏せダウン" 
            or query.state_enemy_hit.name == "頭側うつ伏せダウン"
            or query.state_enemy_hit.name == "空中"
            or query.state_enemy_hit.name == "空中吹き飛び"
            or query.state_enemy_hit.name == "空中きりもみ"
            or query.state_enemy_hit.name == "空中縦回転"
            or query.state_enemy_hit.name == "叩きつけ"
            or query.state_enemy_hit.name == "空中裏返り"):
                query.frame_hit_es = "Down"
            elif (query.state_enemy_hit.name == "空中浮かせ(通常)"
            or query.state_enemy_hit.name == "空中浮かせ(高)"
            or query.state_enemy_hit.name == "空中浮かせ(低)"
            or query.state_enemy_hit.name == "空中トルネード"
            or query.state_enemy_hit.name == "腹崩れ"):
                query.frame_hit_es = "Combo"
            elif (query.state_enemy_hit.name == "立ち(ガード可能硬直)"
            or query.state_enemy_hit.name == "尻餅"):
                query.frame_hit_es = "Guard"
            else:
                query.frame_hit_es = ""
        
    for query in queryset:
        if query.state_enemy_counter:
            if (query.state_enemy_counter.name == "足側仰向けダウン" 
            or query.state_enemy_counter.name == "足側うつ伏せダウン" 
            or query.state_enemy_counter.name == "頭側うつ伏せダウン" 
            or query.state_enemy_counter.name == "頭側うつ伏せダウン"
            or query.state_enemy_counter.name == "空中"
            or query.state_enemy_counter.name == "空中吹き飛び"
            or query.state_enemy_counter.name == "空中きりもみ"
            or query.state_enemy_counter.name == "空中縦回転"
            or query.state_enemy_counter.name == "叩きつけ"
            or query.state_enemy_counter.name == "空中裏返り"):
                query.frame_counter_es = "Down"
            elif (query.state_enemy_counter.name == "空中浮かせ(通常)"
            or query.state_enemy_counter.name == "空中浮かせ(高)"
            or query.state_enemy_counter.name == "空中浮かせ(低)"
            or query.state_enemy_counter.name == "トルネード"
            or query.state_enemy_counter.name == "腹崩れ"):
                query.frame_counter_es = "Combo"
            elif (query.state_enemy_counter.name == "立ち(ガード可能硬直)"
            or query.state_enemy_counter.name == "尻餅"):
                query.frame_counter_es = "Guard"
            else:
                query.frame_counter_es = ""
        
    return queryset
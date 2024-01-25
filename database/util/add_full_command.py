def add_full_command_jp(queryset):
    for query in queryset:
        parent_move = query.parent_move
        full_command_jp = query.command_jp

        while parent_move:
            full_command_jp = f"{parent_move.command_jp} > {full_command_jp}"
            parent_move = parent_move.parent_move
            
        query.full_command_jp = full_command_jp
        
    return queryset
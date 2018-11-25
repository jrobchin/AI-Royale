def redis_game_key(gid, game_name):
    return "game:{}:{}".format(game_name, gid)
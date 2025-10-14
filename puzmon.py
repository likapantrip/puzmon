# インポート
import random
import re
import itertools

# グローバル変数の宣言
ELEMENT_SYMBOLS = {
    '火': '$',
    '水': '~',
    '風': '@',
    '土': '#',
    '命': '&',
    '無': ' '
}

ELEMENT_COLORS = {
    '火': '41',
    '水': '44',
    '風': '42',
    '土': '43',
    '命': '45',
    '無': '47'
}

GEM_ELEMENT = ['火', '水', '風', '土', '命']
COMMAND = "ABCDEFGHIJKLMN"

# 関数宣言
def main():
    player_name = input('プレイヤー名を入力してください >>')
    if not player_name:
        print('エラー：プレイヤー名を入力してください')
    else:
        print('### Puzzle & Monsters ###')
        # 敵モンスター
        slime = {'name':'スライム', 'hp':100, 'max_hp':100, 'element':'水', 'ap':10, 'dp':1}
        goblin = {'name':'ゴブリン', 'hp':200, 'max_hp':200, 'element':'土', 'ap':20, 'dp':5}
        big_bat = {'name':'オオコウモリ', 'hp':300, 'max_hp':300, 'element':'風', 'ap':30, 'dp':10}
        wolf = {'name':'ウェアウルフ', 'hp':400, 'max_hp':400, 'element':'風', 'ap':40, 'dp':15}
        dragon = {'name':'ドラゴン', 'hp':600, 'max_hp':600, 'element':'火', 'ap':50, 'dp':20}
        enemies =[slime, goblin, big_bat, wolf, dragon]

        #味方モンスター
        suzaku ={'name':'朱雀', 'hp':150, 'max_hp':150, 'element':'火', 'ap':25, 'dp':10}
        seiryu ={'name':'青龍', 'hp':150, 'max_hp':150, 'element':'風', 'ap':15, 'dp':10}
        byakko ={'name':'白虎', 'hp':150, 'max_hp':150, 'element':'土', 'ap':20, 'dp':5}
        genbu ={'name':'玄武', 'hp':150, 'max_hp':150, 'element':'水', 'ap':20, 'dp':15}
        friends =[suzaku, seiryu, byakko, genbu]

        # パーティ
        party = organize_party(player_name, friends)

        # モンスターを5体倒すとクリア
        kill_enemies = go_dungeon(party, enemies)
        if kill_enemies == 5:
            print('### GAME CLEARED!! ###')
        else:
            print('### GAME OVER!! ###')
        print(f'倒したモンスター数={kill_enemies}')

def print_monster_name(monster):
    global ELEMENT_SYMBOLS, ELEMENT_COLORS
    element = monster['element']
    symbol = ELEMENT_SYMBOLS[element]
    color = ELEMENT_COLORS[element]
    monster_name = monster['name']
    print(f'\033[{color}m{symbol}{monster_name}{symbol}\033[0m', end='')

def organize_party(player_name, friends):
    total_hp = sum([f['hp'] for f in friends])
    dp = sum([f['dp'] for f in friends])
    dp_avg = dp / len(friends)
    party = {'player_name': player_name, 'friends': friends,
             'max_hp': total_hp, 'hp': total_hp, 'dp': dp_avg}
    return party

def go_dungeon(party, enemies):
    print(f'{party['player_name']}のパーティ(HP={party['hp']})はダンジョンに到着した')
    show_party(party)
    win_flg = 0

    for enemy in enemies:
        win_flg += do_battle(party, enemy)
        if party['hp'] <= 0:
            print(f'{party['player_name']}はダンジョンから逃げ出しました')
            return win_flg
        else:
            print(f'{party['player_name']}はさらに奥へ進んだ')
            print('=' * 35)

    print(f'{party['player_name']}はダンジョンを制覇した')
    return win_flg

def show_party(party):
    print('')
    print('<パーティ編成>' + '-' * 21)
    for friend in party['friends']:
        print_monster_name(friend)
        print(f' HP= {friend['hp']} 攻撃= {friend['ap']} 防御= {friend['dp']}')
    print('-' * 35)
    print('')

def do_battle(party, enemy):
    print_monster_name(enemy)
    print('が現れた！')
    print('')
    gems = []
    gems = fill_gems(gems)
    
    battle_field = {
        'enemy': enemy,
        'party': party,
        'gems': gems
    }

    while True:
        on_player_turn(battle_field)
        if enemy['hp'] <= 0:
            break
        on_enemy_turn(party, enemy)
        if party['hp'] <= 0:
            print('パーティのHPは0になりました')
            return 0
    
    print_monster_name(enemy)
    print(f'を倒した!')
    return 1

def fill_gems(gems):
    global GEM_ELEMENT
    new_gems = gems[:] #gemsリストの全要素をコピーして新しいリストを作成
    now_gems_len = len(gems)
    required_gems = 14 - now_gems_len
    new_gems += [random.choice(GEM_ELEMENT) for i in range(required_gems)]
    return new_gems

def on_player_turn(battle_field):
    party = battle_field['party']
    gems = battle_field['gems']

    print(f'【{party['player_name']}のターン】(HP= {party['hp']})')
    show_battle_field(battle_field)

    command = input('コマンド入力 >>')
    while not check_valid_command(command):
        print('A~Nの大文字2文字でコマンド入力してください。同じ文字を入力することはできません')
        command = input('コマンド入力 >>')
    
    move_gem(gems, command)
    evaluate_gems(battle_field, command)

def show_battle_field(battle_field):
    enemy = battle_field['enemy']
    party = battle_field['party']

    print('')
    print_monster_name(enemy)
    print('')
    print(f'HP = {enemy['hp']} / {enemy['max_hp']}')
    print('')
    for friend in party['friends']:
        print_monster_name(friend)
        print(' ', end='')
    print('')

    print(f'HP = {party['hp']} / {party['max_hp']}')
    print('')

    print('-' * 28)
    for c in COMMAND:
        print(c, end=" ")
    print('')

    print_gems(battle_field['gems'])
    print('')
    print('-' * 28)

def print_gems(gems):
    gems_with_color_code = [f'\033[{ELEMENT_COLORS[element]}m{ELEMENT_SYMBOLS[element]}\033[0m' for element in gems]
    for gem in gems_with_color_code:
        print(gem, end=' ')

def check_valid_command(command):
    pattern = r'^([A-N])(?!\1)[A-N]$'
    if re.match(pattern, command):
        return True
    else:
        return False

def move_gem(gems, command):
    global COMMAND
    start_index = COMMAND.index(command[0])
    end_index = COMMAND.index(command[1])

    if start_index < end_index:
        direction = 1
        move_count = end_index - start_index
    else:
        direction = -1
        move_count = start_index - end_index

    print_gems(gems)
    print('')

    for i in range(0, move_count):
        swap_gems(gems, start_index+(i*direction), direction)
        print_gems(gems)
        print('')

def swap_gems(gems, designated_gem_idx, direction):
    """
    designated_gem_idx：移動させる宝石
    direction:  右なら１、左なら−１に動かす
    """
    # 隣の宝石をtmpに格納
    tmp = gems[designated_gem_idx + direction]
    # 移動させる宝石を隣に格納
    gems[designated_gem_idx + direction] = gems[designated_gem_idx]
    # 隣の宝石を移動元に格納
    gems[designated_gem_idx] = tmp

def evaluate_gems(battle_field, command):
    gems = battle_field['gems']
    start_idx, end_idx = check_banishable(gems)
    if start_idx is None:
        print('攻撃が失敗しました')
    else:
        banish_gems(battle_field, start_idx, end_idx, command)
        shift_gems(gems, start_idx, end_idx)
        spawn_gems(gems)

def check_banishable(gems):
    result = []
    index = 0
    for key, group in itertools.groupby(gems):
        group_list = list(group)
        length = len(group_list)
        if length >= 3:
            start = index
            end = index + length - 1
            result.append((start, end))
        index += length
    if result:
       return result[0]
    else:
        return None, None

def banish_gems(battle_field, start_idx, end_idx, command):
    gems = battle_field['gems']
    enemy = battle_field['enemy']

    for i in range(start_idx, end_idx+1):
        gems[i] = '無'
    print_gems(gems)
    print('')
    do_attack(enemy, command)

def do_attack(enemy, command):
    damage = hash(command) % 50
    damage = int(random.uniform(damage - 0.1*damage, damage + 0.1*damage))
    print(f'相手に{damage}のダメージを与えた')
    enemy['hp'] -= damage
    if enemy['hp'] <= 0:
        enemy['hp'] = 0

def shift_gems(gems, start_idx, end_idx):
    print_gems(gems)
    print('')
    
    for i in range(start_idx, end_idx+1):
        del gems[start_idx]
        gems.append('無')
        print_gems(gems)
        print('')

def spawn_gems(gems):
    for i in range(14):
        if gems[i] == '無':
            gems[i] = random.choice(GEM_ELEMENT)
    print_gems(gems)
    print('')

def on_enemy_turn(party, enemy):
    print('')
    print(f'【{enemy['name']}のターン】(HP= {enemy['hp']})')
    do_enemy_attack(party)

def do_enemy_attack(party):
    damage = 10
    party['hp'] -= damage
    print(f'{damage}のダメージを受けた')
    print('')
    if party['hp'] < 0:
        party['hp'] = 0

main()
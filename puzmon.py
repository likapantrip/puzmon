# インポート
import random

# グローバル変数の宣言
ELEMENT_SYMBOLS = {
    '火': '$',
    '水': '~',
    '風': '@',
    '土': '#',
    '命': '&',
    '無': '-'
}

ELEMENT_COLORS = {
    '火': 1,
    '水': 6,
    '風': 2,
    '土': 3,
    '命': 5,
    '無': 7
}

GEM_ELEMENT = ['火', '水', '風', '土', '命']
COMMAND = "ABCDEFGHIGKLMN"

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
    print(f'\033[3{color}m{symbol}{monster_name}{symbol}\033[0m', end='')

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
    party, enemy = battle_field['party'], battle_field['enemy']
    print(f'【{party['player_name']}のターン】(HP= {party['hp']})')
    
    show_battle_field(battle_field)
    command = input('コマンド入力 >>')
    do_attack(enemy, command)

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
    gems_with_color_code = [f'\033[3{ELEMENT_COLORS[element]}m{ELEMENT_SYMBOLS[element]}\033[0m' for element in gems]
    for gem in gems_with_color_code:
        print(gem, end=' ')

def do_attack(enemy, command):
    damage = hash(command) % 50
    damage = int(random.uniform(damage - 0.1*damage, damage + 0.1*damage))
    print(f'相手に{damage}のダメージを与えた')
    print('')
    enemy['hp'] -= damage
    if enemy['hp'] <= 0:
        enemy['hp'] = 0

def on_enemy_turn(party, enemy):
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
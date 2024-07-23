import CHaser  # 同じディレクトリに CHaser.py がある前提
import random

def main():
    client = CHaser.Client()  # サーバーと通信するためのインスタンス
    previous_position = None  # 前回の位置を保存する
    move_log = []  # 移動ログ
    value = [] #サーバーからの応答を保存する
    backtrack_limit = 3  # バックトラックの許容回数
    item_move_mode = 0
    block_check = 0

    while True:
        value = client.get_ready()  # サーバーに行動準備が完了したと伝える
        
        if item_move_mode != 0:
            if item_move_mode == 1:
                value = client.walk_up()
                item_move_mode = 0
                #break
            elif item_move_mode == 2:
                value = client.walk_right()
                item_move_mode = 0
                #break
            elif item_move_mode == 3:
                value = client.walk_down()
                item_move_mode = 0
                #break
            elif item_move_mode == 4:
                value = client.walk_left()
                item_move_mode = 0
                #break
            
        elif item_move_mode == 0:
            # 現在の位置の周囲の情報を取得
            surroundings = {
                "up": value[1],
                "right": value[5],
                "down": value[7],
                "left": value[3]
            }

            # マップの端にいるかどうかを確認
            at_edge = {
                "up": surroundings["up"] == 2,
                "right": surroundings["right"] == 2,
                "down": surroundings["down"] == 2,
                "left": surroundings["left"] == 2
            }

            # 敵の位置を探す
            if 1 in surroundings.values():
                # 敵がいる方向に攻撃
                for direction, content in surroundings.items():
                    if content == 1:
                        print("true kill")
                        if direction == "up":
                            value = client.put_up()
                        elif direction == "right":
                            value = client.put_right()
                        elif direction == "down":
                            value = client.put_down()
                        elif direction == "left":
                            value = client.put_left()
                        break
            else:
                # アイテムを探す
                if 3 in surroundings.values() and block_check == 0:
                    # アイテムがある方向に移動
                    print("true item")
                    for direction, content in surroundings.items():
                        if content == 3:
                            if direction == "up" and not at_edge["up"]:
                                value = client.look_up()
                                print(f"look_up response: {value}")  # デバッグ用
                                value = value
                                if value[6] == 2 and value[4] == 2 and value[8] == 2:  # ブロックがある場合
                                    print("block")
                                    block_check = 1
                                    break
                                else:
                                    #value = client.walk_up()
                                    item_move_mode = 1
                                    break
                            elif direction == "right" and not at_edge["right"]:
                                value = client.look_right()
                                print(f"look_right response: {value}")  # デバッグ用
                                if value[0] == 2 and value[4] == 2 and value[6] == 2:  # ブロックがある場合
                                    print("block")
                                    block_check = 1
                                    break
                                else:
                                    #value = client.walk_right()
                                    item_move_mode = 2
                                    break
                            elif direction == "down" and not at_edge["down"]:
                                value = client.look_down()
                                print(f"look_down response: {value}")  # デバッグ用
                                if value[0] == 2 and value[4] == 2 and value[2] == 2:  # ブロックがある場合
                                    print("block")
                                    block_check = 1
                                    break
                                else:
                                    #value = client.walk_down()
                                    item_move_mode = 3
                                    break
                            elif direction == "left" and not at_edge["left"]:
                                value = client.look_left()
                                print(f"look_left response: {value}")  # デバッグ用
                                if value[2] == 2 and value[4] == 2 and value[8] == 2:  # ブロックがある場合
                                    print("block")
                                    block_check = 1
                                    break
                                else:
                                    #value = client.walk_left()
                                    item_move_mode = 4
                                    break
                            """
                            if item_move_mode == 1:
                                value = client.walk_up()
                            elif item_move_mode == 2:
                                value = client.walk_right()
                            elif item_move_mode == 3:
                                value = client.walk_down()
                            elif item_move_mode == 4:
                                value = client.walk_left()
                            """
                    

                                
                        
                else:
                
                    moved = False        
                    if not moved:
                        print("all not move")
                        # 全ての方向に動けない場合、最も安全な方向に動く
                        directions = ["up", "right", "down", "left"]
                        random.shuffle(directions)

                        for direction in directions:
                            if not at_edge[direction]:
                                if direction == "up":
                                    if surroundings["up"] != 2:  # ブロックがない場合のみ移動
                                        value = client.walk_up()
                                        previous_position = "up"
                                        print(f"{direction}に移動しました")
                                        move_log.append(direction)  # 移動ログに追加
                                        block_check = 0
                                        break
                                elif direction == "right":
                                    if surroundings["right"] != 2:
                                        value = client.walk_right()
                                        previous_position = "right"
                                        print(f"{direction}に移動しました")
                                        move_log.append(direction)  # 移動ログに追加
                                        block_check = 0
                                        break
                                elif direction == "down":
                                    if surroundings["down"] != 2:
                                        value = client.walk_down()
                                        previous_position = "down"
                                        print(f"{direction}に移動しました")
                                        move_log.append(direction)  # 移動ログに追加
                                        block_check = 0
                                        break
                                elif direction == "left":
                                    if surroundings["left"] != 2:
                                        value = client.walk_left()
                                        previous_position = "left"
                                        print(f"{direction}に移動しました")
                                        move_log.append(direction)  #
                                        block_check = 0
                                        break
                    

        # 移動ログをファイルに保存
        with open("log.txt", "a") as log_file:
            log_file.write(f"{previous_position}\n")

        print(f"Previous position: {previous_position}")
        print(f"Move log: {move_log}")

if __name__ == "__main__":
    main()

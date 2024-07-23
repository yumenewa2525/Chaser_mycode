import socket
import ipaddress
import os
"""
このコードはゆーせーが元のソースコードを改良したものです

元のソースコード
https://github.com/tomio2480/chaser-python/blob/master/CHaser.py
"""

class Client:
    def __init__(self):
        try:
            print("ポート変更・グローバルIPに接続時⇒手動接続\n一人で実験する・自分がホスト側の場合⇒ローカルホスト接続\n同じネットワーク内の他のPCに接続する場合⇒LAN接続")
            setting = int(input("接続モード選択\n1:手動接続（ポートを変更している場合もこっち）\n2:ローカルホスト接続\n3:LAN接続"))

            if setting == 1:
                print("手動接続が選択されましたぁ！")
                self.port = input("ポート番号を入力してください → ")
                self.name = input("ユーザー名を入力してください → ")[:15]
                self.host = input("サーバーのIPアドレスを入力してください → ")
            elif setting == 2:
                print("ローカルホスト接続が選択されましたぁ！")
                local_mode = int(input("プレイヤーの選択 1:Cool 2:Hot"))
                if local_mode == 1:
                    self.port = "2009"
                    self.name = input("ユーザー名を入力してください → ")[:15]
                    self.host = "127.0.0.1"
                elif local_mode == 2:
                    self.port = "2010"
                    self.name = input("ユーザー名を入力してください → ")[:15]
                    self.host = "127.0.0.1"
            elif setting == 3:
                print("LAN接続が選択されましたぁ！")
                local_mode = int(input("プレイヤーの選択 1:Cool 2:Hot"))
                print("サーバーのIPアドレスはプライベートIPを入力してください!\nグローバルIPは手動接続から接続することを推奨します!\n")
                if local_mode == 1:
                    self.port = "2009"
                    self.name = input("ユーザー名を入力してください → ")[:15]
                    self.host = input("サーバーのIPアドレスを入力してください → ")
                elif local_mode == 2:
                    self.port = "2010"
                    self.name = input("ユーザー名を入力してください → ")[:15]
                    self.host = input("サーバーのIPアドレスを入力してください → ")
            else:
                raise ValueError("無効な接続モードが選択されました")

            if not self.__ip_judge(self.host):
                os._exit(1)

            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect((self.host, int(self.port)))

            print("port:", self.port)
            print("name:", self.name)
            print("host:", self.host)

            self.__str_send(self.name + "\n")

        except Exception as e:
            print("エラーが発生しました: ", e)
            os._exit(1)

    def __ip_judge(self, ip):
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            print("無効なIPアドレスです")
            return False

    def __str_send(self, string):
        self.client.sendall(string.encode('utf-8'))

    def __order(self, order_str, gr_flag=False):
        try:
            # もしgr_flagがTrueの場合、サーバーからの応答を受け取り、接続が完了したかどうかを確認する
            if gr_flag:
                response = self.client.recv(4096)

                if b'@' in response:
                    pass  # Connection completed.
                else:
                    print("Connection failed.")

            # 指定された命令をサーバーに送信
            self.__str_send(order_str + "\r\n")

            # サーバーからの応答を受け取る
            response = self.client.recv(4096)[0:11].decode("utf-8")

            # gr_flagがFalseの場合、特定の文字列をサーバーに送信
            if not gr_flag:
                self.__str_send("#\r\n")

            # 応答の最初の文字に応じて処理を行う
            print(f"response: {response}")
            if response[0] == '1':
                return [int(x) for x in response[1:10]]
            elif response[0] == '0':
                raise OSError("Game Set!")
            else:
                print("response[0] = {0} : Response error.".format(response[0]))
                raise OSError("Response Error")

        except OSError as e:
            print(e)
            self.client.close()
            os._exit(0)

    def get_ready(self):
        return self.__order("gr", True)

    def walk_right(self):
        return self.__order("wr")

    def walk_up(self):
        return self.__order("wu")

    def walk_left(self):
        return self.__order("wl")

    def walk_down(self):
        return self.__order("wd")

    def look_right(self):
        return self.__order("lr")

    def look_up(self):
        return self.__order("lu")

    def look_left(self):
        return self.__order("ll")

    def look_down(self):
        return self.__order("ld")

    def search_right(self):
        return self.__order("sr")

    def search_up(self):
        return self.__order("su")

    def search_left(self):
        return self.__order("sl")

    def search_down(self):
        return self.__order("sd")

    def put_right(self):
        return self.__order("pr")

    def put_up(self):
        return self.__order("pu")

    def put_left(self):
        return self.__order("pl")

    def put_down(self):
        return self.__order("pd")
    
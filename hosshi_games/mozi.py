import pyxel as px
import PyxelUniversalFont as puf
import sys

# --- TextAnimator クラス ---
class TextAnimator:
    def __init__(self, writer, x, y, font_size, color):
        """
        TextAnimatorの初期化
        :param writer: PyxelUniversalFont.Writerのインスタンス
        :param x: 表示開始X座標
        :param y: 表示開始Y座標
        :param font_size: フォントサイズ
        :param color: 文字色 (Pyxelのパレットカラーインデックス)
        """
        self.writer = writer
        self.x = x
        self.y = y
        self.font_size = font_size
        self.color = color
        
        self.text_to_display = ""
        self.display_char_count = 0
        self.char_display_speed = 3  # 何フレームごとに1文字表示するか (値が小さいほど速い)
        self.is_finished = False     # 全ての文字が表示されたかどうかのフラグ

    def set_text(self, text, speed=3):
        """
        表示するテキストを設定します。
        新しいテキストを設定すると、表示は最初からやり直されます。
        :param text: 表示する文字列
        :param speed: 1文字を表示するのにかかるフレーム数 (デフォルトは3)
        """
        self.text_to_display = text
        self.display_char_count = 0
        self.char_display_speed = speed
        self.is_finished = False

    def update(self):
        """
        アニメーションの状態を更新します。
        ゲームのupdate関数内で呼び出してください。
        """
        if self.is_finished:
            return

        if px.frame_count % self.char_display_speed == 0:
            if self.display_char_count < len(self.text_to_display):
                self.display_char_count += 1
            else:
                self.is_finished = True # 全ての文字が表示された

        # スペースキーが押されたら文字をすべて表示する（スキップ機能）
        if px.btnp(px.KEY_SPACE):
            self.display_char_count = len(self.text_to_display)
            self.is_finished = True

    def draw(self):
        """
        現在のテキストを描画します。
        ゲームのdraw関数内で呼び出してください。
        """
        if not self.text_to_display: # 表示するテキストが設定されていなければ何もしない
            return

        current_text = self.text_to_display[:self.display_char_count]
        self.writer.draw(self.x, self.y, current_text, self.font_size, self.color)

    def is_animation_finished(self):
        """
        全てのアニメーションが完了したかどうかを返します。
        """
        return self.is_finished

# --- アプリケーション本体 ---
class App:
    def __init__(self):
        px.init(500, 200)
        self.writer = puf.Writer("misaki_gothic.ttf")

        # TextAnimatorのインスタンスを作成
        # 引数: writer, X座標, Y座標, フォントサイズ, 文字色
        self.animator = TextAnimator(self.writer, 25, 4, 10, 7)
        
        # 最初のテキストを設定
        self.animator.set_text("こんにちは。私はホッシーです。これはPyxelでRPG風に文字を流すテストです。")
        
        self.current_message_index = 0
        self.messages = [
            "こんにちは。私はホッシーです。これはPyxelでRPG風に文字を流すテストです。",
            "このメッセージが表示し終わったら、次のメッセージに切り替わります。",
            "スペースキーを押すと、一瞬で全文が表示されますよ！",
            "これで、あなたのゲームでも簡単に流れる文字が実現できますね！"
        ]

        px.run(self.update, self.draw)
    
    def update(self):
        # TextAnimatorの更新処理を呼び出す
        self.animator.update()

        # アニメーションが終了したら次のメッセージを表示
        if self.animator.is_animation_finished() and px.btnp(px.KEY_RETURN): # Enterキーで次のメッセージへ
            self.current_message_index += 1
            if self.current_message_index < len(self.messages):
                self.animator.set_text(self.messages[self.current_message_index])
            else:
                # 全てのメッセージが表示し終わったら、最初のメッセージに戻るなど、ループ処理を記述
                self.current_message_index = 0
                self.animator.set_text(self.messages[self.current_message_index])


    def draw(self):
        px.cls(0)
        # TextAnimatorの描画処理を呼び出す
        self.animator.draw()
        
        # メッセージがすべて表示されたら指示を出す
        if self.animator.is_animation_finished():
            self.writer.draw(25, 100, "メッセージの表示が完了しました。Enterキーで次へ進めます。", 10, 13)


if __name__ == "__main__":
    print("起動します")
    app = App()
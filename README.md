## ✅Chill Cue
ユーザーがタスクを管理し、達成後にYouTube動画をご褒美として視聴できる習慣化支援アプリです。

<img width="1920" height="1080" alt="Image" src="https://github.com/user-attachments/assets/86795003-0a19-4223-af6a-df884b801131" />

## 🌐アプリURL
https://todo-app-862v.onrender.com

## 📔このアプリについて
### アプリを作った背景
学習や開発に取り組む中で、作業の合間についSNSや動画アプリを長時間見てしまうことがありました。
ちょっとした休憩のつもりが、気づけばかなりの時間が経っている・・・。
そんな経験が多くの人にもあるのではないかと思います。
そこで、休憩時に癒しやちょっとした刺激が得られて、なおかつ気分をすばやく切り替えられる仕組みがあったら、だらだらと休憩せずに済むのでは？と考え、このアプリを開発しました。

### ユーザーが抱える課題
- 休憩中、ついSNSや動画アプリに没頭してしまう。
- タスクをやりきるためのモチベーションが湧かない。
- 作業を終えた後の癒しが欲しい。

### 解決方法
タスク管理ができ、タスク達成後に短い動画を一つ見られるアプリケーション。

### 望む未来
- タスク完了時に短時間の楽しみを用意することで、次の行動にスムーズに移れるようになる。
- 楽しみを伴うタスク管理によって、努力の習慣化がストレスなく実現できるようになる。

## 🐈機能一覧
| ログイン・新規登録 | タスク管理機能 |
|---|---|
|<img width="906" height="906" alt="Image" src="https://github.com/user-attachments/assets/21f75c60-f333-42ca-b7d2-43764bccb6ab" />|<img width="906" height="906" alt="Image" src="https://github.com/user-attachments/assets/a2bef016-3ff8-4a2b-94fd-a4c77d546789" />|
| ログインIDとパスワードでの認証機能を実装しました。 | タスクを管理できる機能を実装しました。追加、削除、並び替えができます。 |

| 動画へのリンク表示 | 動画のカテゴリ選択 |
|---|---|
|<img width="906" height="906" alt="Image" src="https://github.com/user-attachments/assets/dfe06f2b-64be-4b19-b2c7-b23ef185c5ef" />|<img width="906" height="906" alt="Image" src="https://github.com/user-attachments/assets/2799e695-dae0-4bc4-8a07-774ce53629ba" />|
| タスク完了時、動画へのリンクが出てきます。 | 観たい動画のカテゴリを選択できます。 |

| 動画へのリンク表示 | 管理画面 |
|---|---|
|<img width="906" height="906" alt="Image" src="https://github.com/user-attachments/assets/60700dea-a34c-4a6e-89ab-bdf010f4b15e" />|<img width="906" height="906" alt="Image" src="https://github.com/user-attachments/assets/972563c1-23ad-4958-8ab9-7410e07a8861" />|
| 選ばれたカテゴリから動画をランダムで表示します。 | 管理者権限を持つユーザーが動画を管理できる機能を実装しました。 |

## 🛠️使用技術
### バッグエンド
- Python
- Flask (軽量なWebフレームワーク)
- SQLAlchemy (ORM)
### フロントエンド
- HTML/CSS/JavaScript
- Jinja2 (Flask用テンプレートエンジン)
- Bootstrap5 (レスポンシブ対応UIライブラリ)
### 外部API
- YouTube Data API v3 (動画検索に使用)
### データベース
- PostgreSQL
### コード解析
- ESLint (JavaScriptのコード品質チェック)
- Pylint (Pythonのコード品質チェック)
- pytest (テストツール)
### デプロイ先
- Render

## 📋ER図
<p align="center">
<img width="860" height="550" alt="Image" src="https://github.com/user-attachments/assets/10a3bd42-5274-4f24-a371-92b9e6be0215" />


## 📄DFD
<p align="center">
  <a href="[画像へのリンク](https://github.com/user-attachments/assets/54b22bdf-2d85-491b-91b4-978c3ba4552d)">
    <img width="611" height="552" alt="Image" src="https://github.com/user-attachments/assets/54b22bdf-2d85-491b-91b4-978c3ba4552d" />
  </a>
</p>

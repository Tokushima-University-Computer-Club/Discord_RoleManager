# 概要
ロールの付与、剝奪を管理するためのbotです。
## 主な機能
- ロールの付与
- ロールの剥奪
- ロールの自動付与

# ユーザーガイド
## コマンド
`/role [option] [user] [role]`
### 引数
- option: optionにはgive/remove/autoのいずれかを選択します。
	- `give`: `user`に`role`を付与します。
	- `remove`: `user`から`role`を剝奪します。
	- `auto`: 新規参加者に`role`を自動で付与するよう設定します。
    
- `user`: 対象となるユーザ。optionでautoを選択した場合は無視されます。
- `role`: 対象となるロール。

# ply2fbx-armature.py
**MagicaVoxel**で**PLY**形式で出力したボクセルのキャラクターにウェイトを設定して、Unityで簡単にアニメーションさせるためのBlender用のスクリプトです。

以下の2通りの方法でウェイト設定をしたキャラクターを作ることができます。

- Blenderのみ利用する方法
  - だいし様の[MagicaVoxelで作ったプリキュアをUnityで動かす](https://github.dev7.jp/b/2015/12/15/precureadv20151213/)の記事で配布されているアーマチュアと素材を使って、ウェイト設定をして、FBXとPNGファイルをエクスポート
- Blenderとmixamoを利用
  - BlenderでエクスポートしたテクスチャーとFBXファイルをZIP圧縮して、[mixamo](https://www.mixamo.com/)にアップロードしてウェイト設定とアニメーション付けをする

# インストール
**Blender 2.79b**にインストールする手順です。Blenderはインストール済みとします。

- Blenderが起動していたら閉じておきます
- Blenderのインストールフォルダーを開いて、`scripts/startup`フォルダーを開きます
  - Windowsの場合、デフォルトのインストーす先は`C:\Program Files\Blender Foundation\Blender\2.79\`です



- プログラムの[ダウンロード](https://github.com/am1tanaka/ply2fbx/releases/download/v1.0.0/ply2fbx-armature.py)

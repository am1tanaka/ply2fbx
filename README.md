# ply2fbx-armature.py
**MagicaVoxel**で**PLY**形式で出力したボクセルのキャラクターにウェイトを設定して、Unityで簡単にアニメーションさせるためのBlender用のスクリプトです。

2通りの方法で、ウェイト設定をしたキャラクターを作ることができます。

- Blenderのみ利用する方法
  - だいし様の[MagicaVoxelで作ったプリキュアをUnityで動かす](https://github.dev7.jp/b/2015/12/15/precureadv20151213/)の記事で配布されているアーマチュアと素材を使って、ウェイト設定をして、FBXとPNGファイルをエクスポート
- Blenderとmixamoを利用
  - BlenderでエクスポートしたテクスチャーとFBXファイルをZIP圧縮して、[mixamo](https://www.mixamo.com/)にアップロードしてウェイト設定とアニメーション付けをする

# インストール
**Blender 2.79b**にインストールする手順です。Blenderはインストール済みとします。

- Blenderが起動していたら閉じておきます
- Blenderのインストールフォルダーを開いて、`scripts/startup`フォルダーを開きます
  - Windowsの場合、デフォルトのインストーす先は`C:\Program Files\Blender Foundation\Blender\2.79\`です

![open startup folder](doc-images/img00.png)
- [こちら](https://github.com/am1tanaka/ply2fbx/releases/download/v1.0.1/ply2fbx-armature.py)からダウンロードした`ply2fbx-armature.py`を、`startup`フォルダーにコピーします(管理者権限が必要かも知れません)

![copy py file](doc-images/img01.png)

以上でインストール完了です。Blenderを起動すると、スクリプトが機能します。Miscタブが追加されて、3つのボタン(Import PLY, Auto Weight, Export FBX and Texture)が確認できればOKです。

![show ply tool](doc-images/img02.png)

> Add-onにするものかもですが、詳しくないのでとりあえず手っ取り早くStartupで起動することにしました。タブ名もデフォルトっぽい*Misc*のまま。気になるようでしたらMITライセンスですのでご自由に修正ください。プルリク歓迎！

# BlenderのみでヒューマノイドモデルのFBXとPNGを生成
だいし様の[MagicaVoxelで作ったプリキュアをUnityで動かす](https://github.dev7.jp/b/2015/12/15/precureadv20151213/)の記事から、**MagicaVoxel用素体**(`base.vox`)と**素体用アーマチュア**(`BaseArmature.blend`)をダウンロードしてください

![Download base](doc-images/img03.png)

## MagicaVoxelでキャラクター作り
- [MagicaVoxel](https://ephtracy.github.io/)を起動して、base.voxを読み込みます
- 記事に従ってキャラクターを作成します(手順を確認する場合はbase.voxのままで構いません)
- *Export* -> *ply*をクリックします

![Export PLY](doc-images/img04.png)

- 分かりやすい場所に任意のファイル名で保存します。ファイル名は半角英数のみ推奨(Unityで色々起きる可能性があるので)

![Export Dialog](doc-images/img05.png)

以上でキャラクター完成です。

## アーマチュアとPLYの読み込み
ここからBlenderでの作業になります。必要なファイルを読み込みます。

- Blenderが起動していなければ起動します
- ダウンロードしてあった`BaseArmature.blend`をBlenderにドラッグ＆ドロップします

![Load Armature](doc-images/img06.png)

- 3D Viewの左のメニューから*Misc*タブをクリックします

![Click Misc](doc-images/img07.png)

- *Import PLY*ボタンをクリックします

![Click Import PLY](doc-images/img08.png)

- PLYファイルのフォルダーを設定して、読み込むファイルを選択して、*Import PLY*ボタンをクリックします

![Import](doc-images/img09.png)

> デフォルトのPLYのサイズだと大きくなりすぎるので、アーマチュアとサイズが丁度良くなるようにサイズを0.22倍するようにしています。倍率は左下の*Scale*欄で設定できるので、読み込みと同時にサイズを調整したい場合は、値を変更してから*Import PLY*をクリックしてください。

PLYファイルのインポートが完了しました。

![Import done](doc-images/img10.png)

デフォルトのアーマチュアとbase.voxを使っていれば、最初から大きさと位置がぴったりと合います。

もし、大きさや位置がずれている場合は、この段階で調整してから次に進んでください。

## ウェイト設定
Blenderでウェイトを設定する場合は、メッシュとアーマチュアを階層して親子設定をするのですが、それらは*Auto Weight*ボタンを押せば完了です。

![Auto Weight](doc-images/img11.png)

以下のように、*Outliner*で*armature*の子供にメッシュが設定されていれば成功です。

![Result](doc-images/img12.png)

## エクスポート
PLYはテクスチャーを持たないので、Unityで色を付けるにはテクスチャーをベイクする必要があります。また、マテリアルの作成も必要です。**面倒なので自動化しました。**

- *Export FBX and Texture*ボタンをクリックします

![Export FBX](doc-images/img13.png)

- エクスポート先とファイル名を設定したら*Export FBX and Texture*ボタンをクリックすれば完了です

![Click Export](doc-images/img14.png)

> デフォルトで生成されるテクスチャーのサイズは512x512ピクセルです。ボクセル数が多いと足りないかも知れないので、Unityで見た時に色がずれているような場合は、*Texture Width*と*Texture Height*を`1024`や`2048`に変更してみてください。
> ボクセル数が少なく、こんなに必要ないという場合は小さい値にしてください。不具合を避けるため、テクスチャーのサイズは2の累乗にしてください(よく分からない場合はいじらないでください)。

以上で完了です。出力先のフォルダーに、以下のように`fbx`と`png`の2つのファイルが出力されていれば成功です。

![output](doc-images/img15.png)

## Unityに読み込む
Unityに読み込んで動作テストしてみます。以下、前提です。

- Unity2018.1.3で確認(2017以降なら似たような操作でいけると思います)
- Standard Assetsインストール済み

Unityを起動して、確認用のプロジェクト(空のプロジェクトでよいです)を開きます。

- *Assets*メニューから*Import Package* -> *Characters*を選択して、*Import*します

![Import Assets](doc-images/img20.png)

- エクスポートした`.fbx`と`.png`を[Ctrl]キーを押しながら選択して、まとめてUnityのProjectビューにドロップします

![Import Models](doc-images/img21.png)

**注意！！ FBXとPNGファイルを同時にドラッグ＆ドロップしないとテクスチャーが貼られないので気を付けてください！！**

- Projectビューで読み込んだPNGを選択して、以下を設定します
  - *Generate Mip Map*のチェックを外す
    - 小さくした時に変な線が出ることがあるので
  - *Wrap Mode*を*Clamp*に設定
    - 画像端のにじみ防止
  - *Filter Mode*を*Point(no filter)に設定
    - にじみ防止
  - 以上できたら、*Apply*ボタンをクリック

![PNG Setting](doc-images/img22.png)

- Projectビューで読み込んだモデルを選択します
- *Model*について、以下を設定します
  - *Import Visibility*, *Import Cameras*, *Import Lights*のチェックを外す
    - くっついてませんが念のため
  - 設定したら*Apply*ボタンをクリック

![Model Setting](doc-images/img23.png)

- *Rig*について、以下を設定します
  - *Animation Type*を*Humanoid*に変更します
  - *Apply*ボタンをクリックします

![Rig Setting](doc-images/img24.png)

これで、*Configure...*の左にチェックが表示されれば成功です。これをやらないと、設定したアーマチュアなどの設定が反映されないので重要な設定です。

マテリアルを取り出します。

- *Materials*について、以下を設定します
  - *Extract Materials...*ボタンをクリックします

![Material Setting](doc-images/img25.png)

- 保存先のフォルダーを選択します。*Materials*フォルダーを作成して、そこを選択するとよいでしょう

![Select Folder](doc-images/img26.png)

キャラクターを作ります。

- *Hierarchy*ビューの*Create*をクリックして、*Craete Empty*で空のゲームオブジェクトを作成します

![Create Empty](doc-images/img27.png)

- 作成したオブジェクト名をキャラクターの名前などにするとよいでしょう(`Player`など)
- *Project*ビューからキャラクターのモデルをドラッグして、*Hierarchy*ビューに作成したゲームオブジェクトにドロップして、子供にします

![Import Model](doc-images/img28.png)

- *Hierarchy*ビューにドロップしたモデルをクリックして選択して、*Inspector*ビューで以下を確認＆設定します
  - *Transform*の*Position*・・・すべて`0`
  - *Rotation*・・・キャラクターを向かせたい方向(奥を向かせるのが一般的)
  - *Scale*・・・良さそうな大きさに調整

![Reset Transform](doc-images/img29.png)

これでモデルが表示されます！

![Chr](doc-images/img30.png)

**注意！！　Rigidbodyをアタッチしたゲームオブジェクトの*Scale*は、必ず`1`にします。そうしないとRigidbodyの動作が破綻します。空のゲームオブジェクトを作って、モデルをその子供にしたのはモデルを調整しやすくするためです**

ただ、少し色が暗いので、マテリアルを調整しておきます。

- *Project*ビューで、保存したマテリアルを選択します

![Select Material](doc-images/img31.png)

- *Inspector*ビューの*Albedo*の右の白い四角をクリックしてカラーパネルを表示したら、色を真っ白にして、*x*で閉じます

![Set Albedo](doc-images/img32.png)

アニメーションを設定して、動かして見ましょう。

- *Hierarchy*ビューからキャラクターモデルを選択しておきます

![Select Chr Model](doc-images/img33.png)

- *Project*ビューで、*Standard Assets* -> *Characters* -> *ThirdPersonCharacter* -> *Animator*の左の三角をクリックして開きます

![Set Animator](doc-images/img34.png)

- *ThirdPersonAnimatorController*をドラッグして、*Inspector*ビューの*Controller*欄にドロップします
- テスト時に動かれると面倒なので、*Apply Root Motion*のチェックを外しておきます

![Clear Root Motion](doc-images/img37.png)

- *Project*ビューで*ThirdPersonAnimatorController*をダブルクリックします

![Double Click Animator](doc-images/img35.png)

- *Animator*ウィンドウが表示されるので、左にある*Parameters*をクリックして、パラメーターを表示します

![Click Parameters](doc-images/img36.png)

以上で準備完了です。Unityを*Play*してください。

*Animator*ウィンドウをクリックしてアクティブにしたら、パラメーターの値をいじってみてください。

![Animation Test](doc-images/img38.png)

走ったり、しゃがんだり、アニメーションすることが確認できれば成功です。

# 参考・関連URL
- [Blender](https://www.blender.org/)
- [MagicaVoxel](https://ephtracy.github.io/)
- [Blender 2.79.0 855d2955c49 - API documentation](https://docs.blender.org/api/2.79/)
- [だいし. MagicaVoxelで作ったプリキュアをUnityで動かす](https://github.dev7.jp/b/2015/12/15/precureadv20151213/)

# BlenderでヒューマノイドモデルのFBXとPNGを生成する
だいし様の[MagicaVoxelで作ったプリキュアをUnityで動かす](https://github.dev7.jp/b/2015/12/15/precureadv20151213/)の記事に掲載されている**MagicaVoxel用素体**(`base.vox`)と**素体用アーマチュア**(`BaseArmature.blend`)を利用して、Blenderで自動ウェイト設定をして、FBXに出力して、Unityでテスト動作させる手順です。

# 準備
[MagicaVoxelで作ったプリキュアをUnityで動かす](https://github.dev7.jp/b/2015/12/15/precureadv20151213/)を開いて、**MagicaVoxel用素体**(`base.vox`)と**素体用アーマチュア**(`BaseArmature.blend`)をダウンロードしてください

![Download base](doc-images/img03.png)

# PLYファイルからウェイト設定したキャラクターモデルとテクスチャーをエクスポート

## MagicaVoxelでキャラクター作り
- [MagicaVoxel](https://ephtracy.github.io/)を起動して、base.voxを読み込みます
- 記事に従ってキャラクターを作成します(手順を確認する場合はbase.voxのままで構いません)
- キャラクターが完成したら、*Export* -> *ply*をクリックします

![Export PLY](doc-images/img04.png)

- 分かりやすい場所に任意のファイル名で保存します。ファイル名は半角英数のみ推奨(日本語や全角が混じったファイル名だとUnityで不具合が起きる可能性があります)

![Export Dialog](doc-images/img05.png)

## アーマチュアとPLYの読み込み
ここからはBlenderでの作業です。必要なファイルを読み込みます。

- Blenderが起動していなければ起動します
- ダウンロードしてあった`BaseArmature.blend`をBlenderにドラッグ＆ドロップするなどして開きます

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

デフォルトのアーマチュアとbase.voxを使っていれば、大きさと位置が合っているはずです。もし、モデルとアーマチュアの配置がずれている場合は、縮小や移動をして上記のように重ねてから次に進んでください。

## ウェイト設定
Blenderでウェイトを設定する場合は、メッシュとアーマチュアを階層して親子設定をするのですが、それらを*Auto Weight*ボタンで自動化しました。

![Auto Weight](doc-images/img11.png)

以下のように、*Outliner*で*armature*の子供にメッシュが設定されていれば成功です。

![Result](doc-images/img12.png)

## エクスポート
PLYはテクスチャーを持たないので、Unityで色を付けるにはテクスチャーをベイクする必要があります。また、マテリアルの作成も必要です。そそれらの作業を自動的に実行します。

- *Export FBX and Texture*ボタンをクリックします

![Export FBX](doc-images/img13.png)

- エクスポート先とファイル名を設定したら*Export FBX and Texture*ボタンをクリックすれば完了です

![Click Export](doc-images/img14.png)

> デフォルトで生成されるテクスチャーのサイズは512x512ピクセルです。ボクセル数が多いと足りないかも知れないので、Unityで見た時に色がずれているような場合は、*Texture Width*と*Texture Height*を`1024`や`2048`に変更してみてください。

> ボクセル数が少なくて、もっと小さいテクスチャーで構わない場合は`128`や`256`にしてみてください。テクスチャーのサイズは2のテクスチャーのサイズは2の累乗である必要があります。よく分からない場合は、この設定はいじらないでください。

以上で完了です。出力先のフォルダーに、以下のように`fbx`と`png`の2つのファイルが出力されていれば成功です。

![output](doc-images/img15.png)

# Unityで動作確認する
作成したモデルをUnityに読み込んで動かしてみましょう。以下、前提です。

- Unity2018.1.3で確認(2017以降なら似たような操作でいけると思います)
- Standard Assetsインストール済み

## テスト用シーンを作成する
Unityを起動して、確認用のプロジェクト(空のプロジェクトでよいです)を開きます。

- *Assets*メニューから*Import Package* -> *Characters*を選択して、*Import*します

![Import Assets](doc-images/uni/img00.png)

- 地面用のPlaneを作成します。*Hierarchy*ビューの*Create*をクリックして、*3D Object* -> *Plane*を選択します

![Set Plane](doc-images/uni/img01.png)

- *Hierarchy*ビューで作成した*Plane*をクリックして選択します
- *Inspector*ビューで、*Transform*の右の歯車アイコンをクイックして、*Reset*を選択して、場所を原点にしておきます

![Set Zero](doc-images/uni/img03.png)

- *Plane*にマテリアルを設定して色を着けたり、*Main Camera*の位置を調整して、*Game*ビューでそれっぽく見えるようにします

![Sample Plane](doc-images/uni/img04.png)

- *Project*ビューで、*Standard Assets* -> *Characters* -> *ThirdPersonCharacter* -> *Prefabs*の左の三角アイコンをクリックして開きます

![Set TPC](doc-images/uni/img05.png)

- *ThirdPersonController*プレハブをドラッグして、*Scene*ビューで良さそうな場所に配置します

テスト用のシーンができました。*Play*して、矢印キーや[A][S][D][W]キーでキャラクターを操作できます。

## 作成したキャラクターを設定
エクスポートしたキャラクターを読み込み、設定します。

- Blenderでエクスポートした`FBX`と`PNG`を[Ctrl]キーを押しながら選択して、まとめてUnityの*Project*ビューにドロップします

![Import Models](doc-images/uni/img02.png)

**注意！！ FBXとPNGファイルを同時にドラッグ＆ドロップしないとテクスチャーが貼られないので気を付けてください！！**

- *Project*ビューで、読み込んだPNGを選択して以下を設定します
  - *Generate Mip Map*のチェックを外す
    - 小さくした時に変な線が出ることがあるので
  - *Wrap Mode*を*Clamp*に設定
    - 画像端のにじみ防止
  - *Filter Mode*を*Point(no filter)に設定
    - にじみ防止
  - 以上できたら、*Apply*ボタンをクリック

![PNG Setting](doc-images/uni/img06.png)

- Projectビューで、読み込んだモデルをクリックして選択します

![Select Model](doc-images/uni/img07.png)

- *Model*について、以下を設定します
  - *Import Visibility*, *Import Cameras*, *Import Lights*のチェックを外す
    - くっついてませんが念のため
  - 設定したら*Apply*ボタンをクリック

![Model Setting](doc-images/uni/img08.png)

- *Rig*について、以下を設定します
  - *Animation Type*を*Humanoid*に変更します
  - *Apply*ボタンをクリックします

![Rig Setting](doc-images/uni/img09.png)

これで、*Configure...*の左にチェックが表示されれば成功です。これをやらないと、設定したアーマチュアなどの設定が反映されないので重要な設定です。

以上でキャラクターの読み込みと設定完了です。

## プレイヤーに適用して動かす
読み込んだモデルをテスト用のキャラクターに差し替えて動かして見ましょう。

- *Hierarchy*ビューで、*ThirdPersonController*の左側の三角をクリックして開きます

![Open TPC](doc-images/uni/img10.png)

- *Hierarchy*ビューで、[Shift]キーを押しながら、*EthanBody*, *EthanGlasses*, *EthanSkeleton*の3つを選択します

![Select Original Models](doc-images/uni/img11.png)

- *Inspector*ビューの左上のチェックを外して、選択したオブジェクトを無効にします

![Set Disable](doc-images/uni/img12.png)

- *Project*ビューから読み込んだモデルをドラッグして、*Hierarchy*ビューの*ThirdPersonController*にドロップします

![DaD Model](doc-images/uni/img13.png)

- *Hierarchy*ビューで、ドロップしたモデルをクリックして選択します

![Select My Model](doc-images/uni/img14.png)

- *Inspector*ビューで、*Animator*の左のチェックを外して、モデルにくっついているアニメーターを無効にします

![Disable Animator](doc-images/uni/img15.png)

ThirdPersonControllerのアニメーターを作成したモデルで再生するようにします。

- *Project*ビューで、読み込んだモデルの左の三角をクリックして開いておきます

![open model](doc-images/uni/img17.png)

- *Hierarchy*ビューで、*ThirdPersonController*をクリックして選択します

![select tpc](doc-images/uni/img16.png)

- *Project*ビューからモデルの子供にある*Avatar*をドラッグして、*Inspector*ビューの*Avatar*欄にドロップします

![Set Avatar](doc-images/uni/img18.png)

これで、*ThirdPersonController*のアニメーターが、オリジナルキャラクターのアバターを制御するようになります。

*Play*して、矢印キーなどで操作してみてください。エクスポートに成功していたらアニメーションを確認できます。

![demo](doc-images/uni/ply2fbx.gif)

## キャラクターの大きさを調整したい場合の注意点
動かして見るとちょっとキャラクターが大きすぎるようです。半分の大きさにしてみます。

重要なのは、**親のゲームオブジェクトのScaleを変更しないこと**です。変更するのは、子供にしたモデルのオブジェクトのScaleにしてください。以下の通りです。

![Scaling](doc-images/uni/img19.png)

RigidbodyをアタッチしているゲームオブジェクトのScaleは、必ず`1`にしておきます。これを守らないと当たり判定や動作で予想外の不具合を引き起こします。必ず守りましょう！

# まとめ
以上で、MagicaVoxelで作成したPLY形式のキャラクターにウェイト設定をして、Unityに読み込んで、テスト動作させることができました。

Unity側での作業も少々あるので、一瞬で完了できる、というほどではありませんが、かなり手軽にモデルの修正をして、Unityに持ってくることができるのではないかと思います。

ご活用いただければ幸いです。

# 参考・関連URL
- [Blender](https://www.blender.org/)
- [MagicaVoxel](https://ephtracy.github.io/)
- [Blender 2.79.0 855d2955c49 - API documentation](https://docs.blender.org/api/2.79/)
- [だいし. MagicaVoxelで作ったプリキュアをUnityで動かす](https://github.dev7.jp/b/2015/12/15/precureadv20151213/)

# 1.Python3(Anaconda)のインストール
[ANACONDA](https://www.anaconda.com/distribution/ "ANACONDA")  
このサイトから自身のOS環境のAnacondaをインストール。今回はWindows用のAnacondaをインストール。<br>
インストール時に`Add Anaconda to my PATH environment variable`にチェックを入れる。<br>
これで、コマンドプロンプトからPythonを実行できるようになる。<br>
installされたAnacondaは、`C:\Users\username\Anaconda3`に保存される.
- ANACONDA NAVIGATORを使用して、Pythonの実行環境を準備したりできる。<br>
今後は、ここに実行環境を追加して、プロジェクトごとに必要なファイルを追加する。
## Anacondaとは
「アナコンダ(Anaconda)」とは、データ分析や人工知能技術のためのPythonおよびR言語用のディストリビューション。必要とするライブラリを1つずつインストールする手間を省くことができる。<br>
また、複数の仮想環境を構築することができ、プロジェクトごとに必要なライブラリをinstallすることができる。

# 2.仮想環境の追加
- Windows環境ならコマンドプロンプトを使用
- macOS, Linuxならターミナル・端末を使用  

1. 環境の作成  
コマンドプロンプト上で、`conda`コマンドを使用することで、複数の仮想環境を切り替えて使用することができる。<br>
今回は、py36という名前の環境を作成
`conda create -n py36`

1. 環境へ移動  
- Windowsなら、`activate 環境名`
  - 環境を終了する場合、`deactivate`
- macOS,Linuxなら、`source activate 環境名`
  - 環境を終了する場合、`source deactivate`<br>

移動したら、(環境名)が付く。`(py36) C:\Users\USER>`  
ソフトウェアによっていろんなパッケージが必要になるので、仮想環境を複数作る。  

3. Djangoのインストール<br>
`(py36) C:\Users\USER>conda install django`
- Django以外にも必須のパッケージがinstallされる。

4. バージョンの確認と対話的実行
- バージョンの確認  
```
(py36) C:\Users\USER>python --version
Python 3.8.5
```
- pythonの対話的実行環境を立ち上げる<br>
`(py36) C:\Users\USER>python`<br>
Pythonの演算が可能となる。  
\>>> 3+4<br>
7<br>
\>>> 3*5<br>
15<br>
\>>> 5/3<br>1.6666666666666667<br>
\>>> print('Hello World!')<br>
Hello World!<br>
- 対話的実行環境を抜ける<br>
`exit()`
- 仮想環境の一覧を表示する<br>
`conda info -e`

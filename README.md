# WRS2020トンネル競技に出場するODENSチーム用のChoreonoid拡張

大阪電気通信大学 升谷研究室  
2021年8月  

## 導入

- [choreonoid_ext_ODENS](https://github.com/MasutaniLab/choreonoid_ext_ODENS) を[Choreonoid](https://github.com/choreonoid/choreonoid)のソースツリー中の`choreonoid/ext/ODENS` にする．

- [WRS-TDRRC-2020SG1](https://github.com/WRS-TDRRC/WRS-TDRRC-2020SG1)を基にしているが，ODENSチームの事情に合わせて色々改変している．

- オリジナルを基に改変したファイルには，その名前に`_odens`を付けている．例： `DoubleArmV7A_odens.body`

## 内容

- model
    - ODENS版のDoubleArmV7のモデル
- project
    - ODENS版のDoubleArmV7を使うためのプロジェクト
    - [WRS-TDRRC-2020SG1](https://github.com/WRS-TDRRC/WRS-TDRRC-2020SG1)では，ROS用のPublisherプラグインに[BodyPublisher](https://github.com/choreonoid/choreonoid_ros/tree/master/src/plugin/deprecated)を使っているが，その代わりに，[BodyROS](https://github.com/choreonoid/choreonoid_ros/tree/master/src/plugin)を使っている．[choreonoid_ros](https://github.com/choreonoid/choreonoid_ros)のコードでは，PythonのスクリプトからBodyROSItemを利用できないので，それを改変した[choreonoid_ros_odens](https://github.com/MasutaniLab/choreonoid_ros_odens)を必ず使うこと．
- script
    - 競技用の環境でODENS版のDoubleArmV7を動かすためのプロジェクトを生成するPython Script

## 既知の問題点・TODO


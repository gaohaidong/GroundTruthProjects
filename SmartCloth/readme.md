># 学习下其他小伙伴的做法
># Rank9-round1: 资料待整理，可参考其他代码
>>## https://github.com/maozezhong/TIANCHI_XUELANG_AI
># **Rank28-round1: 锐捷智慧教室团队（郑智雄、吴宏和、黄杰）**
>>## https://github.com/lightfate/XueLang-YOLOhasst
>>## 方法一
>>>### 1. 和我们的思路很像，整体用的是YOLO框架
>>>### 2. 切割和滑动和我之前的想法异曲同工
>>>### 3. 概率融合的方式和我们的不一样
>>>### 4. 遇到的问题和我们一样，边缘处误检为瑕疵
>>## 方法二
>>>### 在方法一的基础上加了全局的思想
>>>### <p> 然后我们开始很哲学地去思考，对于布匹瑕疵检测这个问题，如果是人眼来找瑕疵会怎么做。应该是有两步，一是一眼看过去有没有瑕疵，然后再一块块细看有没有小的瑕疵。实际上我们方法1的切割对应的就是第二步，而我们还缺了第一步，就是全局地去查看。 </p>
>>>### 训练数据
>>>>#### 无重叠分块 6* 8: 块大小320, 块间无重叠
>>>>>##### 缺陷例: Area_defect > 0.3 * 0.3 * Area_total
>>>>>##### 正常例: Area_defect > 0.3 * 0.3 * Area_total
>>>### 训练网络
>>>>#### Inception-Resnet-V2 + SPP
>>>>#### Resnet50, VGG16, 差别不大
>>>### 测试方式
># **Rank32-round1**
>>## https://github.com/bobo0810/XueLangTianchi
>>## 这篇工作应该已经看过了~
># **Rank53-round1**
>>## https://github.com/nlceyes/TianChi-XueLang
># yuhaitao, 1994
>>## https://github.com/yuhaitao1994/Tianchi_xuelangAI_ResNet50withSlim
># LiXin-Ren
>>## https://github.com/LiXin-Ren/TianChi_XueLang
># abosun
>>## https://github.com/abosun/xuelang_round1
># Ref1
>>## https://github.com/akudet/tianchi-xuelang
># Ref2
>>## https://github.com/tuofeilunhifi/xuelang-AI-competition/tree/master/preliminary
># maozehong
>>## https://github.com/maozezhong/TIANCHI_XUELANG_AI
># 徐勇、游剑
>>## https://github.com/Msword9465/Tianchi-Competition

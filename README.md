# deepspace_helper

> Paper Games - Love and DeepSpace



## 1. 一些基础类

目前货币仅实现了加法和乘法。

~~~python
# 货币
Diamond(100)  # 100钻石
StarDice(100) # 100星谕骰

# 角色卡牌
Card(
    rarity=4,
    character="沈星回",
    name="漉漉温言",
    price=StarDice(880)
)

# 衣服
Clothing(
    position="头饰",
    name="童趣小鸭",
    price=StarDice(100)
)
~~~



# 2. 老虎机模块

传入`per_cost`和`chance_table`参数实例化老虎机。

值得一提的是`chance_table`参数的概率之和必须为1。

~~~python
# 构造概率表
sd_100 = StarDice(100)
sd_50 = StarDice(50)
sd_20 = StarDice(20)
sd_10 = StarDice(10)
sd_5 = StarDice(5)

sxh_shower_card, ls_shower_card, qy_shower_card = all_cards["shower_card"]
duck_clothing, bamboo_clothing, horn_clothing = all_clothing["shower_clothing"]

chance_table = {
    sxh_shower_card: 1 / 300,
    ls_shower_card: 1 / 300,
    qy_shower_card: 1 / 300,
    duck_clothing: 0.01,
    bamboo_clothing: 0.01,
    horn_clothing: 0.01,
    sd_100: 0.04,
    sd_50: 0.12,
    sd_20: 0.15,
    sd_10: 0.5,
    sd_5: 0.15
}

sm = SlotMachine(per_cost=Diamond(100), chance_table=chance_table)
~~~

老虎机是一个可调用对象，调用时可指定抽奖次数。

`record`属性是汇总过后的总获奖记录。

~~~python
sm(10)
print(sm.record)
"""
Counter(
    {
        StarDice(value=1): 2175, 
        Clothing(position='头饰', name='竹蜻蜓', price=StarDice(value=100)): 2,
        Clothing(position='头饰', name='黄金尖角', price=StarDice(value=100)): 1
    }
)
"""
~~~

使用`.initialize()`方法初始化老虎机

~~~python
sm.initialize()
print(sm.record)
# Counter()
~~~



# 3. 分析器模块

传入老虎机实例化分析器

~~~python
# 实例化分析器
ana = Analyzer(
    slot_machine=sm
)
~~~



## 3.1 按给定投入实验

~~~python
n_samples = 1000
result_df = ana.roll_by_coins(10000, n_samples=n_samples)

# 查看出货概率
sxh_ratio = len(result_df[result_df[sxh_shower_card] >= 1]) / n_samples
print("沈星回:", sxh_ratio)
# 沈星回: 0.281

# 画图
fig, ax = plt.subplots()
result_df[StarDice(1)].hist(ax=ax)
fig.savefig('star_dice_hist.png')
~~~

从正态分布图中可以看出平均值为1800左右，即投入10000钻石可平均获得1800星谕骰。

![star_dice_hist](https://raw.githubusercontent.com/ShirleySprite/picgo_imgs/master/picgo/star_dice_hist.png)



## 3.2 按给定目标实验

设定目标，注意如果是货币，使用`{Coin(1): n}`的形式传入。

~~~python
# 设定目标
target = {
    sxh_shower_card: 1,
    ls_shower_card: 1,
    qy_shower_card: 1,
}
~~~

~~~python
# 朴素计算
naive_result = ana.roll_by_target_naive(
    target,
    step=10,
    n_samples=1000
)
print("naive_result", naive_result["total_cost"].mean())
# naive_result 10854.0

# 二分计算
bin_result = ana.roll_by_target_bin(
    target,
    n_samples=1000
)

print("bin_search:", bin_result["total_cost"].mean())
# bin_search: 10284.3
~~~

~~~python
# 画图
fig, ax = plt.subplots()
bin_result["total_cost"].hist(ax=ax)
fig.savefig('total_cost_hist.png')
~~~

从正态分布图中可以看出平均值为10000左右，即投入10000钻石可达成三种卡个1张的目标。

![total_cost_hist](https://raw.githubusercontent.com/ShirleySprite/picgo_imgs/master/picgo/total_cost_hist.png)

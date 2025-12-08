幼儿园环境设定见prompt01，共5个场景，
        "classroom",
        "corridor",
        "nap_room",
        "playground",
        "gate_area"
每一天的模拟从7:30在gate_area开始，17:30在gate_area结束。
共10小时，10分钟为一个step，总共60个steps。
每个时间段的活动内容与场景已写入shared memories。



人物分为3类角色(prompt02,03,04)，分别是：
1. Miss T，幼儿园老师
1名，设定包含behavior principles和goal。

2. Sheldon，5岁孤独症儿童(AS)
1名，设定包含behavior principles, goal。

3. Neurotypical Children，神经典型发育儿童(neurotypical, NT)
15名，设定除了behavior principles和goal，还有trait。

data_trait_NT.csv里记录了92名儿童的姓名、年龄、性别以及各种trait的分数。
每轮模拟从92名儿童中随机抽取10名作为本轮的NT儿童角色，MissT和Sheldon固定不变。




value system (prompt05)
Sheldon和NT儿童的行为均受value system影响，他们共用一组5维度的value，但Sheldon和NT儿童在这项维度上的hardcoded_state不同
MissT无value system



test system 
每10分钟(step结束)对NT儿童进行一次测试，测试内容包括
    flap hands(prompt06)  --- v1v2两个版本都需要测试，它们在问题描述上有细微差别
    friendship(prompt07)  --- 这个prompt需要在每轮模拟中将抽样好的{name_list}传入




需要记录的数据：
value system在每个step的变化
每个step结束时的test结果
通过LLM rater和LLM surveryor获得的，每个step中各角色的行为内容和心理活动
# -*- coding: utf-8 -*-
# @File    : main.py
# @Author  : Gczmy
# @Date    : 2023/9/8
# @Software: PyCharm

target_score = 32000


def get_reward_target_score(reward_step):
    reward_target_score = 1000
    if reward_step == 1:
        reward_target_score = 1000
    if reward_step == 2:
        reward_target_score = 2000
    if reward_step == 3:
        reward_target_score = 4000
    if reward_step == 4:
        reward_target_score = 6000
    if reward_step == 5:
        reward_target_score = 8000
    return reward_target_score


def get_open_target_score(step):
    if step == "10 青铜宝箱":
        open_target = 10
    elif step == "20 青铜宝箱":
        open_target = 20
    elif step == "30 黄金宝箱":
        open_target = 30
    elif step == "40 铂金宝箱":
        open_target = 40
    elif step == "80 铂金宝箱":
        open_target = 80
    elif step == "100 铂金宝箱":
        open_target = 100
    elif step == "70 黄金宝箱":
        open_target = 70
    elif step == "50 铂金宝箱":
        open_target = 50
    elif step == "100 钻石宝箱":
        open_target = 100
    else:
        raise ValueError(f'Input \'step\' is not correct: {step}')
    return open_target


class Score:
    def __init__(self, init=0, wood=0, bronze=0, gold=0, platinum=0, step="10 青铜宝箱", step_score=0,
                 open_reward_box=True):
        """
        :param init: 已拥有积分数
        :param wood: 木质宝箱个数
        :param bronze: 青铜宝箱个数
        :param gold: 黄金宝箱个数
        :param platinum: 铂金宝箱个数
        :param step: "10 青铜宝箱", "20 青铜宝箱", "30 黄金宝箱", "40 铂金宝箱", "80 铂金宝箱", "100 铂金宝箱", "70 黄金宝箱",
        "50 铂金宝箱", "100 钻石宝箱"
        :param step_score: 开箱进度分数
        :param open_reward_box: True：开启奖励宝箱分， False：不开启奖励宝箱分（默认开启）
        """
        self.__WOOD_REWARD = 1
        self.__BRONZE_REWARD = 10
        self.__GOLD_REWARD = 20
        self.__PLATINUM_REWARD = 50
        self.__open_reward_box = open_reward_box
        self.__box_score = self.__WOOD_REWARD * wood + self.__BRONZE_REWARD * bronze + self.__GOLD_REWARD * gold \
                           + self.__PLATINUM_REWARD * platinum
        self.__open_rest_score, self.__reward_score, self.__open_step, \
        self.__reward_bronze, self.__reward_gold, self.__reward_platinum = self.__get_reward_score(step, step_score,
                                                                                                   open_reward_box)
        self.__all_score = init + self.__box_score + self.__reward_score
        self.__round, self.__reward_step, self.__rest_score, self.__needed_score = self.__get_open_step()
        self.__reward_target_score = get_reward_target_score(self.__reward_step)
        self.__needed_box_score = self.__get_needed_box_score()

    # GETTERS
    @property
    def open_reward_box(self):
        return self.__open_reward_box

    @property
    def box_score(self):
        return self.__box_score

    @property
    def open_rest_score(self):
        return self.__open_rest_score

    @property
    def reward_score(self):
        return self.__reward_score

    @property
    def open_step(self):
        return self.__open_step

    @property
    def reward_bronze(self):
        return self.__reward_bronze

    @property
    def reward_gold(self):
        return self.__reward_gold

    @property
    def reward_platinum(self):
        return self.__reward_platinum

    @property
    def all_score(self):
        return self.__all_score

    @property
    def round(self):
        return self.__round

    @property
    def reward_step(self):
        return self.__reward_step

    @property
    def rest_score(self):
        return self.__rest_score

    @property
    def needed_score(self):
        return self.__needed_score

    @property
    def reward_target_score(self):
        return self.__reward_target_score

    @property
    def needed_box_score(self):
        return self.__needed_box_score

    def __get_reward_step_parameters(self, step):
        bronze_reward = self.__BRONZE_REWARD
        gold_reward = self.__GOLD_REWARD
        platinum_reward = self.__PLATINUM_REWARD
        bronze = 0
        gold = 0
        platinum = 0
        reward = 0  # reward box score when achieve the open target score
        open_target = 10
        if step == "10 青铜宝箱":  # 10 青铜宝箱
            reward = bronze_reward
            bronze = 1
            step = "20 青铜宝箱"
            open_target = 20
        elif step == "20 青铜宝箱":  # 20 青铜宝箱
            reward = bronze_reward
            bronze = 1
            step = "30 黄金宝箱"
            open_target = 30
        elif step == "30 黄金宝箱":  # 30 黄金宝箱
            reward = gold_reward
            gold = 1
            step = "40 铂金宝箱"
            open_target = 40
        elif step == "40 铂金宝箱":  # 40 铂金宝箱
            reward = platinum_reward
            platinum = 1
            step = "80 铂金宝箱"
            open_target = 80
        elif step == "80 铂金宝箱":  # 80 铂金宝箱
            reward = platinum_reward
            platinum = 1
            step = "100 铂金宝箱"
            open_target = 100
        elif step == "100 铂金宝箱":  # 100 铂金宝箱
            reward = platinum_reward
            platinum = 1
            step = "70 黄金宝箱"
            open_target = 70
        elif step == "70 黄金宝箱":  # 70 黄金宝箱
            reward = gold_reward
            gold = 1
            step = "50 铂金宝箱"
            open_target = 50
        elif step == "50 铂金宝箱":  # 50 铂金宝箱
            reward = platinum_reward
            platinum = 1
            step = "100 钻石宝箱"
            open_target = 100
        elif step == "100 钻石宝箱":  # 100 钻石宝箱
            reward = 0
            step = "10 青铜宝箱"
            open_target = 10
        return reward, step, open_target, bronze, gold, platinum

    def __get_reward_score(self, step, step_score, open_reward_box):
        score = self.__box_score + step_score
        bronze_box = 0
        gold_box = 0
        platinum_box = 0
        bronze_reward = self.__BRONZE_REWARD
        gold_reward = self.__GOLD_REWARD
        platinum_reward = self.__PLATINUM_REWARD
        open_target = get_open_target_score(step)
        while score >= open_target:
            score -= open_target
            reward, step, open_target, bronze, gold, platinum = self.__get_reward_step_parameters(step)
            bronze_box += bronze
            gold_box += gold
            platinum_box += platinum
            if open_reward_box:  # 选择开启奖励分
                score += reward
        reward_score = bronze_reward * bronze_box + gold_reward * gold_box + platinum_reward * platinum_box
        if not open_reward_box:  # 选择不开启奖励分
            reward_score = 0
        return score, reward_score, step, bronze_box, gold_box, platinum_box

    def __get_open_step(self):
        score = self.__all_score
        round = 1
        reward_step = 1
        rest_score = 0
        needed_score = 0
        while score and round <= 4:
            if 0 < score <= 1000:
                reward_step = 1
                rest_score = score
                needed_score = 8000 - score
                break
            elif score <= 2000:
                reward_step = 2
                rest_score = score
                needed_score = 8000 - score
                break
            elif score <= 4000:
                reward_step = 3
                rest_score = score
                needed_score = 8000 - score
                break
            elif score <= 6000:
                reward_step = 4
                rest_score = score
                needed_score = 8000 - score
                break
            elif score <= 8000:
                reward_step = 5
                rest_score = score
                needed_score = 8000 - score
                break
            else:
                score -= 8000
                round += 1
        if round > 4:
            round = 4
            reward_step = 4
            rest_score = score - 32000
            needed_score = 0
        return round, reward_step, rest_score, needed_score

    def __get_needed_box_score(self):
        """
        计算开满奖励所需要的积分（不计算奖励分）
        :return: 积分
        """
        reward_score = 0
        needed_score = self.__needed_score  # 开满奖励所需要的总积分（宝箱积分+奖励积分）
        step = self.__open_step
        open_target = get_open_target_score(step) - self.__open_rest_score
        box_score = 0
        step_score = 0
        all_score = 0
        while all_score < needed_score:
            if needed_score < open_target:
                break
            box_score += 1
            step_score += 1
            if step_score >= open_target:
                step_score -= open_target
                reward, step, open_target, bronze, gold, platinum = self.__get_reward_step_parameters(step)
                reward_score += reward
                step_score += reward  # 奖励的箱子所开的分数也计入开箱进度中
            all_score = box_score + reward_score
        return box_score

    def print(self):
        print(f"当前宝箱积分: {self.box_score},",
              f"选择开启奖励分" if self.open_reward_box else "选择不开启奖励分",
              f"\n当前宝箱开启奖励分: {self.reward_score}, "
              f"奖励青铜宝箱: {self.reward_bronze}, "
              f"奖励黄金宝箱: {self.reward_gold}, "
              f"奖励铂金宝箱: {self.reward_platinum}",
              f"\n当前总积分: {self.all_score}",
              f"\n距离目标积分: {target_score - self.all_score}",
              f"\n最后开箱进度: {self.open_rest_score}{'/'}{self.open_step}",
              f"\n预计完成: {self.round - 1}轮；余: {self.rest_score}积分；"
              f"距离下一轮: {self.needed_score}积分",
              f"\n处在第{self.round}轮，第{self.reward_step}奖励阶段： "
              f"{self.rest_score}{'/'}{self.reward_target_score}",
              f"\n距离下一轮还需宝箱积分: {self.needed_box_score}")


fish_king_box_score = Score(init=0, wood=242, bronze=222, gold=3, platinum=3, step="10 青铜宝箱", step_score=1)
fish_king_box_score.print()

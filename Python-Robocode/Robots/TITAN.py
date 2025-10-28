#! /usr/bin/python
# -*- coding: utf-8 -*-

from robot import Robot
import math
from math import cos, sin, radians

# ---------- helpers ----------
def wh_from(obj):
    if hasattr(obj, "width") and hasattr(obj, "height"):
        return float(obj.width()), float(obj.height())
    if hasattr(obj, "x") and hasattr(obj, "y"):
        return float(obj.x()), float(obj.y())
    if isinstance(obj, (tuple, list)) and len(obj) >= 2:
        return float(obj[0]), float(obj[1])
    if isinstance(obj, dict):
        if "width" in obj and "height" in obj: return float(obj["width"]), float(obj["height"])
        if "x" in obj and "y" in obj:         return float(obj["x"]), float(obj["y"])
    return float(obj[0]), float(obj[1])

# ---------- constants (T800準拠) ----------
MOVE_STEP  = 10
MOVE_LIMIT = 50   # 壁から最小距離

STATE_INIT       = 0
STATE_RUNNING_C0 = 1
STATE_RUNNING_C1 = 2
STATE_RUNNING_C2 = 3

# ---------- dwell(滞留)ブレーカー ----------
DWELL_RADIUS   = 120   # この半径以内に留まっていたら“同じ場所”
DWELL_TICKS    = 700   # これ以上連続滞在で脱出発動
DWELL_COOLDOWN = 900   # 脱出発動後、次の発動までの最小間隔
ESCAPE_HOP     = 260   # 脱出時のオフセット距離（横跳び）

# ---------- 攻勢ウィンドウ（脱出直後だけ射撃を緩める） ----------
ATTACK_WINDOW_TICKS   = 240   # 脱出開始からこのtickだけ攻勢許可
ATTACK_PROBE_INTERVAL = 35    # 攻勢中の牽制射(威力1)の間隔
ATTACK_ERR_DEG        = 12    # 銃口誤差がこの角度以内なら本射可（中遠距離）
ATTACK_NEAR_DIST      = 180   # 近距離なら静止条件無しで撃つ

class TITAN(Robot):
    """T800の挙動をほぼそのままPythonへ移植（型互換のみ追加）
       ＋ “一定エリア滞留ブレーカー” ＋ “脱出直後の攻勢ウィンドウ射撃”
       ※移動系(MyMove/MyGoto/角プラン)は不変、射撃だけ膠着打破用に拡張
    """

    def init(self):
        self.setColor(0, 10, 0)
        self.setGunColor(0, 10, 0)
        self.setRadarColor(0, 0, 0)
        self.setBulletsColor(0, 0, 0)

        self.MapX, self.MapY = wh_from(self.getMapSize())

        self.state = STATE_INIT
        self.runcounter = 0
        self.last_time = 0

        self.C0X = self.C0Y = -1
        self.C1X = self.C1Y = -1
        self.C2X = self.C2Y = -1

        self.radarVisible(True)
        self.lockRadar("gun")     # ← T800同様に砲塔連動
        self.radarGoingAngle = 5
        self.lookingForBot = 0
        self.angleMinBot = 0
        self.angleMaxBot = 0

        self.enemies = {}         # {botId: {"x","y","move"}}

        # --- dwell breaker state ---
        self.dwell_origin = None      # (x,y) 計測開始点
        self.dwell_start  = 0         # 開始tick
        self.last_dwell_escape = -999 # 直近の脱出tick
        self.escape_target = None     # (tx,ty) 一時退避先

        # --- 攻勢ウィンドウ状態 ---
        self.attack_started_tick = -999
        self.attack_probe_last   = -999

    # ---- T800の将来衝突回避つき移動 ----
    def MyMove(self, step: int):
        angle = self.getHeading() % 360
        pos = self.getPosition()
        myX, myY = pos.x(), pos.y()
        deltaY = step * cos(radians(angle))
        deltaX = - step * sin(radians(angle))

        move_ok = True
        if (deltaX > 0) and (myX + deltaX > self.MapX - MOVE_LIMIT): move_ok = False
        if (deltaX < 0) and (myX + deltaX < MOVE_LIMIT):             move_ok = False
        if (deltaY > 0) and (myY + deltaY > self.MapY - MOVE_LIMIT): move_ok = False
        if (deltaY < 0) and (myY + deltaY < MOVE_LIMIT):             move_ok = False

        if move_ok:
            self.move(step)
        else:
            self.rPrint("simulating wall hit, but stopped before contact")
            self.onHitWall()

    # ---- 敵重心から最遠2角の算出（T800準拠）----
    def MyComputeDestAway(self):
        x = y = r = 0
        for botId in self.enemies:
            r += 1
            x += self.enemies[botId]["x"]
            y += self.enemies[botId]["y"]
        if r == 0: return
        x = x // r
        y = y // r

        pos = self.getPosition()
        myX, myY = pos.x(), pos.y()

        if myX > x: self.C1X = self.MapX - MOVE_LIMIT * 1.5
        else:       self.C1X = MOVE_LIMIT * 1.5
        if myY > y: self.C1Y = self.MapY - MOVE_LIMIT * 1.5
        else:       self.C1Y = MOVE_LIMIT * 1.5

        if abs(self.C1X - x) > abs(self.C1Y - y):
            self.C2X = self.C1X
            self.C2Y = self.MapY - self.C1Y
        else:
            self.C2Y = self.C1Y
            self.C2X = self.MapX - self.C1X

    # ---- 角へ行く（T800準拠：バック選択含む）----
    def MyGoto(self, x, y, step, urgency_flag) -> bool:
        pos = self.getPosition()
        myX = int(pos.x())
        myY = int(pos.y())

        x = x // MOVE_LIMIT
        y = y // MOVE_LIMIT
        myX = myX // MOVE_LIMIT
        myY = myY // MOVE_LIMIT

        if myX == x and myY == y:
            return True

        angle = self.getHeading() % 360

        new_angle = -1
        if   x > myX and y > myY: new_angle = 315
        elif x > myX and y < myY: new_angle = 225
        elif x < myX and y < myY: new_angle = 135
        elif x < myX and y > myY: new_angle = 45
        elif x > myX and y == myY: new_angle = 270
        elif x < myX and y == myY: new_angle = 90
        elif x == myX and y < myY: new_angle = 180
        elif x == myX and y > myY: new_angle = 0

        delta_angle = new_angle - angle

        if delta_angle > 90:
            delta_angle -= 180
            step = -step
        if delta_angle < -90:
            delta_angle += 180
            step = -step

        turn_step = -5 if delta_angle < -5 else (5 if delta_angle > 5 else ( -1 if delta_angle < 0 else (1 if delta_angle > 0 else 0) ))
        if turn_step != 0:
            self.turn(turn_step)

        if urgency_flag or abs(delta_angle) < 30:
            self.MyMove(step)

        return False

    # ---- レーダー：角度帯最適化＆単体時の射撃（T800＋緩和）----
    def MyComputeBotSearch(self, botSpotted):
        angles = {}
        e1 = len(self.getEnemiesLeft()) - 1
        e2 = len(self.enemies)
        if e1 == e2 and e2 > 0:
            pos = self.getPosition()
            my_radar_angle = self.getRadarHeading() % 360

            for botId in self.enemies:
                dx = self.enemies[botId]["x"] - pos.x()
                dy = self.enemies[botId]["y"] - pos.y()
                enemy_angle = math.degrees(math.atan2(dy, dx)) - 90
                a = enemy_angle - my_radar_angle
                if a < -180: a += 360
                elif a > 180: a -= 360
                angles[a] = botId

            amin = min(angles.keys())
            amax = max(angles.keys())
            self.angleMinBot = angles[amin]
            self.angleMaxBot = angles[amax]

            if len(self.enemies) == 1:
                # 単体追尾：微調整（T800そのまま）
                if   amin > 0: self.radarGoingAngle = min([5, amin])
                elif amin < 0: self.radarGoingAngle = -min([5, -amin])
                else:          self.radarGoingAngle = 1

                # ---- 元の射撃条件（T800と同じ）----
                if botSpotted!=0 and abs(self.radarGoingAngle)<1 and self.runcounter>self.last_time:
                    dx=self.enemies[angles[amin]]["x"]-pos.x()
                    dy=self.enemies[angles[amin]]["y"]-pos.y()
                    dist=math.sqrt(dx*dx+dy*dy)
                    if self.runcounter-self.enemies[angles[amin]]["move"] > 2:  # 静止2tick
                        power = int(1000/dist)+1
                        # power = max(1, min(10, power))  # ルールに合わせて有効化
                        self.fire(power)
                        self.last_time=self.runcounter+int(dist/150)

                # --- 脱出中だけ少し撃ちやすく（軽い緩和・撃ちすぎ防止に短CD）---
                if self.escape_target is not None and abs(self.radarGoingAngle) < 2 and self.runcounter > self.last_time:
                    dx = self.enemies[angles[amin]]["x"] - pos.x()
                    dy = self.enemies[angles[amin]]["y"] - pos.y()
                    dist = math.sqrt(dx*dx+dy*dy)
                    power = int(1000/dist)+1
                    # power = max(1, min(10, power))
                    self.fire(power)
                    self.last_time = self.runcounter + int(dist / 180)

                # === 追加：攻勢ウィンドウ中の発砲ロジック ===========================
                # 直近で滞留脱出を始めた後、短時間だけ射撃条件を緩める
                if self.attack_started_tick >= 0 and (self.runcounter - self.attack_started_tick) <= ATTACK_WINDOW_TICKS:
                    dx = self.enemies[angles[amin]]["x"] - pos.x()
                    dy = self.enemies[angles[amin]]["y"] - pos.y()
                    dist = math.sqrt(dx*dx + dy*dy)

                    # ① 牽制射（威力1）：間引き＆銃口がほぼ向いている時のみ
                    if abs(self.radarGoingAngle) < 3 and (self.runcounter - self.attack_probe_last) >= ATTACK_PROBE_INTERVAL:
                        self.fire(1)
                        self.attack_probe_last = self.runcounter

                    # ② 本射（低～中パワー）：近距離 or 銃口誤差が小さいとき
                    if abs(self.radarGoingAngle) < 2 and self.runcounter > self.last_time:
                        allow = (dist < ATTACK_NEAR_DIST) or (abs(amin) < ATTACK_ERR_DEG)
                        if allow:
                            power = int(1000/dist)+1
                            # power = max(1, min(10, power))
                            self.fire(power)
                            # 再発射までの間隔を距離連動で少し短めに（元: dist/150）
                            self.last_time = self.runcounter + int(dist / 180)
                # =====================================================================

            elif self.lookingForBot == botSpotted:
                if self.lookingForBot == self.angleMinBot:
                    self.lookingForBot = self.angleMaxBot
                    if self.radarGoingAngle < 0: self.radarGoingAngle = -self.radarGoingAngle
                else:
                    self.lookingForBot = self.angleMinBot
                    if self.radarGoingAngle > 0: self.radarGoingAngle = -self.radarGoingAngle

            elif self.lookingForBot not in self.enemies:
                if self.radarGoingAngle > 0:
                    self.lookingForBot = self.angleMaxBot
                else:
                    self.lookingForBot = self.angleMinBot

    # ---- dwell: 滞留検知（DWELL_RADIUS内に長く留まったらTrue）----
    def _update_dwell(self):
        pos = self.getPosition(); x, y = pos.x(), pos.y()
        if self.dwell_origin is None:
            self.dwell_origin = (x, y); self.dwell_start = self.runcounter
            return False
        # 半径外に出たらリセット
        if math.hypot(x - self.dwell_origin[0], y - self.dwell_origin[1]) > DWELL_RADIUS:
            self.dwell_origin = (x, y); self.dwell_start = self.runcounter
            return False
        # 一定tick以上滞在したら膠着とみなす
        return (self.runcounter - self.dwell_start) >= DWELL_TICKS

    # ---- 脱出先（横跳び）を計算 ----
    def _compute_escape_point(self):
        # 現在方位に対して ±90° へ“横跳び”
        heading = self.getHeading() % 360
        side = -90 if ((self.runcounter // 200) % 2 == 0) else 90  # 200tickごとに左右反転
        ang = math.radians((heading + side) % 360)
        dx = -math.sin(ang) * ESCAPE_HOP
        dy =  math.cos(ang) * ESCAPE_HOP

        x = self.getPosition().x() + dx
        y = self.getPosition().y() + dy
        # マップ内にクランプ（壁自損を避ける）
        tx = max(MOVE_LIMIT, min(self.MapX - MOVE_LIMIT, x))
        ty = max(MOVE_LIMIT, min(self.MapY - MOVE_LIMIT, y))
        return (tx, ty)

    # ---- main（T800の状態機械）----
    def run(self):
        self.runcounter += 1

        # --- 滞留検知：一定エリアに長く滞在したら脱出モード起動 ---
        if self._update_dwell():
            if (self.runcounter - self.last_dwell_escape) > DWELL_COOLDOWN and self.escape_target is None:
                self.escape_target = self._compute_escape_point()
                self.last_dwell_escape = self.runcounter
                self.attack_started_tick = self.runcounter    # 攻勢ウィンドウ開始！
                self.fire(1)  # 脱出開始時に低パワー牽制を1発（自傷リスク低）

        # --- 脱出モード優先（移動はEscape先へ、それ以外は既存の状態機械）---
        if self.escape_target is not None:
            # レーダーは通常通り駆動
            self.MyComputeBotSearch(0)
            self.gunTurn(self.radarGoingAngle)
            # 逃げ先へ移動（緊急フラグTrue）
            if self.MyGoto(self.escape_target[0], self.escape_target[1], MOVE_STEP, True):
                # 到達 → 脱出終了、滞留原点を更新して再計測
                self.escape_target = None
                p = self.getPosition()
                self.dwell_origin = (p.x(), p.y())
                self.dwell_start = self.runcounter
            return  # このtickは脱出移動に専念

        # --- ここから下は元のT800状態機械そのまま ---
        if self.state == STATE_INIT:
            pos = self.getPosition()
            myX, myY = pos.x(), pos.y()
            if myX < self.MapX // 2:
                self.C0X = MOVE_LIMIT
                self.radarGoingAngle = -5
            else:
                self.C0X = self.MapX - MOVE_LIMIT
            if myY < self.MapY // 2:
                self.C0Y = MOVE_LIMIT
            else:
                self.C0Y = self.MapY - MOVE_LIMIT

            self.setRadarField("round")
            self.state = STATE_RUNNING_C0
            self.MyGoto(self.C0X, self.C0Y, MOVE_STEP, True)

        if self.state == STATE_RUNNING_C0:
            if self.runcounter > self.last_time + 5:
                self.setRadarField("thin")
            self.MyComputeBotSearch(0)
            self.gunTurn(self.radarGoingAngle)  # lockRadar("gun")なので砲塔=レーダー
            self.MyGoto(self.C0X, self.C0Y, MOVE_STEP, True)
            if self.C1X != -1:
                self.state = STATE_RUNNING_C1

        if self.state == STATE_RUNNING_C1:
            self.setRadarField("thin")
            self.MyComputeBotSearch(0)
            self.gunTurn(self.radarGoingAngle)
            if self.MyGoto(self.C1X, self.C1Y, MOVE_STEP, False):
                self.state = STATE_RUNNING_C2

        if self.state == STATE_RUNNING_C2:
            self.setRadarField("thin")
            self.MyComputeBotSearch(0)
            self.gunTurn(self.radarGoingAngle)
            if self.MyGoto(self.C2X, self.C2Y, MOVE_STEP, False):
                self.state = STATE_RUNNING_C1

    # ---- events（T800準拠＋攻勢ウィンドウ制御）----
    def onHitWall(self):
        self.rPrint("ouch! a wall !")

    def sensors(self):
        # 死亡敵の掃除
        alive_ids = [r["id"] for r in self.getEnemiesLeft()]
        to_del = [botId for botId in self.enemies if botId not in alive_ids]
        for botId in to_del:
            del self.enemies[botId]

    def onRobotHit(self, robotId, robotName):  pass
    def onHitByRobot(self, robotId, robotName): pass
    def onHitByBullet(self, bulletBotId, bulletBotName, bulletPower): pass

    def onBulletHit(self, botId, bulletId):
        # 命中したら攻勢ウィンドウは終了（十分に状況が動いた）
        self.attack_started_tick = -999

    def onBulletMiss(self, bulletId):          pass
    def onRobotDeath(self):                     pass

    def onTargetSpotted(self, botId, botName, botPos):
        if botId not in self.enemies:
            self.enemies[botId] = {"x": botPos.x(), "y": botPos.y(), "move": self.runcounter}
            self.MyComputeDestAway()
        else:
            if self.enemies[botId]["x"] != botPos.x() or self.enemies[botId]["y"] != botPos.y():
                self.enemies[botId]["x"] = botPos.x()
                self.enemies[botId]["y"] = botPos.y()
                self.enemies[botId]["move"] = self.runcounter
                self.MyComputeDestAway()
        self.MyComputeBotSearch(botId)

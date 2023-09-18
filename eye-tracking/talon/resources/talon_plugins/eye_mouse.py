from collections import defaultdict
from datetime import datetime
from typing import Any, Optional, cast
import json
import math
import os
import queue
import threading
import time

from talon import app, canvas, cron, ctrl, debug, screen, tap, ui, metrics, skia
from talon.api import ffi, lib
from talon.debug import log_exception
from talon.scripting import rctx
from talon.track.filter import PointFilter, OneEuroFilter, Acceleration
from talon.types import Rect, Point2d, Point3d
from talon_init import TALON_HOME
from talon import fs
from talon import usb
from talon.track import tobii
import atexit

main_screen = ui.main_screen()
print(f'@@@@ {os.getcwd()} @@@@')
print(TALON_HOME)
PYTHON_PATH = os.getenv('PYTHONPATH')
PATH_LOGS = PYTHON_PATH + "/examination/tobi_logs/"
NOW = datetime.now()
DATE_LOG = f"logs_examination_{NOW.strftime('%d/%m/%Y %H:%M:%S')}"

eye_samples = []
#### user configuration ####
class config:
    # will be overridden in on_screen_change later
    size_mm: Point2d = Point2d(main_screen.mm_x, main_screen.mm_y)
    offx_mm: float   = 0.0
    rect:    Rect    = main_screen.rect.copy()
    ### Other config ###
    calib_file: str     = os.path.join(TALON_HOME, 'calib.bin')
    velocity: Point2d   = Point2d(150, 225)
    control_mouse: bool = False

    # Acceleration and filter configs
    acceleration = Acceleration.default
    one_euro_filter = OneEuroFilter.default
#### end config

# temp hack until the eye mouse supports multi-eye-tracker
tracker: Optional[tobii.TobiiEC] = None

#setup of tracker
def tracker_setup(tracker: tobii.TobiiEC) -> None:
    with metrics.timeit('eye_open'):
        tracker.display_setup(config.size_mm.x, config.size_mm.y, config.offx_mm)

    if os.path.exists(config.calib_file):
        with open(config.calib_file, 'rb') as f:
            calibration = f.read()

        ctx = rctx.active()
        def start_tracker():
            with cron.watchdog('eye_calibrate', '5s'), ctx.enter():
                with metrics.timeit('eye_set_calibration'):
                    tracker.cmd(tobii.CALIBRATE_UPLOAD, calibration)
                metrics.startup('eye_ready')
                sync_tracker()

        threading.Thread(target=start_tracker).start()

#attaching the device, to log
def on_attach(dev) -> None:
    global tracker
    if isinstance(dev, tobii.TobiiEC):
        if not tracker:
            tracker = dev
            tracker_setup(tracker)
            menu.disabled = False
            no_tracker.hidden = True
            with open(os.path.join(TALON_HOME, 'attach_logs.txt'), 'w+') as file:
                file.write('x')

#detaching the device, log
def on_detach(dev) -> None:
    global tracker
    if dev == tracker:
        tracker = None
        menu.disabled = True
        no_tracker.hidden = False
        with open( os.path.join(TALON_HOME, 'attach_logs.txt'), 'w+') as file:
                file.truncate(0)
                file.write('x')

#detecting blink, let us to gaze
class Blink:
    def __init__(self):
        self.beep = False # requires winsound
        self.two_blinks = True # one blink means you will have lots of misclicks
        self.magic = 4 # CHANGME if not clicking accuratley (won't work on 4C speed probably like =35)
        self.second = False
        self.blinking = False
        self.nosignal = 0
        self.signal = 0
        self.expire = 700 # lower if you blink twice a lot
        self.focus_sensitivity = 50 # 42 pixel focus region before clicking
        self.MAXSIZE = 120
        self.eye_history = []
        self.main_screen = ui.main_screen()
        self.size_px = Point2d(self.main_screen.width, self.main_screen.height)
        self.get_time = lambda: int(round(time.time() * 1000))
        self.current_time = 0
        self.first_blink = 0
        self.eyes = True
        self.last_blink = False

    def hist_add(self, key, value):
        if len(self.eye_history) == self.MAXSIZE:
            min = int(self.MAXSIZE//2)
            self.eye_history = self.eye_history[self.MAXSIZE//2:]
        self.eye_history.append(value)


    def estimate_focus(self, eye_history, magic):
        if magic <= 6:
            lo = magic-3 # 3
        elif magic <= 5:
            lo = magic-2 # 3
        elif magic <=3:
            lo = magic-2 # 1
        else:
            lo = 1
        hi = lo+magic+8
        counter = 0
        x_avg = 0; y_avg = 0
        for i in range(lo,hi+1):
            x = eye_history[-1*i][0]
            y = eye_history[-1*i][1]
            x_avg+=x; y_avg += y; counter+=1
        x_avg = x_avg/counter; y_avg = y_avg/counter
        return x_avg,y_avg

    
    def on_gaze(self, frame):
        # probablsy does not need to fire every time, but I timed it with gazes
        l, r = frame.left, frame.right
        pos = frame.gaze
        pos *= self.size_px
        self.current_time = int(self.get_time())
        with open(os.path.join(PATH_LOGS, 'logs.txt'), 'a+') as file:
            file.write(f'{time.time()}, {pos.x}, {pos.y}\n')
            file.close()
        if not (pos.x <= 0 and pos.y <= 0):
            # Eye signal
            self.nosignal = 0
            self.signal += 1
            if self.signal < 3:#4:
                return 
            if self.eyes == False:
                if self.two_blinks:
                    if abs(self.current_time-self.first_blink) > self.expire:
                        # Second blink, but expired.
                        with open(os.path.join(TALON_HOME, 'blink.txt'), 'a+') as file:
                            file.write(f'{time.time()}\n')
                            file.close()
                        print("Click expired:",self.current_time-self.first_blink)
                        self.first_blink = self.current_time
                        self.second = False
                    if not self.second:
                        try:
                            try:
                                self.target_history = self.eye_history[-1*self.magic]
                            except Exception as e:
                                print(e)
                                self.target_history = self.eye_history[len(self.eye_history)*-1]

                            fx,fy = self.estimate_focus(self.eye_history, self.magic)
                            self.target_x, self.target_y = self.target_history[0], self.target_history[1]

                            if abs(fx-self.target_x) > self.focus_sensitivity \
                                            or abs(fy-self.target_y) > self.focus_sensitivity:
                                print("Misclick assumed, not focusing enough or change params.")
                                print(abs(fx-self.target_x),abs(fy-self.target_y))
                                self.first_blink = self.current_time-15000 
                                if self.beep: self.beep_win(3500,20)
                            else:
                                self.first_blink = self.current_time
                            self.second = True
                        except Exception as e:
                            print("ERR",e)
                    else:
                        pass
                    pass
            self.eyes = True
            px,py = ctrl.mouse_pos()
            self.hist_add(self.current_time, [px,py])
        else:
            # no signal
            self.signal = 0
            if self.nosignal == 0:
                self.eyes = False
            self.nosignal += 1

blink = Blink()

#additional
class EyeMouse:
    eye_hist:   list[tobii.GazeFrame]
    xy_hist:    list[Point2d]
    delta_hist: list[Point2d]
    last_time:  float
    filt: PointFilter

    jump_filt:  PointFilter
    jump_queue: list[Point2d]
    origin: Point2d
    accel:  PointFilter

    clicking:   bool
    last_click: float

    last_ctrl: Optional[Point2d]
    last_move: float
    move_clicking: bool
    break_force:   float

    zone1: Optional[tuple[Point2d, Point2d, float]]
    zone2: Optional[tuple[Point2d, Point2d, float]]

    lock: threading.RLock
    attached_tracker: Optional[tobii.TobiiEC]

    def __init__(self):
        self.eye_hist   = []
        self.xy_hist    = []
        self.delta_hist = []
        self.last_time  = 0.0
        self.filt       = PointFilter(OneEuroFilter, **config.one_euro_filter)
        self.jump_filt  = PointFilter(OneEuroFilter, **config.one_euro_filter)
        self.jump_queue = []
        self.origin     = Point2d(0, 0)
        self.accel      = PointFilter(Acceleration, **config.acceleration)

        self.clicking   = False
        self.last_click = 0

        self.last_ctrl = None
        self.last_move = 0
        self.move_clicking = False
        self.break_force   = 0

        self.zone1 = self.zone2 = None
        self.lock  = threading.RLock()
        self.attached_tracker = None

    def reset(self) -> None:
        self.last_ctrl = None
        self.last_move = 0

    def enable(self) -> None:
        with self.lock:
            if self.attached_tracker != tracker:
                try:
                    if self.attached_tracker:
                        self.attached_tracker.unregister('gaze', self.on_gaze)
                except Exception: pass
                if tracker:
                    tracker.register('gaze', self.on_gaze)
                    tap.register(tap.MCLICK, self.on_click)
                self.attached_tracker = tracker
            self.reset()

    def disable(self) -> None:
        with self.lock:
            if self.attached_tracker is not None:
                try:
                    self.attached_tracker.unregister('gaze', self.on_gaze)
                except Exception: pass
                self.attached_tracker = None
                tap.unregister(tap.MCLICK, self.on_click)

    def on_click(self, e):
        if e.up:
            self.clicking = bool(ctrl.mouse_buttons_down())

    def recent_click(self) -> bool:
        now = time.perf_counter()
        if not self.clicking:
            if ctrl.mouse_buttons_down():
                self.clicking = True
                self.last_click = now
        if self.clicking and now - self.last_click < 0.32:
            return True
        return False

    def on_gaze(self, frame: tobii.GazeFrame) -> None:
        now = frame.ts
        l, r = frame.left, frame.right

        rect = config.rect
        pos  = cast(Point2d, frame.gaze)
        if pos is None:
            return
        pos = rect.pos + pos * rect.size
        pos = rect.clamp(pos)

        if self.last_time == 0:
            self.origin = pos
        if self.xy_hist and not (l or r):
            pos = self.xy_hist[-1]
        pos.ts = now

        origin = pos
        delta = Point2d(0, 0)
        dt = 1 if self.last_time == 0 else now - self.last_time
        self.last_time = now
        if dt < 1e-6:
            return

        deltas: tuple[Point2d, ...] = ()
        eye_recent = [(frame.left.rel, frame.right.rel)
                       for frame in self.eye_hist
                       if frame.ts >= now - 0.100]
        left_recent  = [ll for ll, lr in eye_recent if not ll.zero()]
        right_recent = [lr for ll, lr in eye_recent if not lr.zero()]
        if left_recent and not l.rel.zero():
            ll = left_recent[-1]
            ldelt = (l.rel - ll) / 2
            deltas += ldelt,
        if right_recent and not r.rel.zero():
            lr = right_recent[-1]
            rdelt = (r.rel - lr) / 2
            deltas += rdelt,

        if self.eye_hist and self.xy_hist and deltas:
            out = []
            for delt in deltas:
                out.append(Point2d(-delt.x, delt.y))
            delt = out[0]
            for o in out[1:]:
                delt += o
            delt /= len(out)

            delt = self.filt(delt, dt=dt)
            delt *= config.velocity
            delt = self.accel(delt, dt=dt)

            if self.recent_click():
                if abs(delt.x) < 10 and abs(delt.y) < 10:
                    delt.x = delt.y = 0

            lastpos = self.last_ctrl or self.xy_hist[-1]
            travel = (lastpos - self.origin).len()
            elapsed = pos.ts - self.origin.ts
            zone1 = 200 * min((elapsed / 0.6) ** 2, 1)
            zone2 = (math.log(max(travel, zone1 / 4) + 20) * 18)
            # prevents jump when recent velocity over a threshold
            recent_delta = [d for d in self.delta_hist if d.ts >= now - 0.100] + [delt]
            if recent_delta:
                avg_velocity = (sum(recent_delta, start=Point2d(0, 0)) / len(recent_delta)).len()
                no_jump = avg_velocity > 2.5

            center2 = lastpos
            self.zone1 = (pos, self.origin, zone1)
            self.zone2 = (pos, center2, zone2)
            exit1 = (pos - self.origin).len() > zone1
            exit2 = (pos - center2).len() > zone2
            if elapsed > 0.050 and exit1 and exit2 and not no_jump:
                if self.jump_queue:
                    queue = self.jump_queue + [pos]
                    self.jump_queue = []
                    pos = sum(queue, start=Point2d(0, 0)) / len(queue)
                    pos.ts = now
                self.origin = pos
            elif elapsed <= 0.050 and not exit2 and not no_jump:
                self.jump_queue.append(pos)
                pos = lastpos
            else:
                pos = lastpos + delt
            delta = pos - lastpos

        pos.ts = now
        delta.ts = now
        self.eye_hist.append(frame)
        self.xy_hist.append(pos)
        self.delta_hist.append(delta)
        self.eye_hist = self.eye_hist[-90 * 10:]
        self.xy_hist = self.xy_hist[-90 * 10:]
        self.delta_hist = self.delta_hist[-90 * 10:]

        should_move = bool(l or r) and delta.len() > 0.00001
        x, y = rect.clamp(pos)
        if config.control_mouse and should_move:
            ref = Point2d(*ctrl.mouse_pos())
            clicking = bool(ctrl.mouse_buttons_down())
            if now - self.last_move > 0.5 and not (self.move_clicking and clicking):
                if self.last_ctrl:
                    self.break_force *= 0.95
                    dist = math.floor(min((p - ref).len() for p in [self.last_ctrl] + self.xy_hist[-10:]))
                    if dist > 1:
                        self.break_force += dist
                    if self.break_force < 0.005:
                        self.break_force = 0
                if self.last_ctrl and self.break_force > 6:
                    self.break_force = 0
                    self.last_move = now
                    origin.ts = self.origin.ts
                    self.origin = origin
                    self.move_clicking = clicking
                else:
                    global eye_samples
                    ref = Point2d(x, y)
                    self.move_clicking = False
                self.last_ctrl = ref

mouse = EyeMouse()

#calibration of tracker
class Calibration:
    tracker:  tobii.TobiiEC
    gaze:     list[Point2d]
    points:   list[Point2d]
    ctx:      rctx.ResourceContext
    tests:    list[list[Point2d]]
    test_num: int
    running:  bool
    success:  bool
    streamq:  queue.Queue[tobii.GazeFrame]
    canvas:   Optional[canvas.Canvas]
    green:    Optional[Point2d]

    def __init__(self, tracker):
        self.tracker = tracker
        self.gaze = []
        self.points = []
        self.ctx = rctx.active()
        tests = [
            [(0.5, 0.5)],
            [(0.5, 0.95), (0.05, 0.5), (0.95, 0.5), (0.5, 0.05)],
            [(0.1, 0.1), (0.9, 0.9), (0.1, 0.9), (0.9, 0.1)],
        ]
        self.tests = [[Point2d(*p) for p in test] for test in tests]
        self.test_num = 0
        self.running = False
        self.success = False
        self.streamq = queue.Queue()
        self.canvas = None
        self.green = None

        t = threading.Thread(target=self.stream_loop)
        t.daemon = True
        t.start()

    def cmd(self, *args, thread: bool=False) -> Any:
        if thread:
            t = threading.Thread(target=self.tracker.cmd, args=args)
            t.daemon = True
            t.start()
        else:
            return self.tracker.cmd(*args)

    def start(self) -> None:
        if not tracker:
            raise ValueError('need tracker to calibrate')
        self.tracker = tracker
        self.started = datetime.utcnow()
        self.success = False
        self.data_size = 0
        self.green = None

        if self.canvas:
            self.canvas.unregister('draw', self.draw)
            self.canvas.close()
        self.canvas = canvas.Canvas.from_screen(main_screen)
        self.canvas.fullscreen = True
        self.canvas.blocks_mouse = True
        self.canvas.focused = True
        self.canvas.register('draw', self.draw)
        self.canvas.register('key', self.on_canvas_key)
        self.canvas.register('focus', self.on_canvas_focus)
        self.running = True
        self.tracker.register('gaze', self.stream_queue)
        self.test_num = 0
        self.points = self.tests[self.test_num].copy()
        try:
            self.gaze = []
            self.cmd(tobii.CALIBRATE_START)
            try: self.cmd(tobii.CALIBRATE_CLEAR)
            except tobii.EyeCmdErr:
                pass
        except Exception:
            log_exception('error starting calibration')
            app.notify('error starting calibration')
            self.stop()

    def on_canvas_key(self, e):
        if e.key == 'esc':
            self.stop()

    def on_canvas_focus(self, focused: bool) -> None:
        if not focused:
            self.stop()

    def stop(self) -> None:
        try:
            self.tracker.unregister('gaze', self.stream_queue)
        except Exception:
            pass
        metrics.record('eye_calibration_finished',
                       fields={
                           'success': self.success,
                           'duration': (datetime.utcnow() - self.started),
                           'data_size': self.data_size,
                       })

        if self.canvas:
            self.canvas.fullscreen = False
            self.canvas.blocks_mouse = False
            self.canvas.unregister('draw', self.draw)
            self.canvas.unregister('key', self.on_canvas_key)
            self.canvas.unregister('focus', self.on_canvas_focus)
            self.canvas.close()
            self.canvas = None
        if self.running:
            self.gaze = []
            self.points = []
            self.running = False
            self.cmd(tobii.CALIBRATE_STOP)

    def stream_loop(self) -> None:
        with self.ctx.enter(), debug.collapse_thread(tag='eye_mouse', label='eye mouse event thread'):
            while True:
                msg = self.streamq.get()
                try:
                    self.on_gaze(msg)
                except:
                    log_exception('eye mouse thread error')
                    try:
                        calib_stop()
                    except Exception:
                        pass

    def stream_queue(self, msg: tobii.GazeFrame) -> None:
        self.streamq.put(msg)

    def on_gaze(self, frame: tobii.GazeFrame) -> None:
        pos = cast(Point2d, frame.gaze)
        if pos is None:
            return
        pos.ts = frame.ts
        self.gaze.append(pos)
        self.gaze = [p for p in self.gaze if p.ts >= pos.ts - 2]
        self.gaze = self.gaze[-120:]

        hits = []
        if self.running and self.points:
            try:
                for pos in self.gaze:
                    close = self.points[0]
                    diag = (pos - close).len()
                    for p in self.points[1:]:
                        d = (p - pos).len()
                        if d < diag:
                            close = p
                            diag = d
                    if diag < 0.75:
                        hits.append(close)

                match = None
                for point in self.points:
                    if hits.count(point) > 60 and point is self.green:
                        match = point

                if match:
                    self.cmd(tobii.CALIBRATE_POINT_ADD2D, match.x, match.y, 3)
                    self.gaze = []
                    self.points.remove(match)

                if not self.points:
                    self.cmd(tobii.CALIBRATE_POINTS_APPLY)
                    self.test_num += 1
                    if self.test_num >= len(self.tests):
                        self.cmd(tobii.CALIBRATE_STOP)
                        with metrics.timeit('eye_get_calibration'):
                            data = self.cmd(tobii.CALIBRATE_DOWNLOAD)
                        self.data_size = 0
                        if data:
                            self.data_size = len(data[0])
                            with open(config.calib_file, 'wb') as f:
                                f.write(data[0])
                        self.running = False
                        self.success = True
                        with open(os.path.join(TALON_HOME, 'calib_logs.txt'), 'w+') as f:
                            f.write('x')
                        self.gaze = []
                        calib_stop()
                    else:
                        self.points = self.tests[self.test_num].copy()
            except Exception:
                log_exception('calibration failed')
                calib_stop()

    def draw(self, canvas: skia.Canvas):
        if not self.running:
            return False

        paint = canvas.paint
        paint.color = '3c3c3c'
        paint.style = paint.Style.FILL
        rect = canvas.rect
        canvas.draw_rect(rect)

        if not self.gaze: return
        pos = self.gaze[-1]

        paint.stroke_width = 2
        for p in self.points:
            dist = (pos - p).len()
            fill = 0.0
            if dist < 0.20:
                fill = (1.0 - dist / 0.25)
                self.green = p

            paint.style = paint.Style.STROKE
            paint.color = 'ffffff'
            pos = rect.pos + rect.size * p
            canvas.draw_circle(pos.x, pos.y, 8)

            paint.style = paint.Style.FILL
            paint.color = (0, int(fill * 255), 0, 255)
            canvas.draw_circle(pos.x, pos.y, 8)

#calibration start
def calib_start() -> None:
    if not tracker:
        app.notify('Error', 'No eye tracker found')
        return
    calib.start()

def calib_stop() -> None:
    calib.stop()

from talon import app

def sync_tracker() -> None:
    from talon_plugins import eye_zoom_mouse
    external = eye_zoom_mouse.zoom_mouse.enabled
    if tracker and (config.control_mouse or external):
        mouse.enable()
    else:
        mouse.disable()

def toggle_control(state: bool) -> None:
    config.control_mouse = state
    sync_tracker()

def toggle_debug_overlay(state: bool) -> None:
    raise NotImplementedError

# used by knausj_talon
def toggle_camera_overlay(state: bool) -> None:
    raise NotImplementedError

menu = app.menu.submenu('Eye Tracking', weight=999, disabled=True)
app.menu.sep(weight=998)

no_tracker = menu.item('No eye tracker found.', weight=1000, hidden=True)
menu.sep(weight=999)
if not tracker:
    menu.disabled = True
    no_tracker.hidden = False

calibration_button = menu.item('Calibrate', weight=3, cb=lambda item: calib_start())
menu.sep(weight=2)
control_mouse = menu.toggle('Track eyes', weight=2, cb=lambda item: tracker.register('gaze', blink.on_gaze)) #toggle_control

ui.register('screen_sleep', lambda e: tracker and tracker.cmd(tobii.PAUSE_SET, 1))
ui.register('screen_wake',  lambda e: tracker and tracker.cmd(tobii.PAUSE_SET, 0))

calib = Calibration(tracker)
usb.register('attach', on_attach)
usb.register('detach', on_detach)

for dev in usb.devices():
    on_attach(dev)

calib_started = False
eye_tracking_started = False
no_data_combo = 0

#start tracker after running script
tracker.register('gaze', blink.on_gaze)

#maybe we need that later
# def on_change(x,y):
#     with open(communication_path,'r+') as f:
#         lines = f.read().splitlines()
#         last_command = lines[-1].split()[-1]
#         print(last_command)
#         if last_command == 'calibration':
#             calib_start()
#         elif last_command == 'tracking':
#             tracker.register('gaze', blink.on_gaze)
#         f.close()


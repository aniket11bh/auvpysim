#
# Testing solutions for Coursera
#
#
#
try:
  from urllib import urlencode
  from urllib2 import urlopen
except Exception:
  from urllib.parse import urlencode
  from urllib.request import urlopen
import hashlib
import base64
import re
import math
import helpers

class CourseraException(Exception):
    pass

class WeekTestCase:
    
    RX = re.compile(r"(?P<name>[a-zA-Z_]+)=(?P<value>-?[0-9]+(?:\.[0-9]+)?);")
    
    def __init__(self, week):
        self.testsuite = week
        self.name = "Name not set"
        self.test_id = "XXXYYYZZZ"
        
    def parseChallenge(self,challenge):
        result = {}
        for m in self.RX.finditer(challenge):
            try:
                result[m.group('name')] = float(m.group('value'))
            except Exception:
                raise CourseraException("Unknown challenge format. Please contact developers for assistance.")                
        return result

class WeekTest:
    coursera_challenge_url = "http://class.coursera.org/conrob-002/assignment/challenge"
    coursera_submit_url = "http://class.coursera.org/conrob-002/assignment/submit"

    def __init__(self, gui):
        self.gui = gui
        self.week = 0
        # Test is a tuple - 'title','id',function
        self.tests = []
        self.login = None
        self.password = None
        
        self.callback = None
        self.submit = True
        
        self.testname = 'Name not set'
    
    def setuser(self, login, password):
        self.login = str(login).strip()
        self.password = str(password).strip()
    
    def run_tests(self,tests = None):
        if tests is None:
            tests = list(range(len(self.tests)))
        for i in tests:
            self.test(self.tests[i])
    
    def test(self,testcase,callback):
        
        if isinstance(testcase,int):
            testcase = self.tests[testcase]
        
        self.callback = callback
        self.testcase = testcase

        params = urlencode({
            'email_address' : self.login,
            'assignment_part_sid' : testcase.test_id,
            'response_encoding' : 'delim'
            }).encode('utf-8')
        response = urlopen(url=WeekTest.coursera_challenge_url, data = params)

        string = response.read().decode('utf-8').split('|')[1:]

        self.c_response = {}
        for i in range(len(string)//2):
            try:
                self.c_response[string[2*i]] = string[2*i+1]
            except Exception:
                pass
            
        if 'email_address' not in self.c_response or not self.c_response['email_address']:
            raise CourseraException("Communication with server failed")
        elif 'challenge_key' not in self.c_response or not self.c_response['challenge_key'] \
                or 'state' not in self.c_response or not self.c_response['state']:
            # Error occured, error string in email_address
            raise CourseraException(self.c_response['email_address'])
        
        testcase.start_test(self.c_response['challenge_aux_data'])

    def respond(self,fn_output):
        
        if self.callback is None:
            return

        ch_resp = hashlib.sha1((self.c_response['challenge_key'] + self.password).encode('utf-8')).hexdigest()

        params = urlencode(
        {'assignment_part_sid': self.testcase.test_id,
            'email_address': self.c_response['email_address'],
            'submission': base64.standard_b64encode(fn_output.encode('utf-8')),
            'submission_aux': b'',
            'challenge_response': ch_resp,
            'state': self.c_response['state']}).encode('utf-8');
        
        self.callback(urlopen(url=self.coursera_submit_url, data = params).read().decode('utf-8'))
        
        self.testcase = None
        self.callback = None

class Week1(WeekTest):
  def __init__(self, gui):
    WeekTest.__init__(self, gui)
    
    self.testname = "Programming Assignment Week 1"
    
    self.week = 1
    self.tests.append(Week1Test1(self))
    
class Week1Test1(WeekTestCase):
    def __init__(self, week):
        self.testsuite = week
        self.name = "Running the simulator"
        self.test_id = "k3pa0rK4"

    def __call__(self,event,args):
        if event == "log":
            message, objclass, objcolor = args
            if message == "Switched to Hold":
                self.stop_test()
                self.testsuite.respond("-1")
        return False
        
    def start_test(self,challenge):
        self.testsuite.gui.start_testing()
        self.testsuite.gui.load_world('week1.xml')
        self.testsuite.gui.register_event_handler(self)
        self.testsuite.gui.run_simulation()
        
    def stop_test(self):
        self.testsuite.gui.unregister_event_handler()
        self.testsuite.gui.stop_testing()       

class Week2(WeekTest):
  def __init__(self, gui):
    WeekTest.__init__(self, gui)
    
    self.testname = "Programming Assignment Week 2"
    
    self.week = 2
    self.tests.append(Week2Test1(self))
    self.tests.append(Week2Test2(self))
    self.tests.append(Week2Test3(self))
    
class Week2Test1(WeekTestCase):
    """Test 1: Test uni2diff"""
    def __init__(self, week):
        self.testsuite = week
        self.name = "Unicycle to differential-drive\ntransformation"
        self.test_id = "QihGedxL"
        
    def start_test(self,challenge):
        vals = self.parseChallenge(challenge)
        
        if 'v' not in vals or 'w' not in vals:
            raise CourseraException("Unknown challenge format. Please contact developers for assistance.")

        v = vals['v']
        w = vals['w']
                    
        from supervisors.week2 import QuickBotSupervisor
        from robots.quickbot import QuickBot
        from pose import Pose
        
        info = QuickBot(Pose()).get_info()
        info.color = 0
        s = QuickBotSupervisor(Pose(),info)
        
        vl, vr = s.uni2diff((v,w))
        
        self.testsuite.respond("{:0.3f},{:0.3f}".format(vr,vl)) # Note the inverse order
        
class Week2Test2(WeekTestCase):
    def __init__(self, week):
        self.testsuite = week
        self.name = "Odometry"
        self.test_id = "TQkrYtec"
        
    def start_test(self,challenge):
        vals = self.parseChallenge(challenge)
        
        if 'v' not in vals or 'theta' not in vals:
            raise CourseraException("Unknown challenge format. Please contact developers for assistance.")

        v = vals['v']
        theta = vals['theta']
                    
        from supervisors.week2 import QuickBotSupervisor
        from robots.quickbot import QuickBot
        from pose import Pose
        from helpers import Struct
        from math import pi
        
        bot = QuickBot(Pose())
        info = bot.get_info()
        info.color = 0
        s = QuickBotSupervisor(Pose(),info)
        params = Struct()
        params.goal = theta*180/pi
        params.velocity = v
        params.pgain = 1
        s.set_parameters(params)
        
        tc = 0.033 # 0.033 sec' is the SimIAm time step
        
        for step in range(25): # 25 steps
            bot.move(tc)
            bot.set_inputs(s.execute(bot.get_info(), tc))
            
        xe,ye,te = s.pose_est
        xr,yr,tr = bot.get_pose()
        
        if xr == 0:
            xr = 0.0000001
        if yr == 0:
            yr = 0.0000001
        if tr == 0:
            tr = 0.0000001
        
        self.testsuite.respond("{:0.3f},{:0.3f},{:0.3f}".format(abs((xr-xe)/xr), abs((yr-ye)/yr), abs(abs(tr-te)%(2*pi)/tr)))

class Week2Test3(WeekTestCase):
    
    def __init__(self, week):
        self.testsuite = week
        self.name = "Converting raw IR sensor values\nto distances"
        self.test_id = "yptGGVPr"
        
    def start_test(self,challenge):
        vals = self.parseChallenge(challenge)
        
        if 'd1' not in vals or 'd2' not in vals:
            raise CourseraException("Unknown challenge format. Please contact developers for assistance.")

        d1 = vals['d1']
        d2 = vals['d2']
                    
        from supervisors.week2 import QuickBotSupervisor
        from robots.quickbot import QuickBot, QuickBot_IRSensor
        from pose import Pose
        
        bot = QuickBot(Pose())
        sensor = QuickBot_IRSensor(Pose(),bot)
        
        id1 = sensor.distance_to_value(d1)
        id2 = sensor.distance_to_value(d2)
        
        info = bot.get_info()
        info.color = 0
        s = QuickBotSupervisor(Pose(),info)
        # Just in case a student iterates in a weird way
        s.robot.ir_sensors.readings = [id1,id2,id1,id2,id1]
        ird = s.get_ir_distances()
                    
        self.testsuite.respond("{:0.3f},{:0.3f}".format(abs((d1-ird[0])/d1), abs((d2-ird[1])/d2)))

class Week3(WeekTest):
  def __init__(self, gui):
    WeekTest.__init__(self, gui)
    
    self.testname = "Programming Assignment Week 3"
    
    self.week = 3
    self.tests.append(Week3Test1(self))
    self.tests.append(Week3Test2(self))
    self.tests.append(Week3Test3(self))

class Week3Test1(WeekTestCase):
    """Run the simulator until the robot reaches the goal or collides with the wall.
       Stops after 30 seconds."""    
    def __init__(self, week):
        self.testsuite = week
        self.name = "Arriving at the goal location"
        self.test_id = "pKyj9jyA"
        
        self.dst2goal = 'math.sqrt((robot.get_pose().x - supervisor.parameters.goal.x)**2 + (robot.get_pose().y - supervisor.parameters.goal.y)**2)'

    def __call__(self,event,args):
        if self.testsuite.gui.simulator_thread.get_time() > 30:
            self.stop_test()
            self.testsuite.respond("0")
        
        if event == "plot_update": # get distance to goal from the simulator
            dst = args[0][self.dst2goal]
            if dst < 0.05:
                self.stop_test()
                self.testsuite.respond("1")
        elif event == "log": # watch for collisions
            message, objclass, objcolor = args
            if message.startswith("Collision with"):
                self.stop_test()
                self.testsuite.respond("0")
        elif event == "make_param_window": # in the beginning rewrite parameters
            robot_id, name, params = args
            # FIXME What follows is a hack, that will only work
            # in the current GUI implementation. 
            # For a better solution we need to change the API again
            params[0][1][0] = ('x',self.p.goal.x)
            params[0][1][1] = ('y',self.p.goal.y)
            params[1][1][0] = ('v',self.p.velocity.v)
            params[2][1][0] = (('kp','Proportional gain'), self.p.gains.kp)
            params[2][1][1] = (('ki','Integral gain'), self.p.gains.ki)
            params[2][1][2] = (('kd','Differential gain'), self.p.gains.kd)
           
            self.testsuite.gui.run_simulator_command('apply_parameters', robot_id, self.p)

        #elif event == 'reset' # World constructed, safe    
            
        return False
        
    def stop_test(self):
        self.testsuite.gui.unregister_event_handler()
        self.testsuite.gui.pause_simulation()   
        self.testsuite.gui.stop_testing()   
 
    def start_test(self,challenge):
        vals = self.parseChallenge(challenge)
        
        if 'v' not in vals or 'x_g' not in vals or 'y_g' not in vals:
            raise CourseraException("Unknown challenge format. Please contact developers for assistance.")
        
        self.p = helpers.Struct()
        self.p.goal = helpers.Struct()
        self.p.goal.x = vals['x_g']
        self.p.goal.y = vals['y_g']
        self.p.velocity = helpers.Struct()
        self.p.velocity.v = vals['v']
        self.p.gains = helpers.Struct()
        self.p.gains.kp = 3
        self.p.gains.ki = 6
        self.p.gains.kd = 0.01
        
        docks = self.testsuite.gui.dockmanager.docks
        if len(docks):
            dock = docks[list(docks.keys())[0]]
            self.p.gains = dock.widget().contents.get_struct().gains

        self.testsuite.gui.start_testing()
        self.testsuite.gui.register_event_handler(self)
        self.testsuite.gui.load_world('week3.xml')
        self.testsuite.gui.run_simulator_command('add_plotable',self.dst2goal)
        
        #self.testsuite.gui.dockmanager.docks[self.dockname].widget().apply_click()
        
        self.testsuite.gui.run_simulation()
        
class Week3Test2(WeekTestCase):
    """Test 2: check if the PID gains do not lead to oscillations"""
    def __init__(self, week):
        self.testsuite = week
        self.name = "Tuning the PID gains for performance"
        self.test_id = "2aZEky7h"
        
        self.dtheta = '((math.atan2(supervisor.parameters.goal.y - robot.get_pose().y, supervisor.parameters.goal.x - robot.get_pose().x) - robot.get_pose().theta + math.pi)%(2*math.pi) -math.pi)/math.atan2(supervisor.parameters.goal.y,supervisor.parameters.goal.x)'
        self.dst2goal = 'math.sqrt((robot.get_pose().x - supervisor.parameters.goal.x)**2 + (robot.get_pose().y - supervisor.parameters.goal.y)**2)'
          
    def __call__(self,event,args):
        if self.testsuite.gui.simulator_thread.get_time() > 15: # Not more than 15 minutes
            self.stop_test()
        
        if event == "plot_update": # get dtheta
            
            dtheta = args[0][self.dtheta]
            self.dthetas.append(abs(dtheta))
            if dtheta < self.dtheta_min:
                self.dtheta_min = dtheta           
                
            dst2goal = abs(args[0][self.dst2goal])
            if dst2goal < 0.05:
                self.stop_test()
                
        elif event == "log": # watch for collisions
            message, objclass, objcolor = args
            if message.startswith("Collision with"):
                self.stop_test()
        elif event == "make_param_window": # in the beginning rewrite parameters
            robot_id, name, params = args
            # FIXME What follows is a hack, that will only work
            # in the current GUI implementation. 
            # For a better solution we need to change the API again
            params[0][1][0] = ('x',self.p.goal.x)
            params[0][1][1] = ('y',self.p.goal.y)
            params[1][1][0] = ('v',self.p.velocity.v)
            params[2][1][0] = (('kp','Proportional gain'), self.p.gains.kp)
            params[2][1][1] = (('ki','Integral gain'), self.p.gains.ki)
            params[2][1][2] = (('kd','Differential gain'), self.p.gains.kd)
           
            self.testsuite.gui.run_simulator_command('apply_parameters', robot_id, self.p)

        #elif event == 'reset' # World constructed, safe    
            
        return False
        
    def stop_test(self):
        self.testsuite.gui.unregister_event_handler()
        self.testsuite.gui.pause_simulation()   
        self.testsuite.gui.stop_testing()

        i_iter = -1
        i_dec = 0
        i_dec_max = 50 # Simiam has 0.05 tc and 20 max
        settletime = -1
        
        for i_iter, dtheta in enumerate(self.dthetas):
            if dtheta < 0.1:
                i_dec += 1
                if i_dec > i_dec_max:
                    settletime = (i_iter-i_dec)*0.02
                    break
            else:
                i_dec = 0
                settletime = -1*0.02

        self.testsuite.respond("{:0.3f},{:0.3f}".format(settletime,abs(self.dtheta_min)))
        
    def start_test(self,challenge):
        vals = self.parseChallenge(challenge)
        
        if 'v' not in vals or 'x_g' not in vals or 'y_g' not in vals:
            raise CourseraException("Unknown challenge format. Please contact developers for assistance.")
       
        self.p = helpers.Struct()
        self.p.goal = helpers.Struct()
        self.p.goal.x = vals['x_g']
        self.p.goal.y = vals['y_g']
        self.p.velocity = helpers.Struct()
        self.p.velocity.v = vals['v']
        self.p.gains = helpers.Struct()
        self.p.gains.kp = 3
        self.p.gains.ki = 6
        self.p.gains.kd = 0.01
        
        docks = self.testsuite.gui.dockmanager.docks
        if len(docks):
            dock = docks[list(docks.keys())[0]]
            self.p.gains = dock.widget().contents.get_struct().gains
        
        self.dtheta_min = math.pi
        self.dthetas = []

        self.testsuite.gui.start_testing()
        self.testsuite.gui.register_event_handler(self)
        self.testsuite.gui.load_world('week3.xml')
        self.testsuite.gui.run_simulator_command('add_plotable',self.dtheta)
        self.testsuite.gui.run_simulator_command('add_plotable',self.dst2goal)
        
        #self.testsuite.gui.dockmanager.docks[self.dockname].widget().apply_click()
        
        self.testsuite.gui.run_simulation()
    
class Week3Test3(WeekTestCase):
    """Test 3: check if ensure_w works"""
    def __init__(self, week):
        self.testsuite = week
        self.name = "Reshaping the output for the hardware"
        self.test_id = "BlIrXfQO"
        
    def start_test(self,challenge):
        vals = self.parseChallenge(challenge)
        
        if 'v' not in vals or 'w' not in vals:
            raise CourseraException("Unknown challenge format. Please contact developers for assistance.")
        
        vd = vals['v']
        wd = vals['w']

        QuickBotSupervisor = helpers.load_by_name('week3.QBGTGSupervisor','supervisors')
        QuickBot = helpers.load_by_name('QuickBot','robots')
        from pose import Pose
        
        bot = QuickBot(Pose())
        info = bot.get_info()
        info.color = 0
        s = QuickBotSupervisor(Pose(),info)
        
        vld, vrd = s.uni2diff((vd,wd))
        vl, vr = s.ensure_w((vld,vrd))
        # Clamp to robot maxima
        vl = max(-info.wheels.max_velocity, min(info.wheels.max_velocity, vl))
        vr = max(-info.wheels.max_velocity, min(info.wheels.max_velocity, vr))
        v, w = bot.diff2uni((vl,vr))

        self.testsuite.respond("{:0.3f}".format(abs(w-wd)/wd))

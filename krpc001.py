# pylint: disable=E1101
# pylint: disable=W0612
 
'''import pickle

pickle_in = open("krpc001.pkl", "rb")
data = pickle.load(pickle_in)
pickle_in.close()
max_1 = []
for i in data:
    max_1.append(i[1])
print(f"Max-Q : {max(max_1)}")'''


 
'''dense = []
for i in data:
    if i[0]>10000.0 and i[0]<11000.0:
        dense.append([i[0],i[2]])
print(dense)'''


 
'''import math
velocity_at_max_q = math.sqrt(((max(max_1))*2)/dense[2][1])'''


 
'''print(velocity_at_max_q)'''


 
import krpc
import time
import os
import math
import pickle

clear = lambda: os.system('cls')


 
'''conn = krpc.connect("Data Logger")
vessel = conn.space_center.active_vessel
#sensor_list = vessel.parts.sensors 

#barometer = sensor_list[0]
#thermometer = sensor_list[1]

ut = conn.add_stream(getattr, conn.space_center, 'ut')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
dynamic_pressure = conn.add_stream(getattr, vessel.flight(), 'dynamic_pressure')
atmosphere_density = conn.add_stream(getattr, vessel.flight(), 'atmosphere_density')
vessel.control.sas = True



def launch_sequence():
    for i in range(12,0,-1):
        print(f"T - {i} seconds and counting...")
        time.sleep(1)
    print(f"T - 0 seconds and")
    print("LAUNCH !!!!")

launch_sequence()

vessel.control.activate_next_stage()

data = []

while True:
    data.append([altitude(),dynamic_pressure(),atmosphere_density()])
    print(f"Altitude : {altitude()} metres, Q: : {dynamic_pressure()}, Density : {atmosphere_density()}")
    time.sleep(0.5)
    if altitude()>70000:
        break

pickle_out = open("krpc001.pkl", "wb")
pickle.dump(data, pickle_out)
pickle_out.close()'''

conn = krpc.connect(name = "KRPC-001")
vessel = conn.space_center.active_vessel 

pitch = 90
max_vel = 384.59852362024066

srf = vessel.orbit.body.reference_frame

ut = conn.add_stream(getattr, conn.space_center, 'ut')
altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
speed = conn.add_stream(getattr, vessel.flight(srf), 'speed')
apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
periapsis = conn.add_stream(getattr, vessel.orbit, 'periapsis_altitude')
stage1_1 = vessel.parts.with_tag('stage1_1')[0]
fuel1_1 = conn.add_stream(stage1_1.resources.amount, 'LiquidFuel')
stage1_2 = vessel.parts.with_tag('stage1_2')[0]
fuel1_2 = conn.add_stream(stage1_2.resources.amount, 'LiquiedFuel')
#resources2 = vessel.resources_in_decouple_stage(stage = 4, cumulative = False)
#fuel2 = conn.add_stream(resources2.amount, 'LiquidFuel')

ref = 0

second_stage_activated = False

fairing_separated = False

heading = 90

timeline_save = []

def time_prettify():
    t = int(time.time()-ref)
    s = t%60
    m = (int(t/60))%60
    h = int(t/3600)
    if(s<10):
        s1 = '0'+str(s)
    else:
        s1 = str(s)
    if(m<10):
        m1 = '0'+str(m)
    else:
        m1 = str(m)
    if(h<10):
        h1 = '0'+str(h)
    else:
        h1 = str(h)
    return(h1+':'+m1+':'+s1)

def timeline(s):
    p = f"T+ {time_prettify()} => " + s
    print(p)
    timeline_save.append(p)

def ini_pitch_over():
    global pitch
    timeline("Starting Initial Pitch Over")
    for i in range(0,5):
        pitch = pitch-1
        time.sleep(0.5)
        vessel.auto_pilot.target_pitch_and_heading(pitch,heading)
    timeline(f"Initial Pitch Over completed after {int(time.time() - ref)} seconds into flight...")
    while altitude()<6500:
        pass
    gravity_turn(altitude())

def MECO(t):
    global second_stage_activated
    if not second_stage_activated:
        if fuel1_1()+fuel1_2()<30:
            vessel.control.throttle = 0
            timeline(f"MECO after {int(time.time()-ref)}seconds into flight.")
            time.sleep(0.5)
            vessel.control.activate_next_stage()
            timeline(f"First stage separated after {int(time.time()-ref)}seconds into flight.")
            time.sleep(1)
            vessel.control.activate_next_stage()
            vessel.control.throttle = t
            second_stage_activated = True

def fairing_separation():
    global fairing_separated
    if not fairing_separated:
        if altitude()>48500:
            vessel.control.activate_next_stage()
            fairing_separated = True
            timeline(f"Fairings separated after {int(time.time()-ref)}seconds into flight.")

def maxq():
    global pitch
    while altitude()<9500:
        r = speed()/max_vel
        if r>1:
            t = 0.5-r/5
            vessel.control.throttle = t
        elif r<0.5:
            t = 1
            vessel.control.throttle = 1
        else:
            t = float((1-r)+0.5)
            vessel.control.throttle = t
    while speed()<(max_vel-70):
        pass
    timeline("Vehicle now reaching Max-Q.")
    print("               The region of maximum dynamic pressure.")
    print("               A very critical moment for the mission.")
    while speed()<(max_vel-10):
        pass
    vessel.control.throttle = 0.9
    timeline("Vehicle is now at MAX Q")
    print("               Claps!!! Claps!!! Claps!!!")
    gravity_turn(altitude())

def orbital_insertion():
    global target_alt
    while apoapsis()<target_alt*0.98:
        fairing_separation()
        MECO(1)
    timeline("Aproaching target apoapsis.")
    print("               Switching to precision mode.")
    while True:
        MECO(0.1)
        vessel.control.throttle = 0.1
        if apoapsis()>target_alt:
            vessel.control.throttle = 0
            break
    timeline(f"Target apoapsis reached after {int(time.time()-ref)}seconds into flight.")
    if gto:
        time.sleep(2)
        timeline(f"Satellite successfully placed into Geostationary-Transfer Orbit after {int(time.time()-ref)}seconds into flight.")
        return(0)

    # Planning circularization burn
    r = vessel.orbit.apoapsis
    mu = vessel.orbit.body.gravitational_parameter
    a1 = vessel.orbit.semi_major_axis
    vi = math.sqrt(mu*(float(2/r)-float(1/a1)))
    vf = math.sqrt(mu*(float(2/r)-float(1/r)))
    dv = vf - vi
    node = vessel.control.add_node(ut() + vessel.orbit.time_to_apoapsis, prograde = dv+50)
        # Calculating burn time
    F = vessel.available_thrust
    Isp = vessel.specific_impulse * 9.82
    m0 = vessel.mass
    m1 = m0/math.exp(dv/Isp)
    flow_rate = F/Isp
    burn_time = (m0-m1)/flow_rate
    vessel.auto_pilot.disengage()
    time.sleep(1)
    vessel.auto_pilot.engage()
    vessel.auto_pilot.reference_frame = node.reference_frame
    vessel.auto_pilot.target_direction = (0, 1, 0)
    vessel.control.rcs = True
    time.sleep(4)
    vessel.auto_pilot.wait()
    conn.space_center.warp_to(ut() + (vessel.orbit.time_to_apoapsis - (burn_time/2)- 5))
    vessel.auto_pilot.disengage()
    vessel.control.sas = True
    vessel.control.sas_mode(conn.space_center.SASMode.prograde)
    # Finally execute the burn
    while vessel.orbit.time_to_apoapsis - (burn_time/2) > 0:
        pass
    vessel.control.throttle = 1
    timeline(f"Starting circularization burn after {int(time.time() - ref)}seconds into flight.")
    time.sleep(burn_time - 2)
    vessel.control.throttle = 0.1
    timeline("Fine turning the orbit.")
    while abs(periapsis()-apoapsis())>2000:
        pass
    vessel.control.throttle = 0.0
    node.remove()
    timeline(f"Orbit now circularized after {int(time.time()-ref)}seconds into flight")
    vessel.control.sas = True
    time.sleep(2)
    vessel.control.activate_next_stage()
    vessel.control.rcs = True
    vessel.control.forward = 1
    time.sleep(0.6)
    vessel.control.forward = 0
    vessel.control.rcs = False
    time.sleep(5)
    vessel.control.set_action_group(1,True)
    timeline(f"Satellite deployed after {int(time.time()-ref)}seconds into flight.")

def gravity_turn(start_alt):
    global pitch
    timeline("Gravity Turn Initiated.")
    end_alt = 45000
    while altitude()<=45000:
        pitch = (((-85)/(end_alt-start_alt))*(altitude()-start_alt)) + 85
        vessel.auto_pilot.target_pitch_and_heading(pitch,heading)
    timeline(f"Gravity turn completed after {int(time.time()-ref)}seconds into flight.")
    orbital_insertion()

vessel.control.sas = True
def launch_sequence():
    global pitch
    global ref
    for i in range(20,15,-1):
        print(f"T - {i} seconds and counting...")
        time.sleep(1)
        clear()
    print("T - 15 Onboard computers now have the control....")
    vessel.control.sas = False
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(pitch,90)
    time.sleep(1)
    clear()
    for i in range(14,5,-1):
        print(f"T - {i} seconds and counting...")
        time.sleep(1)
        clear()
    print(f"T - 5 Ignition sequence start")
    vessel.control.activate_next_stage()
    time.sleep(1)
    clear()
    print("T - 4 seconds and counting...")
    time.sleep(1)
    clear()
    vessel.control.throttle = 0.1
    print("T - 3 Main Engine is Ignited")
    time.sleep(1)
    vessel.control.activate_next_stage()
    clear()
    for i in range(2,0,-1):
        print(f"T - {i} seconds and counting...")
        time.sleep(1)
        clear()
    print(f"T - 0 seconds and")
    vessel.control.throttle = 1.0
    vessel.control.activate_next_stage()
    ref = time.time()
    print("        Mission Timeline")
    print("---------------------------------")
    timeline("LAUNCH !!!!")
    time.sleep(2)
    
    while True:
        if altitude()>600:
            ini_pitch_over()
            break

while True:
    print("--------LKO-LV---------")
    print("Choose type of orbit: ")
    print("1. Transfer Orbit (TO).")
    print("2. Low Kerbin Orbit (LKO).")
    menu = int(input("Enter our choice for type of orbit: "))
    menu_check = 0
    if menu == 1:
        target_alt = float(input("Enter target orbit altitude : "))
        if target_alt<=300000:
            print("This is not a Transfer Orbit. \nTry Again.")
            gto = False
            menu_check = 0
        else:
            print("Launch Sequence Initiated.")
            gto = True
            menu_check = 1
    elif menu == 2:
        target_alt = float(input("Enter target orbit altitude : "))
        if target_alt>300000:
            print("This is not a Low Kerbin Orbit. \nTry Again.")
            gto = False
            menu_check = 0
        else:
            heading = 90 - int(input("Enter Orbital Inclination : "))
            clear()
            print("Launch Sequence Initiated.")
            time.sleep(2)
            clear()
            gto = False
            menu_check = 1
    else:
        print("Don't type rubbish options.")
        menu_check = 0
    if menu_check == 1:
        break

launch_sequence()

time.sleep(5)
print("Mission Completed")

pickle_out = open("mission_timeline.txt","wb")
pickle.dump(timeline_save, pickle_out)
pickle_out.close()

conn.close()
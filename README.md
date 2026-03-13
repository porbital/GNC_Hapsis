# GNC_Hapsis

Software and hardware for GNC Hapsis.

    If you have any questions, please reach out to Matthew Allen on Slack.

## STAG Software 

The C++ code is stored in `STAG/flight_controller_v2`.

This was developed using PlatformIO, but can be used with Arduino IDE as well.

Things that still need to get done:

- [x] Implement Sensor Data (waiting on sensors to be delivered!)

- [x] Merge GNC code (`PID.cpp` is a general PID controller and needs to be properly implemented.)

- [ ] Change GNC_Activation() function to use vertical **velocity** not **acceleration** (right??)

- [ ] Test GNC system

## STAG PCB

The PCB for this project (version 3.1) is stored under `polaris3.1/`.

Things that still need to get done:

- [x] Add high-side switch to +15V power rail for MOSFET arming.
    - We are no longer doing this. 

- [x] PCB is ordered, but needs to be assembled once it arrives.
    - V3.1 PCB is finished, but has some issues (MOSFET pins switched... my b... )

- [ ] Order new PCB revision (Rev 4.1)


### AI Transparency Statement

As I'm sure you all are aware, AI is an incredibly powerful tool. However, I think that it is important to be honest and clear regarding how it is utilized in a project, especially one of this nature.

AI was used for debugging, research, and some code generation (primarily autocomplete and boilerplate code). It also generated the flight visualization script.



# Go Orbital!

# GNC_Hapsis

Software and hardware for GNC Hapsis.

    If you have any questions, please reach out to Matthew Allen on Slack.

## STAG Software 

The C++ code is stored in `STAG/files`.

This was developed using PlatformIO, but can be used with Arduino IDE as well.

Things that still need to get done:

- [ ] Implement Sensor Data (waiting on sensors to be delivered!)

- [ ] Merge GNC code (`PID.cpp` is a general PID controller and needs to be properly implemented.)

## STAG PCB

The PCB for this project (version 3.1) is stored under `polaris3.1/`.

Things that still need to get done:

- [ ] Add high-side switch to +15V power rail for MOSFET arming.

- [ ] PCB is ordered, but needs to be assembled once it arrives.


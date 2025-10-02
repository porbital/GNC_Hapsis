# Model Predictive Contorl
To develop this code we will use the do_mpc package in python. CasADi is a non linear solver that is open source. MATLAB has mutliple videos on MPC, how it works, and examples in Simulink. You can find part 1 of the MPC video series at https://youtu.be/8U0xiOkDcmw.

# Implementation
## Dynamics
This rocket passes through both the subsonic and transonic region. This is a real issue as an MPC requires a well defined dynamics which is difficult to predict in the transonic region. While other controllers like an extremum based controller would be better for the robustness of such a system, we will try to use an MPC or an adaptive MPC as it is easier to implement. 

For the supersonic dynamics we use:
Milne, B., Samson, S., Carrese, R., Gardi, A., & Sabatini, R. (2023). High-Fidelity Dynamics Modelling for the Design of a High-Altitude Supersonic Sounding Rocket. Designs, 7(1), 32. https://doi.org/10.3390/designs7010032 

For our state we need to define some components. The dynamics will be calculated in a Earth Centered Earth fixed refernce frame. This will be assumed to be an inertial reference frame for the problem, infuture iterations, we may include the coriolis and angular acceleration dur to choice of this frame. This will also help us match the resource cited above.

Our state of the rocket will be defined by:
- $x$: Position of our craft along the vector connecting the center of Earth to the intersection of equator of Earth and the prime meridian.
- $y$: Position of our craft that is the cross product of $z$ and $x$.
- $z$: Position of our craft along the vector connecting the center of Earth to its North pole
- $\phi$: Euler angle representing ....
- $\theta$: Euler angle representing ....
- $\psi$: Euler angle representing ..... 
- $\dot x$: Velocity of our craft along the $x$ axis
- $\dot y$: Velocity of our craft along the $y$ axis
- $\dot z$: Velocity of our craft along the $z$ axis
- $m$ mass of the craft at the current time.

$\vdots$

## Constraints
The constraints currently considered include;
 - Inintial position: Position of rocket on Launch day
 - Initial velocity: $\begin{bmatrix} 0\\0\\0 \end{bmatrix}$
 - Final position: Defined by team requirements
 - Maximum total impulse: $30$ Ns per cold gas thruster
 - Minimum impulse: $0.1$ Ns per cold gas thruster
 - Maximum total thrust: 15 N per cold gas thruster


## Cost function

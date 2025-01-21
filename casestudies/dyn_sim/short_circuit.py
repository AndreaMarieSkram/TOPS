import sys
from collections import defaultdict
import matplotlib.pyplot as plt
import time
import src.dynamic as dps
import src.solvers as dps_sol

if __name__ == '__main__':

    # Load model
    import casestudies.ps_data.ieee39 as model_data
    model = model_data.load()

    # Power system model
    ps = dps.PowerSystemModel(model=model)
    ps.init_dyn_sim()
    print(max(abs(ps.state_derivatives(0, ps.x_0, ps.v_0))))

    t_end = 10
    x_0 = ps.x_0.copy()

    # Solver
    sol = dps_sol.ModifiedEulerDAE(ps.state_derivatives, ps.solve_algebraic, 0, x_0, t_end, max_step=5e-3)

    # Initialize simulation
    t = 0
    res = defaultdict(list)
    t_0 = time.time()

    sc_bus_idx = ps.gen['GEN'].bus_idx_red['terminal'][0]

    # Run simulation
    while t < t_end:
        sys.stdout.write("\r%d%%" % (t/(t_end)*100))

        ################  Assignment 3 / 4: Simulation of short-circuit  ################

        #if (...):
        #    ps.y_bus_red_mod[ , ] =
        #else:
        #    ps.y_bus_red_mod[ , ] =

        ##'y_bus_red_mod' refers to the fault admittance, the inverse of fault impedance.
        ##Fault: impedance = zero --> admittance = ?

        ##[0, 0]: corresponds to 'B1' (generator bus).
        ##[1, 1]: corresponds to 'B2' (load bus).
        ##[2, 2]: corresponds to 'B3' (stiff network).

        #################################################################################

        #####  Assignment 5/6: Short-circuit with line disconnection & reconnection #####

        #if (...) and (...):
        #   (...)
        #   ps.y_bus_red_mod[ , ] =

        #if (...) and (...):
        #    (...)
        #    ps.lines['Line'].event(ps, ps.lines['Line'].par['name'][0], 'disconnect')
        #    ps.y_bus_red_mod[ , ] =

        #if (...) and (...):
        #    (...)
        #    ps.lines['Line'].event(ps, ps.lines['Line'].par['name'][0], 'connect')

        #################################################################################

        # Simulate next step
        result = sol.step()
        x = sol.y
        v = sol.v
        t = sol.t

        dx = ps.ode_fun(0, ps.x_0)

        # Store result
        res['t'].append(t)
        res['gen_speed'].append(ps.gen['GEN'].speed(x, v).copy())

    print('Simulation completed in {:.2f} seconds.'.format(time.time() - t_0))

    plt.figure()
    plt.plot(res['t'], res['gen_speed'])
    plt.xlabel('Time [s]')
    plt.ylabel('Gen. speed')
    plt.show()
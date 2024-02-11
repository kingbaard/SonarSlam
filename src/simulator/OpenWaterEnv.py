import holoocean
import matplotlib.pyplot as plt
import numpy as np

#### GET SONAR CONFIG
scenario_config = {
    "name": "SlamTest",
    "world": "SimpleUnderwater",
    "package_name": "Ocean",
    "main_agent": "ROV",
    "agents": [
        {
            "agent_name": "ROV",
            "agent_type": "HoveringAUV",
            "sensors": 
            [
                {
                    "sensor_type": "SinglebeamSonar", #TODO add specifc sensor specs (openingAngle, rangeMin, rangeMax, ect)
                    "RangeMin": 0.5,
                    "RangeMax": 20,
                    "RangeBins": 20
                },
                {
                    "sensor_type": "IMUSensor",
                },
            ],
            "control_scheme": 0, #TODO add control scheme that more represents ROV2?
            "location": [0, 0, 0],
            "rotation": [0, 0, 0]
        }
    ]
}

minR = 0.5
maxR = 20
binsR = 200

#### GET PLOT READY
plt.ion()

t = np.arange(0,50)
r = np.linspace(minR, maxR, binsR)
T, R = np.meshgrid(t, r)
data = np.zeros_like(R)

plt.grid(False)
plot = plt.pcolormesh(T, R, data, cmap='gray', shading='auto', vmin=0, vmax=1)
plt.tight_layout()
plt.gca().invert_yaxis()
plt.gcf().canvas.flush_events()

#### RUN SIMULATION
command = np.array([0,0,0,0,20])
with holoocean.make(scenario_cfg=scenario_config) as env:
    for i in range(1000):
        env.act("auv0", command)
        state = env.tick()

        if 'SinglebeamSonar' in state:
            data = np.roll(data, 1, axis=1)
            data[:,0] = state['SinglebeamSonar']

            plot.set_array(data.ravel())

            plt.draw()
            plt.gcf().canvas.flush_events()

print("Finished Simulation!")
plt.ioff()
plt.show()
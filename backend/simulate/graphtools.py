import matplotlib.pyplot as plt

SNAPSHOT_FOLDER = "backend/snapshots"

def graph_network(sim, filename=None):
    """
    Plot subway network using matplotlib
    - stations: array of Station instances
    - passengers: array of Passenger instances
    - lines: array of edges between stations
    - filename: file to save plot to, if None will display using GUI
    """
    plt.clf()

    # Plot stations
    for station in sim.stations:
        plt.scatter(station.x, station.y, marker=station.shape_marker(), s=200)
        plt.annotate(station.id, xy=(station.x, station.y-15))

        # Plot passengers
        station_passengers = [
            p for p in sim.passengers
            if p.start_station.id == station.id
        ]

        for i, p in enumerate(station_passengers):
            plt.annotate(
                f'{station.id}-{p.__str__()}',
                xy=(station.x+30, station.y-15 - 20*i)
            )

    x = [station.x for station in sim.stations]
    y = [station.y for station in sim.stations]

    # Plot lines
    for line in sim.lines:
        xaxis = [x[line[0]], x[line[1]]]
        yaxis = [y[line[0]], y[line[1]]]
        plt.plot(xaxis, yaxis)

    plt.xlim(-50,550)
    plt.ylim(-50,550)
    plt.gca().invert_yaxis()

    if filename:
        plt.savefig(f'{SNAPSHOT_FOLDER}/{filename}.png')
    else:
        plt.show()
